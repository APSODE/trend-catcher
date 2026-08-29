from dataclasses import dataclass, field
from src.llm_api.model.news_analysis_model import NewsAnalysisModel

@dataclass
class AnalysisResultData:
    processed: list[NewsAnalysisModel] = field(default_factory = list)
    skipped: int = 0
    failed: int = 0

    @property
    def total(self) -> int:
        return len(self.processed) + self.skipped + self.failed