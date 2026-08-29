from src.llm_api.schema.hashtag_prepare_result import HashtagPrepareResultData
from src.llm_api.infrastructure.user_api_client import UserApiClient
from src.llm_api.infrastructure.database import session_scope
from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.service.hashtag_expansion_service import HashtagExpansionService
from src.llm_api.repository.hashtag_repository import HashtagRepository
from src.llm_api.infrastructure.nvidia_client import NvidiaClient
import logging

logger = logging.getLogger(__name__)

class HashtagPreparer:
    def __init__(self, user_api_client: UserApiClient, nvidia_client: NvidiaClient):
        self._user_api_client = user_api_client
        self._nvidia_client = nvidia_client

    async def run(self) -> HashtagPrepareResultData:
        hashtags = await self._user_api_client.get_all_hashtags()

        async with session_scope() as session:
            service = self._build_service(session)
            missing = await service.find_missing(hashtags)

        logger.info("해시태그 확장: [전체:%d개, 미확장:%d개]", len(hashtags), len(missing))

        result = HashtagPrepareResultData()
        for hashtag in missing:
            try:
                async with session_scope() as session:
                    await self._build_service(session).expand(hashtag)
                result.prepared += 1
            except Exception:
                logger.exception("확장 실패: [키워드:%s]", hashtag)
                result.failed += 1
        return result

    def _build_service(self, session: AsyncSession):
        return HashtagExpansionService(self._nvidia_client, HashtagRepository(session))