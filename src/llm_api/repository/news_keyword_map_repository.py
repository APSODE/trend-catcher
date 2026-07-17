from sqlalchemy.orm import Session
from model.news_keyword_map_model import NewsKeywordMapModel

class NewsKeywordMapRepository:
    #새 매핑 추가
    def save(self, session: Session, news_id: int, keyword_id: int) -> None:
        mapping = NewsKeywordMapModel(
            news_id = news_id,
            keyword_id = keyword_id
        )
        session.add(mapping)
        session.flush()
