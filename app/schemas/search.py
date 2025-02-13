from pydantic import BaseModel
from typing import List, Optional

class SimilarityMatch(BaseModel):
    text: str
    similarity_score: float

class SearchResultSchema(BaseModel):
    keyword: str
    matches: List[SimilarityMatch]

class SearchResponse(BaseModel):
    results: List[SearchResultSchema]

class Report(BaseModel):
    content: str

class ReportList(BaseModel):
    reports: List[Report]