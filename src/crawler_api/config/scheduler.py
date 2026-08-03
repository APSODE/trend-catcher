import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.crawler_api.constant.news_sitemap import NewsSitemap
from src.crawler_api.dependencies import article
from src.crawler_api.service.crawling_pipeline import CrawlingPipeline

logger = logging.getLogger(__name__)


# 크롤링 대상 (주석 처리 안 된 항목만)
CRAWL_TARGETS: list[NewsSitemap] = [
    NewsSitemap.CHOSUN_PAGE,
    NewsSitemap.MUNHWA,
    NewsSitemap.JOONGANG,
]


async def run_scheduled_crawl():
    logger.info("스케줄러 크롤링 시작")
    service = article.get_article_service()
    try:
        result = await CrawlingPipeline.run_all_today(source = CRAWL_TARGETS)
    except Exception:
        logger.exception("크롤링 중 오류 발생")
        return

    try:
        await service.create_articles(result)
    except Exception:
        logger.exception("크롤링데이터 저장 실패")

def init_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Seoul")
    scheduler.add_job(
        run_scheduled_crawl,
        trigger = CronTrigger(hour=9, minute=0),
        id = "crawl_morning",
        replace_existing = True,
        misfire_grace_time = 3600,
        max_instances = 1,
        coalesce = True
    )
    scheduler.add_job(
        run_scheduled_crawl,
        trigger = CronTrigger(hour=21, minute=0),
        id = "crawl_evening",
        replace_existing = True,
        misfire_grace_time = 3600,
        max_instances = 1,
        coalesce = True
    )

    return scheduler