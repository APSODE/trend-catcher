from sqlalchemy.ext.asyncio import AsyncSession
from model.keyword_model import KeywordModel
from sqlalchemy import select

class KeywordRepository:
    #키워드 있으면 그거, 없으면 추가 후 반환
    async def get_or_create(self, session: AsyncSession, target_keyword: str) -> KeywordModel:
        query = select(KeywordModel).where(KeywordModel.keyword == target_keyword)
        result = await session.execute(query)
        target = result.scalar_one_or_none()
        if target is not None: #있으면 바로 리턴
            return target
        else: #없으면 추가 후 리턴
            keyword = KeywordModel(
                keyword = target_keyword,
                embedding = None #TODO: 임베딩기능 구현 후 적용 필요
            )
            session.add(keyword)
            await session.flush()
            return keyword

    #키워드 목록 반환
    async def get_all(self, session: AsyncSession) -> list[KeywordModel]:
        result = await session.execute(select(KeywordModel))
        return list(result.scalars().all())
