from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.entity_model import DispatchLogModel, DispatchStatus, Slot

class DispatchRepository:
    # 오늘 이 슬롯에 이미 성공 발송했는지 여부
    async def is_already_sent(
        self, session: AsyncSession, user_id: int, slot: Slot, dispatch_date: str
    ) -> bool:
        query = select(DispatchLogModel.id).where(
            DispatchLogModel.user_id == user_id,
            DispatchLogModel.slot == slot.value,
            DispatchLogModel.dispatch_date == dispatch_date,
            DispatchLogModel.status == DispatchStatus.SUCCESS.value,
        )
        result = await session.execute(query)
        return result.first() is not None

    # 발송 기록 저장
    async def save(self, session: AsyncSession, log: DispatchLogModel) -> DispatchLogModel:
        session.add(log)
        await session.flush()
        await session.refresh(log)
        return log

    # 발송 성공 처리
    async def mark_success(self, session: AsyncSession, log: DispatchLogModel) -> None:
        log.status = DispatchStatus.SUCCESS.value
        log.attempt_count += 1
        log.sent_at = datetime.utcnow()
        log.error_message = None
        await session.flush()

    # 발송 실패 처리
    async def mark_failed(self, session: AsyncSession, log: DispatchLogModel, error: str) -> None:
        log.status = DispatchStatus.FAILED.value
        log.attempt_count += 1
        log.error_message = error[:1000]
        await session.flush()

    # 유저 발송 이력 조회 (최신순)
    async def get_history(
        self, session: AsyncSession, user_id: int, limit: int = 30
    ) -> list[DispatchLogModel]:
        query = (
            select(DispatchLogModel)
            .where(DispatchLogModel.user_id == user_id)
            .order_by(DispatchLogModel.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())