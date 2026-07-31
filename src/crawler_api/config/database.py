from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie

from src.crawler_api.config.setting import get_settings
from src.crawler_api.model.article import Article


async def init_db() -> AsyncMongoClient:
    settings = get_settings()
    client = AsyncMongoClient(settings.mongodb_uri)

    await init_beanie(
        database=client[settings.mongodb_name],
        #model 추가 시 수정
        document_models=[
            Article
        ],
    )
    return client

#서버 생명주기 관리 fail-fast 방식으로
@asynccontextmanager
async def lifespan(app: FastAPI):
    #서버 실행
    client = await init_db()
    app.state.mongo_client = client

    #서버 실행될동안 대기
    yield

    #서버 종료시 클라이언트 객체도 종료되게
    await client.close()




#TODO lifespan, failfast 식 알아보기