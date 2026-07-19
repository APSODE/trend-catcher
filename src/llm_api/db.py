from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///test.db")  # TODO: 오라클로 교체 필요
SessionLocal = async_sessionmaker(bind=engine)