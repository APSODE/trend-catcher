from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field

from src.crawler_api.util.normalize_datetime import now_normalized


class EventType(str, Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"

class DomainEvent(BaseModel):
    entity: str
    event_type: EventType
    entity_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime = Field(default_factory = now_normalized)