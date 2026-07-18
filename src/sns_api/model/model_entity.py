"""
SNS 서비스 ORM 엔티티.
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .model_database import Base


class Slot(str, Enum):
    # 발송 시간대
    MORNING = "MORNING"
    EVENING = "EVENING"


class Channel(str, Enum):
    # 발송 대상 (일단 디코)
    DISCORD = "DISCORD"


class DispatchStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class SubscriptionModel(Base):
    # 구독 설정
    # user_id 는 User 서비스의 PK 를 참조

    __tablename__ = "SNS_SUBSCRIPTION"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)

    channel: Mapped[str] = mapped_column(String(20), default=Channel.DISCORD.value, nullable=False)
    # Discord Webhook URL (유저/채널별). 없으면 서비스 기본 webhook 으로 fallback.
    webhook_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # 아침/저녁 각각 수신 여부
    morning_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    evening_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # 개인화 뉴스 / 주요 뉴스 수신 여부
    personalized_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    major_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class DispatchLogModel(Base):
    __tablename__ = "SNS_DISPATCH_LOG"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    subscription_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)

    slot: Mapped[str] = mapped_column(String(20), nullable=False)       # MORNING / EVENING
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    dispatch_date: Mapped[str] = mapped_column(String(10), index=True, nullable=False)  # YYYY-MM-DD

    status: Mapped[str] = mapped_column(
        String(20), default=DispatchStatus.PENDING.value, nullable=False
    )
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 발송한 메시지 원본 (감사/재발송용)
    payload: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)