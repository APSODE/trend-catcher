from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.crawler_api.config.scheduler import init_scheduler
from src.crawler_api.config.setting import get_settings
from src.crawler_api.db.database_session import init_db
from src.crawler_api.route import article_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    #DB 실행
    client = await init_db()
    app.state.mongo_client = client

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:CrawlerAPI", host = "0.0.0.0", port = 8081, workers =1, log_level = "info", reload = True)