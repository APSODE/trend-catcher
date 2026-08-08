from src.llm_api.core.settings import get_settings
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

settings = get_settings()

#엔진
engine: AsyncEngine = create_async_engine(
    settings.database_url.get_secret_value(),
    echo = settings.db_echo,
    pool_pre_ping = True #연결이 죽은지 감지, 자동 연결
)

#세션팩토리
SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind = engine, #엔진연결
    class_ = AsyncSession, #비동기화
    expire_on_commit = False #커밋하면서 증발히는거 방지
)

#세션 동작부
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        try:
            yield session #일 하라고 보내놓고 대기
            await session.commit() #문제없이 돌아왔으면 커밋
        except Exception: #문제발생했으면
            await session.rollback() #일단 flush들 롤백시키고
            raise #핸들러에게 상황 보고 처리해달라 위임