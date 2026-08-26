import random
from typing import List

from fastapi import Depends

from src.user_api.auth import TokenWhitelist
from src.user_api.constant.permission import Permission
from src.user_api.constant.account_constant import SALT_LENGTH
from src.user_api.db.context import TransactionContext, get_transaction_context
from src.user_api.db.db_creator import DatabaseCreator
from src.user_api.repository.account_repository import LocalAccountRepository
from src.user_api.repository.hashtag_repository import HashtagRepository
from src.user_api.repository.user_hashtag_repository import UserHashtagRepository
from src.user_api.repository.user_repository import UserRepository
from src.user_api.service.base_service import BaseService
from src.user_api.utils.hash_util import HashUtil


SEED_USERS = [
    {"name": f"test_user_{i}", "login_id": f"test_account_{i}", "password": f"test_password_{i}"}
    for i in range(1, 21)
]
SEED_USERS.append(
    {"name": "이건보", "login_id": "2gunbo74@gmail.com", "password": "kunbolee0212@"}
)

SEED_HASHTAGS = [
    "여행", "맛집", "IT", "게임", "운동",
    "패션", "뷰티", "영화", "음악", "책",
    "요리", "반려동물", "육아", "재테크", "자동차",
    "인테리어", "캠핑", "사진", "만화", "스포츠",
]

class TestService(BaseService):
    def __init__(
        self,
        database_creator: DatabaseCreator,
        user_repository: UserRepository,
        local_account_repository: LocalAccountRepository,
        hashtag_repository: HashtagRepository,
        user_hashtag_repository: UserHashtagRepository,
    ):
        self.__database_creator = database_creator
        self.__user_repository = user_repository
        self.__local_account_repository = local_account_repository
        self.__hashtag_repository = hashtag_repository
        self.__user_hashtag_repository = user_hashtag_repository

    async def drop_all(self) -> None:
        await self.__database_creator.drop_all_table()

    async def reset_all(self) -> None:
        await self.__database_creator.drop_all_table()
        await self.__database_creator.init_db()
        await TokenWhitelist.reset_whitelist()

    async def seed_test_users(self) -> List[str]:
        created_login_ids = []

        for seed in SEED_USERS:
            if await self.__local_account_repository.is_already_exist_login_id(seed["login_id"]):
                continue

            new_user = await self.__user_repository.create_user(
                name = seed["name"],
                permission = Permission.GUEST,
                with_flush = True,
            )

            new_salt = HashUtil.create_salt(SALT_LENGTH)
            hashed_password = HashUtil.get_hashed_string(seed["password"], new_salt)

            await self.__local_account_repository.create_account(
                user_pk = new_user.pk,
                login_id = seed["login_id"],
                hashed_password = hashed_password,
                personal_salt = new_salt,
                with_flush = True,
            )
            created_login_ids.append(seed["login_id"])

        return created_login_ids

    async def seed_test_hashtags(self) -> List[str]:
        created_names = []

        for name in SEED_HASHTAGS:
            existing = await self.__hashtag_repository.get_by_tag_name(name)
            if existing is not None:
                continue

            await self.__hashtag_repository.create_hashtag(name, with_flush = True)
            created_names.append(name)

        return created_names

    async def seed_random_interests(self, min_count: int = 2, max_count: int = 5) -> int:
        all_users = await self.__user_repository.find_all()
        all_hashtags = await self.__hashtag_repository.find_all()

        if not all_users or not all_hashtags:
            return 0

        created_count = 0

        for user in all_users:
            pick_count = min(random.randint(min_count, max_count), len(all_hashtags))
            picked_hashtags = random.sample(all_hashtags, pick_count)

            for hashtag in picked_hashtags:
                already_followed = await self.__user_hashtag_repository.is_exist_relation(
                    user_pk = user.pk,
                    hashtag_pk = hashtag.pk,
                )
                if already_followed:
                    continue

                await self.__user_hashtag_repository.create_relation(
                    user_pk = user.pk,
                    hashtag_pk = hashtag.pk,
                    with_flush = True,
                )
                created_count += 1

        return created_count

    async def seed_all(self) -> dict:
        users = await self.seed_test_users()
        hashtags = await self.seed_test_hashtags()
        interest_count = await self.seed_random_interests()
        return {
            "created_users": users,
            "created_hashtags": hashtags,
            "created_interests": interest_count,
        }


async def get_test_service(db_creator: DatabaseCreator = Depends(DatabaseCreator.create_object),
                           context: TransactionContext = Depends(get_transaction_context)) -> TestService:
    return TestService(
        db_creator,
        context.get_repository(UserRepository),
        context.get_repository(LocalAccountRepository),
        context.get_repository(HashtagRepository),
        context.get_repository(UserHashtagRepository)
    )