from pydantic import BaseModel, Field

class HashtagSearchRequestData(BaseModel):
    hashtags: list[str] = Field(min_length = 1)