from datetime import datetime
from src.llm_api.util.datetime_util import DateTimeUtil
import logging

logger = logging.getLogger(__name__)

class SearchCache:
    def __init__(self):
        self._result: dict[str, list[str]] = {}
        self._saved_at: datetime | None = None

    def save(self, result: dict[str, list[str]]) -> None:
        self._result = result
        self._saved_at = DateTimeUtil.get_now_kst()

    def get(self, since: datetime) -> dict[str, list[str]]:
        if self._saved_at is None:
            logger.info("저장된 결과 없음")
            return {}
        if self._saved_at < since:
            logger.info("결과 최신화되지 않음(%s)", self._saved_at)
            return {}
        return self._result