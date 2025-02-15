from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    report: str = "This is a sample report text. It mentions liver metastasis and lung metastasis."
    
    class Config:
        schema_extra = {
            "example": {
                "report": "The patient, a 62-year-old male, was diagnosed with bone metastasis originating from colon cancer, as evidenced by PET-CT findings showing increased uptake in the femur and vertebrae."
            }
        }

class SearchResult(BaseModel):
    keyword: str
    matches: str 