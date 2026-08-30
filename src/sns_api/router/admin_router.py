from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.sns_api.config import get_settings
from src.sns_api.model.database_model import get_session
from src.sns_api.model.entity_model import Slot, DispatchStatus, utc_now
from src.sns_api.model.schema_model import DispatchLogOutData
from src.sns_api.repository.dispatch_repository import DispatchRepository
from src.sns_api.router.dispatch_router import verify_internal_token

settings = get_settings()

router = APIRouter(prefix="/admin", tags=["admin"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/reset-db",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_internal_token)],
)
async def reset_sns_db(session: SessionDep):
    if not settings.debug:
        raise HTTPException(status_code=403, detail="disabled unless debug mode")

    await session.execute(text("TRUNCATE TABLE SNS_DISPATCH_LOG"))
    await session.execute(text("TRUNCATE TABLE SNS_SUBSCRIPTION"))
    await session.commit()

    return {"status": "sns db reset complete"}


@router.get(
    "/dispatch-logs",
    response_model=list[DispatchLogOutData],
    dependencies=[Depends(verify_internal_token)],
)
async def list_dispatch_logs(
    session: SessionDep,
    dispatch_date: str | None = None,
    slot: Slot | None = None,
    status_filter: DispatchStatus | None = None,
):
    if dispatch_date is None:
        dispatch_date = utc_now().strftime("%Y-%m-%d")
    return await DispatchRepository().list_logs(session, dispatch_date, slot, status_filter)


@router.delete(
    "/dispatch-logs",
    dependencies=[Depends(verify_internal_token)],
)
async def delete_dispatch_logs(
    session: SessionDep,
    dispatch_date: str | None = None,
    slot: Slot | None = None,
    user_id: int | None = None,
    include_major: bool = False,
    only_failed: bool = True,
):
    if not settings.debug:
        raise HTTPException(status_code=403, detail="disabled unless debug mode")

    if dispatch_date is None:
        dispatch_date = utc_now().strftime("%Y-%m-%d")

    deleted_count = await DispatchRepository().delete_logs(
        session, dispatch_date, slot, user_id, include_major, only_failed
    )
    await session.commit()

    return {
        "status": "deleted",
        "dispatch_date": dispatch_date,
        "slot": slot.value if slot else "ALL",
        "user_id": user_id if user_id is not None else "ALL",
        "deleted_count": deleted_count,
    }