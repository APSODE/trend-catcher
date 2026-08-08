from typing import List
from warnings import deprecated

from src.user_api.dto.account_data import LocalAccountData
from src.user_api.dto.hashtag_data import HashtagData
from src.user_api.dto.serializer import serialize_many
from src.user_api.model import UserModel

@deprecated("relation 데코레이터로 변경되었음")
def _serialize_accounts(user: UserModel) -> List[LocalAccountData]:
    return serialize_many(user.local_accounts, LocalAccountData)

@deprecated("relation 데코레이터로 변경되었음")
def _serialize_interest(user: UserModel) -> List[HashtagData]:
    return serialize_many([relation.hashtag_model for relation in user.interest], HashtagData)
