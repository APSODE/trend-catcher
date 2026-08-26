from hmac import compare_digest
from typing import Optional
from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from src.user_api.constant.account_constant import SALT_LENGTH, SOCIAL, AccountProvider
from src.user_api.constant.permission import Permission
from src.user_api.dto.serializer import serialize, serialize_many, required_relation
from src.user_api.exceptions.account_exceptions import IsAlreadyExistLoginID, InvalidCredentialData, \
    AlreadyLinkedAccount, UnlinkedSocialAccount, AlreadyLinkedProvider, \
    CannotUnlinkLastLoginMethod, DeleteConfirmationMismatch
from src.user_api.auth import TokenWhitelist, OAuth2Client
from src.user_api.dto import LocalLoginRequest, LocalRegisterRequest, DeleteRequest, TokenPair, TokenType, AccountData, \
    SocialRegisterRequest, SocialLoginRequest, SocialLinkRequest, SocialAccountData, DataCollectionResponse, UserData
from src.user_api.exceptions.user_exceptions import UnknownUserData
from src.user_api.repository import LocalAccountRepository, UserRepository, SocialAccountRepository
from src.user_api.service import BaseService
from src.user_api.utils import HashUtil, JwtUtil
from user_api.exceptions.auth_exceptions import InvalidToken


