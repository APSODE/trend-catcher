from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..model.entity_model import Slot, SubscriptionModel


class SubscriptionRepository:
    # 구독 저장
    async def save(self, session: AsyncSession, subscription: SubscriptionModel) -> SubscriptionModel:
        session.add(subscription)
        await session.flush()
        await session.refresh(subscription)
        return subscription

    # id를 통한 구독 조회
    async def get_by_id(self, session: AsyncSession, sub_id: int) -> SubscriptionModel | None:
        return await session.get(SubscriptionModel, sub_id)

    # 유저의 구독 전체 조회
    async def get_by_user(self, session: AsyncSession, user_id: int) -> list[SubscriptionModel]:
        query = select(SubscriptionModel).where(SubscriptionModel.user_id == user_id)
        result = await session.execute(query)
        return list(result.scalars().all())

    # 슬롯(아침/저녁)을 구독 중인 활성 구독 목록
    async def list_active_for_slot(self, session: AsyncSession, slot: Slot) -> list[SubscriptionModel]:
        query = select(SubscriptionModel).where(SubscriptionModel.is_active.is_(True))
        if slot == Slot.MORNING:
            query = query.where(SubscriptionModel.morning_enabled.is_(True))
        else:
            query = query.where(SubscriptionModel.evening_enabled.is_(True))
        result = await session.execute(query)
        return list(result.scalars().all())

    # 아침/저녁 구독 목록
    async def list_active_for_users(
        self, session: AsyncSession, slot: Slot, user_ids: list[int]
    ) -> list[SubscriptionModel]:
        if not user_ids:
            return []
        query = select(SubscriptionModel).where(
            SubscriptionModel.is_active.is_(True),
            SubscriptionModel.user_id.in_(user_ids),
        )
        if slot == Slot.MORNING:
            query = query.where(SubscriptionModel.morning_enabled.is_(True))
        else:
            query = query.where(SubscriptionModel.evening_enabled.is_(True))
        result = await session.execute(query)
        return list(result.scalars().all())

    # 구독 삭제
    async def delete(self, session: AsyncSession, subscription: SubscriptionModel) -> None:
        await session.delete(subscription)
        await session.flush()