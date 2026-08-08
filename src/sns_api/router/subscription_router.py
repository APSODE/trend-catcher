from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.sns_api.decorator.handle_error import handle_errors
from src.sns_api.model.database_model import get_session
from src.sns_api.model.schema_model import SubscriptionCreateData, SubscriptionOutData, SubscriptionUpdateData
from src.sns_api.service.subscription_service import SubscriptionService

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
service = SubscriptionService()


@router.post("", response_model=SubscriptionOutData, status_code=status.HTTP_201_CREATED)
@handle_errors
async def create_subscription(payload: SubscriptionCreateData, session: SessionDep):
    return await service.create_subscription(session, payload)


@router.get("/{sub_id}", response_model=SubscriptionOutData)
@handle_errors
async def get_subscription(sub_id: int, session: SessionDep):
    return await service.get_subscription(session, sub_id)


@router.get("/user/{user_id}", response_model=list[SubscriptionOutData])
@handle_errors
async def list_user_subscriptions(user_id: int, session: SessionDep):
    return await service.get_subscriptions_by_user(session, user_id)


@router.patch("/{sub_id}", response_model=SubscriptionOutData)
@handle_errors
async def update_subscription(sub_id: int, payload: SubscriptionUpdateData, session: SessionDep):
    return await service.update_subscription(session, sub_id, payload)


@router.delete("/{sub_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_errors
async def delete_subscription(sub_id: int, session: SessionDep):
    await service.delete_subscription(session, sub_id)