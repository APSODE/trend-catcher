from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .entity_model import Channel, DispatchStatus, Slot


# 구독

class SubscriptionCreateData(BaseModel):
    user_id: int
    channel: Channel = Channel.DISCORD
    webhook_url: str | None = None
    morning_enabled: bool = True
    evening_enabled: bool = True
    personalized_enabled: bool = True
    major_enabled: bool = True


class SubscriptionUpdateData(BaseModel):
    webhook_url: str | None = None
    morning_enabled: bool | None = None
    evening_enabled: bool | None = None
    personalized_enabled: bool | None = None
    major_enabled: bool | None = None
    is_active: bool | None = None


class SubscriptionOutData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    channel: str
    webhook_url: str | None
    morning_enabled: bool
    evening_enabled: bool
    personalized_enabled: bool
    major_enabled: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


# 발송

class DispatchRequestData(BaseModel):
    slot: Slot
    user_ids: list[int] | None = None
    dry_run: bool = Field(default=False, description="true면 실제 발송 없이 대상만 계산")


class DispatchResultItemData(BaseModel):
    user_id: int
    status: DispatchStatus
    error: str | None = None


class DispatchResponseData(BaseModel):
    slot: Slot
    dispatch_date: str
    total: int
    success: int
    failed: int
    skipped: int
    results: list[DispatchResultItemData]


# LLM 서비스 응답 (수정 필요)

class NewsItemData(BaseModel):
    title: str
    summary: str
    url: str | None = None


class NewsBundleData(BaseModel):
    personalized: list[NewsItemData] = []
    major: list[NewsItemData] = []