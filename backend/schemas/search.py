from pydantic import BaseModel
from typing import List


class SearchRequest(BaseModel):
    image_data: str  # Base64 encoded PNG


class MatchResult(BaseModel):
    photo_url: str
    confidence: float
    animal_type: str
    photographer: str


class SearchResponse(BaseModel):
    matches: List[MatchResult]
    search_time_ms: int
