from typing import List
from warnings import deprecated

from src.user_api.dto import HashtagData, LocalAccountData
from src.user_api.dto.serializer import serialize_many
from src.user_api.model import UserModel

@deprecated("relation 데코레이터로 변경되었음")
def _serialize_accounts(user: UserModel) -> List[LocalAccountData]:
    return serialize_many(user.local_accounts, LocalAccountData)

@deprecated("relation 데코레이터로 변경되었음")
def _serialize_interest(user: UserModel) -> List[HashtagData]:
    return serialize_many([relation.hashtag_model for relation in user.interest], HashtagData)
