"""
Oracle 비동기 엔진/세션 설정.
python-oracledb 의 async 드라이버를 SQLAlchemy 2.0 async 로 사용한다.
"""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from ..config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.db_url,
    echo=settings.db_echo,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """모든 ORM 모델의 base."""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 의존성으로 주입되는 세션. 요청 단위로 열고 닫는다."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise