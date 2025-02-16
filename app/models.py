from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    report: str = "Patient demonstrates local recurrence at the surgical site with evidence of liver metastasis."
    
    class Config:
        schema_extra = {
            "example": {
                "report": """Follow-up examination reveals recurrent adenocarcinoma at the primary site. 
                          PET-CT shows multiple new hepatic lesions consistent with metastatic disease. 
                          Additionally, enlarged para-aortic lymph nodes suggest lymphatic spread."""
            }
        }

class SearchRequest_test_prompt(BaseModel):
    temperature: float = 0.85
    top_p: float = 0.3
    prompt: str = """Analyze the oncology report for signs of cancer recurrence and metastasis. Return results in JSON format.

        Key Patterns to Identify:
        - Local recurrence patterns
        - Metastatic spread (liver, lung, bone)
        - Lymph node involvement
        - Disease progression indicators
        - Treatment response markers

        Report:
        {report_text}

        Respond with:
        [
            {
                "keyword": "identified pattern",
                "matches": "relevant text from report"
            }
        ]

        Example Analysis:
        Input: "Follow-up imaging shows recurrent tumor at surgical site with multiple new hepatic lesions."
        Output: [
            {
                "keyword": "local recurrence",
                "matches": "recurrent tumor at surgical site"
            },
            {
                "keyword": "liver metastasis",
                "matches": "multiple new hepatic lesions"
            }
        ]"""

class SearchResult(BaseModel):
    keyword: str
    matches: str

class SearchRequest_remote(BaseModel):
    report: str
    api_url: str = "http://192.168.0.202:1234/v1/chat/completions"
    model_name: str = "llama-3.3-70b-instruct"
    temperature: float = 0.85
    top_p: float = 0.3
    max_tokens: int = 2000
    
    class Config:
        schema_extra = {
            "example": {
                "report": """Post-treatment evaluation indicates recurrent disease:
                          - Local recurrence at surgical margin
                          - New metastatic foci in liver segments VI and VII
                          - Progressive lymphadenopathy in para-aortic region""",
                "api_url": "http://192.168.0.202:1234/v1/chat/completions",
                "model_name": "llama-3.3-70b-instruct",
                "temperature": 0.85,
                "top_p": 0.3,
                "max_tokens": 2000
            }
        }