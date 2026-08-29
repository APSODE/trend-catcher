from dataclasses import dataclass

@dataclass
class HashtagPrepareResultData:
    prepared: int = 0
    failed: int = 0

    @property
    def total(self) -> int:
        return self.prepared + self.failed