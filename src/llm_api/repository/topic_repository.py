from sqlalchemy.orm import Session
from model.topic_model import TopicModel
from sqlalchemy import select

class TopicRepository:
    #새 주제 추가
    def save(self, session: Session, topic: TopicModel) -> TopicModel:
        session.add(topic)
        session.flush()
        return topic

    #주제 목록 반환
    def get_all(self, session: Session) -> list[TopicModel]:
        query = select(TopicModel)
        return list(session.execute(query).scalars().all())

    #주제 중복도 증가
    def increment_count(self, session: Session, topic_id: int) -> None:
        topic = session.get(TopicModel, topic_id)
        topic.count += 1
        session.flush()