class UserAccountService(BaseService):
    def __init__(self,
                 local_account_repository: LocalAccountRepository,
                 social_account_repository: SocialAccountRepository,
                 user_repository: UserRepository):
        self.__local_account_repository = local_account_repository
        self.__social_account_repository = social_account_repository
        self.__user_repository = user_repository

    @staticmethod
    async def _issue_jwt_for_account(account: AccountData, session_id: Optional[str] = None) -> TokenPair:
        if session_id is None:
            session_id = str(uuid4())

        token_pair = JwtUtil.create_token_pair(
            session_id = session_id,
            account = account
        )

        await TokenWhitelist.token_pair_register(token_pair)
        return token_pair


    async def local_register(self, register_data: LocalRegisterRequest):
        await self.require_unique_login_id(register_data.login_id)

        new_user = await self.__user_repository.create_user(
            name = register_data.name,
            permission = register_data.permission,
            interest = register_data.interest,
            with_flush = True
        )

        new_salt = HashUtil.create_salt(SALT_LENGTH)
        hashed_password = HashUtil.get_hashed_string(register_data.password, new_salt)

        try:
            await self.__local_account_repository.create_account(
                user_pk = new_user.pk,
                login_id = register_data.login_id,
                hashed_password = hashed_password,
                personal_salt = new_salt,
                with_flush = True
            )
        except IntegrityError:
            await self.__local_account_repository.db_controller.rollback()
            raise IsAlreadyExistLoginID(login_id = register_data.login_id)

    async def social_register(self, register_data: SocialRegisterRequest) -> TokenPair:
        oauth_response = await OAuth2Client.get_client(register_data.provider).fetch_user_info(register_data.provider_access_token)

        existing_account = await self.__social_account_repository.get_account_by_provider_id(
            provider = register_data.provider,
            provider_user_id = oauth_response.provider_user_id,
        )

        if existing_account is not None:
            raise AlreadyLinkedAccount()

        new_user = await self.__user_repository.create_user(
            name = oauth_response.name or f"{register_data.provider.value}_{oauth_response.provider_user_id}",
            permission = Permission.GUEST,
            with_flush = True,
        )

        new_account = await self.__social_account_repository.create_account(
            user_pk = new_user.pk,
            provider = register_data.provider,
            provider_user_id = oauth_response.provider_user_id,
            with_flush = True,
        )

        return await self._issue_jwt_for_account(serialize(new_account, AccountData))

    async def local_login(self, login_data: LocalLoginRequest) -> TokenPair:
        target_account = await self.__local_account_repository.get_account_by_login_id(login_id = login_data.login_id)

        if target_account is None:
            raise InvalidCredentialData()

        hashed_input_password = HashUtil.get_hashed_string(
            target = login_data.password,
            salt = target_account.personal_salt
        )

        compare_result = compare_digest(hashed_input_password, target_account.hashed_password)

        if not compare_result:
            raise InvalidCredentialData()

        return await self._issue_jwt_for_account(serialize(target_account, AccountData))

    async def social_login(self, login_data: SocialLoginRequest) -> TokenPair:
        oauth_response = await OAuth2Client.get_client(login_data.provider).fetch_user_info(login_data.provider_access_token)

        target_account = await self.__social_account_repository.get_account_by_provider_id(
            provider = login_data.provider,
            provider_user_id = oauth_response.provider_user_id,
        )

        if target_account is None:
            raise UnlinkedSocialAccount()

        return await self._issue_jwt_for_account(serialize(target_account, AccountData))

    async def link_social_account(self, user_pk: int, link_data: SocialLinkRequest) -> AccountData:
        if await self.__social_account_repository.is_already_registered_provider(user_pk, link_data.provider):
            raise AlreadyLinkedProvider()

        oauth_response = await OAuth2Client.get_client(link_data.provider).fetch_user_info(link_data.provider_access_token)

        existing_account = await self.__social_account_repository.get_account_by_provider_id(
            provider = link_data.provider,
            provider_user_id = oauth_response.provider_user_id,
        )
        if existing_account is not None:
            raise AlreadyLinkedAccount()

        new_account = await self.__social_account_repository.create_account(
            user_pk = user_pk,
            provider = link_data.provider,
            provider_user_id = oauth_response.provider_user_id,
            with_flush = True,
        )

        return serialize(new_account, AccountData)

    async def unlink_social_account(self, user_pk: int, provider: AccountProvider):
        target_user = await self.__user_repository.get_by_pk(
            target_pk = user_pk,
            load_relations = required_relation(UserData)
        )

        if target_user is None:
            raise UnknownUserData()

        if len(target_user.local_accounts) <= 0:
            raise CannotUnlinkLastLoginMethod()

        await self.__social_account_repository.delete_or_raise(
            exception_factory = UnlinkedSocialAccount,
            filter = (self.__social_account_repository.model_class.user_fk == user_pk)
                     & (self.__social_account_repository.model_class.provider == provider),
            with_flush = True,
        )

    async def get_linked_account_info(self, user_pk: int) -> DataCollectionResponse[SocialAccountData]:
        target_user = await self.__user_repository.get_by_pk(
            target_pk = user_pk,
            load_relations = required_relation(UserData)
        )

        if target_user is None:
            raise UnknownUserData()

        return DataCollectionResponse(
            amount = len(target_user.social_accounts),
            datas = serialize_many(target_user.social_accounts, SocialAccountData)
        )


    async def change_password(self, current_account: AccountData, new_password: str):
        if current_account.account_type == SOCIAL:
            raise InvalidCredentialData()

        new_salt = HashUtil.create_salt(SALT_LENGTH)
        hashed_password = HashUtil.get_hashed_string(new_password, new_salt)

        await self.__local_account_repository.update_password(
            target_account_pk = current_account.pk,
            new_password = hashed_password,
            new_salt = new_salt,
            with_flush = True
        )

    @staticmethod
    async def logout(access_token: str):
        user_jwt = JwtUtil.decode_token(access_token, expected_type = TokenType.ACCESS)
        await TokenWhitelist.revoke_all_by_session(user_jwt)

    @staticmethod
    async def refresh_token(refresh_token: str) -> TokenPair:
        user_jwt = JwtUtil.decode_token(refresh_token, expected_type=TokenType.REFRESH)

        if not await TokenWhitelist.is_registered(user_jwt, refresh_token):
            raise InvalidToken()

        await TokenWhitelist.revoke_all_by_session(user_jwt)
        return await UserAccountService._issue_jwt_for_account(user_jwt.account)

    async def delete_user(self, user_pk: int, delete_data: DeleteRequest):
        target_user = await self.__user_repository.get_by_pk(user_pk)

        if target_user is None:
            raise UnknownUserData()

        if target_user.name != delete_data.name:
            raise DeleteConfirmationMismatch()

        await self.__user_repository.delete_by_pk(
            target_pk = user_pk,
            load_relations = required_relation(UserData),
            with_flush = True
        )



    async def require_unique_login_id(self, new_login_id: str) -> bool:
        if await self.__local_account_repository.is_already_exist_login_id(new_login_id):
            raise IsAlreadyExistLoginID(login_id = new_login_id)

        return True



get_user_account_service = UserAccountService.create_dependency(
    user_repository = UserRepository,
    local_account_repository = LocalAccountRepository,
    social_account_repository = SocialAccountRepository
)
