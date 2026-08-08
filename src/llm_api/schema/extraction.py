from pydantic import BaseModel, Field, field_validator

class ExtractionResultData(BaseModel):
    keywords: list[str] = Field(max_length = 5) #키워드는 최대 5개
    topic: str = Field(max_length = 90) #주제 길이는 최대 90자
    content_score: float = Field(ge = 0.0, le = 1.0)  # 자체점수는 0~1 범위만

    @field_validator("keywords") #keywords는 자동으로 여기 빨려들어가서 빈 문자 날리는 작업을 거침
    @classmethod
    def clean_keywords(cls, value: list[str]) -> list[str]:
        return [word.strip() for word in value if word.strip()]