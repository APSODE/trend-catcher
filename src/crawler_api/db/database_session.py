import logging

from pymongo import AsyncMongoClient
from beanie import init_beanie

from src.crawler_api.config.setting import get_settings
from src.crawler_api.model.article import Article


logger = logging.getLogger(__name__)

async def init_db() -> AsyncMongoClient:
    settings = get_settings()
    client = AsyncMongoClient(settings.mongodb_uri.get_secret_value())

    await init_beanie(
        database=client[settings.mongodb_name],
        #model 추가 시 수정
        document_models=[Article]
    )
    return client