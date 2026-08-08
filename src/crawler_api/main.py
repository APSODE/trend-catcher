from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.crawler_api.config.scheduler import init_scheduler
from src.crawler_api.db.database_session import init_db
from src.crawler_api.event.event_publisher import EventPublisher
from src.crawler_api.route import article_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #DB 실행
    client = await init_db()
    app.state.mongo_client = client

    #event publisher
    event_publisher = EventPublisher()
    #event_publisher.subscribe()
    app.state.event_publisher = event_publisher

    #스케줄러
    scheduler = init_scheduler(app)
    scheduler.start()
    app.state.scheduler = scheduler

    yield

    scheduler.shutdown()
    await client.close()


CrawlerAPI = FastAPI(
    title="Crawler API",
    lifespan=lifespan,
    description="Crawler API",
)

CrawlerAPI.include_router(article_router.router)