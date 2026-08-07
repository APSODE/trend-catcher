from typing import AsyncGenerator
from warnings import deprecated

from src.user_api.db.db_creator import DatabaseCreator
from src.user_api.db.context.transaction_context import TransactionContext
from src.user_api.repository.account_repository import LocalAccountRepository
from src.user_api.repository.user_repository import UserRepository

@deprecated("BaseService에 정의된 create_dependency로 사용")
class UserAccountContext(TransactionContext):
    @property
    def users(self) -> UserRepository:
        return self.get_repository(UserRepository)

    @property
    def accounts(self) -> LocalAccountRepository:
        return self.get_repository(LocalAccountRepository)

@deprecated("BaseService에 정의된 create_dependency로 사용")
async def get_user_account_context() -> AsyncGenerator[UserAccountContext, None]:
    context = UserAccountContext(
        session_factory = DatabaseCreator().session,
        repository_factories = {
            UserRepository: UserRepository,
            LocalAccountRepository: LocalAccountRepository,
        }
    )

    async with context:
        yield context