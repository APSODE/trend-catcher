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