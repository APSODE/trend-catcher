from typing import AsyncGenerator
from warnings import deprecated

from src.user_api.db.context.transaction_context import TransactionContext
from src.user_api.db.db_creator import DatabaseCreator
from src.user_api.repository.hashtag_repository import HashtagRepository
from src.user_api.repository.user_hashtag_repository import UserHashtagRepository
from src.user_api.repository.user_repository import UserRepository

@deprecated("BaseService에 정의된 create_dependency로 사용")
class UserHashtagContext(TransactionContext):
    @property
    def users(self) -> UserRepository:
        return self.get_repository(UserRepository)

    @property
    def hashtags(self) -> HashtagRepository:
        return self.get_repository(HashtagRepository)

    @property
    def relations(self) -> UserHashtagRepository:
        return self.get_repository(UserHashtagRepository)

@deprecated("BaseService에 정의된 create_dependency로 사용")
async def get_user_hashtag_context() -> AsyncGenerator[UserHashtagContext, None]:
    context = UserHashtagContext(
        session_factory = DatabaseCreator().session,
        repository_factories = {
            UserRepository: UserRepository,
            HashtagRepository: HashtagRepository,
            UserHashtagRepository: UserHashtagRepository
        }
    )

    async with context:
        yield context