import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from src.crawler_api.constant.crawling_time import CRAWLING_TIME
from src.crawler_api.constant.news_sitemap import NewsSitemap
from src.crawler_api.db.article_context import ArticleContext
from src.crawler_api.dependencies.article import create_article_service
from src.crawler_api.service.crawling_pipeline import CrawlingPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_scheduled_crawl(app: FastAPI):
    logger.info("scheduler crawling start")

    try:
        result = await CrawlingPipeline.run_all_today(sources=list(NewsSitemap))
    except Exception as e:
        logger.exception("crawling failed: %s", e)
        return
    logger.info("crawling complete")

    try:
        # 기존 depends에 경우 fastapi에서 조립하여 service return 그러나 스케줄러의 경우 fastapi가 조립하지않음
        async with ArticleContext(app.state.mongo_client) as ctx:
            service = await create_article_service(ctx)
            await service.create_articles(result)
    except Exception as e:
        logger.exception("crawler save failed : %s", e)

def init_scheduler(app: FastAPI) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Seoul")

    scheduler.add_job(
        run_scheduled_crawl,
        args=[app],
        trigger=CronTrigger(hour="*", minute=CRAWLING_TIME),
        id="crawl_hourly",
        replace_existing=True, #중복 등록 방지
        misfire_grace_time=3600,
        max_instances=1, # 최대 실행가능한 갯수
        coalesce=True #지연되도 한번만실행 -> 크롤링이라 한번만 실행이 맞음
    )

    return scheduler