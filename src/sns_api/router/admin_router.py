from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.sns_api.config import get_settings
from src.sns_api.model.database_model import get_session
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