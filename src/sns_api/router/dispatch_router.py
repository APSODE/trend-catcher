from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.sns_api.config import get_settings
from src.sns_api.decorator.handle_error import handle_errors
from src.sns_api.model.database_model import get_session
from src.sns_api.model.entity_model import Slot
from src.sns_api.service.dispatch_service import DispatchService

settings = get_settings()

router = APIRouter(prefix="/dispatch", tags=["dispatch"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
service = DispatchService()


# 내부 토큰 검증 (스케줄러 요청 용도)
async def verify_internal_token(x_internal_token: Annotated[str, Header()]) -> None:
    if x_internal_token != settings.internal_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid internal token",
        )


@router.post(
    "/{slot}",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(verify_internal_token)],
)
@handle_errors
# 뉴스 전송
async def trigger_dispatch(slot: Slot, request: Request, session: SessionDep):
    discord_client = request.app.state.discord_client
    user_client = request.app.state.user_client
    llm_client = request.app.state.llm_client
    crawler_client = request.app.state.crawler_client

    if slot == Slot.MORNING:
        slot_label = "아침"
    else:
        slot_label = "저녁"
    # 주요 뉴스 전송
    #await service.dispatch_major(
     #   discord_client, llm_client, crawler_client,
     #   settings.major_news_channel_id, slot_label,
    #)

    # 개인화 뉴스 전송
    await service.dispatch_personalized(
        session, slot, slot_label,
        discord_client, user_client, llm_client, crawler_client,
    )

    return {"status": "dispatch triggered", "slot": slot.value}
