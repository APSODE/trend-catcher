from typing import List

from src.user_api.dto.account_data import AccountData
from src.user_api.dto.hashtag_data import HashtagData
from src.user_api.dto.serializer import serialize_many
from src.user_api.model import UserModel


def _serialize_accounts(user: UserModel) -> List[AccountData]:
    return serialize_many(user.accounts, AccountData)


def _serialize_interest(user: UserModel) -> List[HashtagData]:
    return serialize_many([relation.hashtag_model for relation in user.interest], HashtagData)
