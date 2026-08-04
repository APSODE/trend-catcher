from src.sns_api.exception.sns_exception import NotFoundError
from src.sns_api.model.entity_model import SubscriptionModel
from src.sns_api.model.schema_model import SubscriptionCreateData, SubscriptionUpdateData
from src.sns_api.repository.subscription_repository import SubscriptionRepository


class SubscriptionService:
    def __init__(self) -> None:
        self.repo = SubscriptionRepository()

    async def create_subscription(self, session, payload: SubscriptionCreateData) -> SubscriptionModel:
        subscription = SubscriptionModel(
            user_id=payload.user_id,
            channel=payload.channel.value,
            webhook_url=payload.webhook_url,
            morning_enabled=payload.morning_enabled,
            evening_enabled=payload.evening_enabled,
            personalized_enabled=payload.personalized_enabled,
            major_enabled=payload.major_enabled,
        )
        return await self.repo.save(session, subscription)

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
