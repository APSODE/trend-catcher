from src.user_api.db.redis_creator import RedisCreator
from src.user_api.constant.auth_constant import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from src.user_api.dto.token_data import JsonWebToken, TokenPair, TokenType
from src.user_api.utils.jwt_util import JwtUtil


class TokenWhitelist:
    @staticmethod
    def __create_key(jwt: JsonWebToken) -> str:
        return f"whitelist:{jwt.type}:{jwt.account.account_type}:{jwt.account.pk}:{jwt.session_id}"

    @staticmethod
    def __create_ttl(token_type: TokenType) -> int:
        if token_type == TokenType.ACCESS:
            return ACCESS_TOKEN_EXPIRE_MINUTES * 60
        else:
            return REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

    @staticmethod
    async def register(token: str, token_type: TokenType) -> None:
        await RedisCreator().client.set(
            name = TokenWhitelist.__create_key(jwt = JwtUtil.decode_token(token, token_type)),
            value = token,
            ex = TokenWhitelist.__create_ttl(token_type = token_type),
        )

    @staticmethod
    async def token_pair_register(token_pair: TokenPair) -> None:
        await TokenWhitelist.register(token = token_pair.access_token, token_type = TokenType.ACCESS)
        await TokenWhitelist.register(token = token_pair.refresh_token, token_type = TokenType.REFRESH)

    @staticmethod
    async def is_registered(jwt: JsonWebToken, raw_token: str) -> bool:
        stored_token = await RedisCreator().client.get(
            TokenWhitelist.__create_key(jwt = jwt)
        )
        return stored_token == raw_token

    @staticmethod
    async def revoke_all_by_session(jwt: JsonWebToken) -> None:
        client = RedisCreator().client
        pattern = f"whitelist:*:{jwt.account.account_type}:{jwt.account.pk}:{jwt.session_id}"
        async for key in client.scan_iter(match = pattern):
            await client.delete(key)

    @staticmethod
    async def reset_whitelist():
        await RedisCreator().client.flushdb()

