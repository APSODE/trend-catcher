import asyncio
import logging

from abc import ABC, abstractmethod

from src.crawler_api.event.event_types import DomainEvent


logger = logging.getLogger(__name__)

class EventObserver(ABC):
    @abstractmethod
    async def on_event(self, event: DomainEvent) -> None:
        pass

class LoggingObserver(EventObserver):

    async def on_event(self, event: DomainEvent):
        logger.info(
            "모델=%s 이벤트=%s id=%s 시간=%s",
            event.entity,
            event.event_type.value,
            event.entity_id,
            event.occurred_at.isoformat()
        )

class EventPublisher:
    def __init__(self):
        self._observers: list[EventObserver] = []

    def subscribe(self, observer: EventObserver):
        self._observers.append(observer)

    def unsubscribe(self, observer: EventObserver):
        self._observers.remove(observer)

    async def publish(self, event: DomainEvent) -> None:

        results = await asyncio.gather(
            *[observer.on_event(event) for observer in self._observers],
            return_exceptions=True
        )

        for observer, result in zip(self._observers, results):
            if isinstance(result, Exception):
                logger.exception(
                    "observer 실패=%s",
                    observer.__class__.__name__,
                    exc_info=result
                )

event_publisher = EventPublisher()
