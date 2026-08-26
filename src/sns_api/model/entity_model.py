from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Identity,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .database_model import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Slot(str, Enum):
    MORNING = "MORNING"
    EVENING = "EVENING"


class Channel(str, Enum):
    DISCORD = "DISCORD"


class DispatchStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class SubscriptionModel(Base):
    __tablename__ = "SNS_SUBSCRIPTION"

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    discord_id: Mapped[str | None] = mapped_column(String(30), index=True, nullable=True)

    channel: Mapped[str] = mapped_column(String(20), default=Channel.DISCORD.value, nullable=False)

    morning_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    evening_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    personalized_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    major_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)


class DispatchLogModel(Base):
    __tablename__ = "SNS_DISPATCH_LOG"
    __table_args__ = (
        UniqueConstraint("user_id", "slot", "dispatch_date", name="uq_dispatch_log_user_slot_date"),  # ★ 추가
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    subscription_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    slot: Mapped[str] = mapped_column(String(20), nullable=False)
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    dispatch_date: Mapped[str] = mapped_column(String(10), index=True, nullable=False)

    status: Mapped[str] = mapped_column(String(20), default=DispatchStatus.PENDING.value, nullable=False)
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    payload: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)