from pydantic import BaseModel, Field, field_validator

class HashtagExpansionData(BaseModel):
    aliases: list[str] = Field(max_length = 10) #동의어 (한은 = 한국은행 등)
    children: list[str] = Field(max_length = 10)  # 하위 개체 (인천 - 송도 등)

    @field_validator("aliases", "children")  #빈 문자 날리는 작업
    @classmethod
    def clean_list(cls, value: list[str]) -> list[str]:
        return [word.strip() for word in value if word.strip()]