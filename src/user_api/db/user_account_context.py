from src.user_api.db.transaction_context import TransactionContext
from src.user_api.repository.account_repository import AccountRepository
from src.user_api.repository.user_repository import UserRepository


class UserAccountContext(TransactionContext):
    @property
    def users(self) -> UserRepository:
        return self.get_repository(UserRepository)

    @property
    def accounts(self) -> AccountRepository:
        return self.get_repository(AccountRepository)