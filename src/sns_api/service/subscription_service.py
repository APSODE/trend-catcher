from sqlalchemy.exc import IntegrityError

from src.sns_api.exception.sns_exception import ConflictError, NotFoundError
from src.sns_api.handler.user_client import UserClient
from src.sns_api.model.entity_model import Channel, SubscriptionModel
from src.sns_api.model.schema_model import SubscriptionCreateData, SubscriptionUpdateData
from src.sns_api.repository.subscription_repository import SubscriptionRepository


class SubscriptionService:
    def __init__(self, user_client: UserClient) -> None:
        self.repo = SubscriptionRepository()
        self.user_client = user_client

    async def create_subscription(self, session, payload: SubscriptionCreateData) -> SubscriptionModel:
        subscription = SubscriptionModel(
            user_id=payload.user_id,
            channel=payload.channel.value,
            morning_enabled=payload.morning_enabled,
            evening_enabled=payload.evening_enabled,
            personalized_enabled=payload.personalized_enabled,
            major_enabled=payload.major_enabled,
        )
        try:
            return await self.repo.save(session, subscription)
        except IntegrityError:
            await session.rollback()
            raise ConflictError("이미 구독 중인 유저입니다")

    async def get_subscription(self, session, sub_id: int) -> SubscriptionModel:
        sub = await self.repo.get_by_id(session, sub_id)
        if sub is None:
            raise NotFoundError("subscription not found")
        return sub

    async def get_subscriptions_by_user(self, session, user_id: int) -> list[SubscriptionModel]:
        return await self.repo.get_by_user(session, user_id)

    async def update_subscription(
            self, session, sub_id: int, payload: SubscriptionUpdateData
    ) -> SubscriptionModel:
        sub = await self.repo.get_by_id(session, sub_id)
        if sub is None:
            raise NotFoundError("subscription not found")

        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(sub, field, value)

        await session.flush()
        await session.refresh(sub)
        return sub

    async def delete_subscription(self, session, sub_id: int) -> None:
        sub = await self.repo.get_by_id(session, sub_id)
        if sub is None:
            raise NotFoundError("subscription not found")
        await self.repo.delete(session, sub)

    # 디스코드 서버 입장 -> SNS DB에서 먼저 확인, 없을 때만 User API 역조회
    # discord_id로 못 찾아도, 이미 user_id로 구독이 있으면(API로 먼저 가입한 경우) 그 row를 재사용
    async def upsert_by_discord_id(self, session, discord_user_id: str) -> SubscriptionModel:
        existing = await self.repo.get_by_discord_id(session, discord_user_id)
        if existing:
            existing.is_active = True
            await session.flush()
            return existing

        user_id = await self.user_client.get_user_id_by_discord_id(discord_user_id)
        if user_id is None:
            raise NotFoundError("연동된 유저를 찾을 수 없음")

        # user_id 기준으로 이미 구독이 있는지 한 번 더 확인 (API 선가입 케이스)
        existing_by_user = await self.repo.get_by_user(session, user_id)
        if existing_by_user:
            sub = existing_by_user[0]
            sub.discord_id = discord_user_id
            sub.is_active = True
            await session.flush()
            return sub

        subscription = SubscriptionModel(
            user_id=user_id,
            discord_id=discord_user_id,
            channel=Channel.DISCORD.value,
        )
        return await self.repo.save(session, subscription)

    # 디스코드 서버 퇴장 -> SNS DB에서 바로 찾아 비활성화
    async def deactivate_by_discord_id(self, session, discord_user_id: str) -> None:
        sub = await self.repo.get_by_discord_id(session, discord_user_id)
        if sub:
            sub.is_active = False
            await session.flush()