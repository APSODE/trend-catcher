from hmac import compare_digest
from uuid import uuid4

from fastapi import Depends

from src.user_api.auth.jwt_auth import TokenWhitelist
from src.user_api.constant.account_constant import SALT_LENGTH
from src.user_api.db.context.user_account_context import (
    UserAccountContext,
    get_user_account_context as _get_user_account_context
)
from src.user_api.dto.request_data import LoginRequest, RegisterRequest, DeleteRequest
from src.user_api.dto.token_data import TokenPair, TokenType
from src.user_api.exceptions.account_exceptions import IsAlreadyExistLoginID, InvalidCredentialData
from src.user_api.repository.account_repository import AccountRepository
from src.user_api.repository.user_repository import UserRepository
from src.user_api.service.base_service import BaseService
from src.user_api.utils.hash_util import HashUtil
from src.user_api.utils.jwt_util import JwtUtil


class UserAccountService(BaseService):
    def __init__(self, account_repository: AccountRepository, user_repository: UserRepository):
        self.__account_repository = account_repository
        self.__user_repository = user_repository

    async def register(self, register_data: RegisterRequest):
        await self.require_unique_login_id(register_data.login_id)

        new_user = await self.__user_repository.create_user(
            name = register_data.name,
            permission = register_data.permission,
            interest = register_data.interest,
            with_flush = True
        )

        new_salt = HashUtil.create_salt(SALT_LENGTH)
        hashed_password = HashUtil.get_hashed_string(register_data.password, new_salt)

        await self.__account_repository.create_account(
            user_pk = new_user.pk,
            login_id = register_data.login_id,
            hashed_password = hashed_password,
            personal_salt = new_salt,
            with_flush = True
        )

    async def login(self, login_data: LoginRequest) -> TokenPair:
        target_account = await self.__account_repository.get_account_by_login_id(login_id = login_data.login_id)

        if target_account is None:
            raise InvalidCredentialData()

        hashed_input_password = HashUtil.get_hashed_string(
            target = login_data.password,
            salt = target_account.personal_salt
        )

        compare_result = compare_digest(hashed_input_password, target_account.hashed_password)

        if not compare_result:
            raise InvalidCredentialData()

        jwt_token_pair = JwtUtil.create_token_pair(
            session_id = str(uuid4()),
            account_pk = target_account.pk
        )
        await TokenWhitelist.token_pair_register(jwt_token_pair)
        return jwt_token_pair

    async def logout(self, access_token: str):
        user_jwt = JwtUtil.decode_token(access_token, expected_type = TokenType.ACCESS)
        await TokenWhitelist.revoke_all_by_session(user_jwt)

    async def refresh_token(self, refresh_token: str) -> TokenPair:
        user_jwt = JwtUtil.decode_token(refresh_token, expected_type = TokenType.REFRESH)
        await TokenWhitelist.revoke_all_by_session(user_jwt)
        user_token_pair = JwtUtil.create_token_pair(
            session_id = user_jwt.session_id,
            account_pk = user_jwt.account_pk
        )
        await TokenWhitelist.token_pair_register(user_token_pair)
        return user_token_pair

    async def delete(self, delete_data: DeleteRequest):
        await self.__account_repository.delete_by_login_id(delete_data.login_id)

    async def require_unique_login_id(self, new_login_id: str) -> bool:
        if await self.__account_repository.is_already_exist_login_id(new_login_id):
            raise IsAlreadyExistLoginID(login_id = new_login_id)

        return True


get_user_account_service = UserAccountService.create_dependency(
    user_repository = UserRepository,
    account_repository = AccountRepository
)

