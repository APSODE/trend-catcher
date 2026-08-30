from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.sns_api.model.entity_model import Channel, DispatchStatus, Slot


# 구독

class SubscriptionCreateData(BaseModel):
    user_id: int
    channel: Channel = Channel.DISCORD
    morning_enabled: bool = True
    evening_enabled: bool = True
    personalized_enabled: bool = True
    major_enabled: bool = True


class SubscriptionUpdateData(BaseModel):
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

class DispatchLogOutData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    slot: str
    channel: str
    dispatch_date: str
    status: str
    attempt_count: int
    error_message: str | None
    created_at: datetime
    sent_at: datetime | None

# LLM과 소통시 받을 것들
class NewsReferenceData(BaseModel):
    crawled_id: str
    score: float

# 최종 완성된 뉴스에 필요한 것들(크롤러로부터 받은 것들)
class NewsItemData(BaseModel):
    title: str
    url: str | None = None
    image_url: str | None = None

class NewsBundleData(BaseModel):
    personalized: list[NewsItemData] = []
    major: list[NewsItemData] = []