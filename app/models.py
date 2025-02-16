from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    report: str = "Sample text for pattern matching and analysis."
    
    class Config:
        schema_extra = {
            "example": {
                "report": """This is a sample text that demonstrates the analysis capabilities. 
                          The system will identify important patterns and key findings based on 
                          the predefined criteria."""
            }
        }

class SearchRequest_test_prompt(BaseModel):
    temperature: float = 0.85
    top_p: float = 0.3
    prompt: str = """Analyze the text for key patterns and findings. Return results in JSON format.

        Key Elements to Identify:
        - Main patterns
        - Important findings
        - Key indicators
        - Significant changes
        - Notable elements

        Text:
        {report_text}

        Respond with:
        [
            {
                "keyword": "identified pattern",
                "matches": "relevant text from input"
            }
        ]

        Example Analysis:
        Input: "The analysis reveals significant changes in the observed patterns."
        Output: [
            {
                "keyword": "pattern change",
                "matches": "significant changes in the observed patterns"
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
                "report": """Analysis results show:
                          - Primary findings in target area
                          - New developments in observed regions
                          - Progressive changes in key indicators""",
                "api_url": "http://192.168.0.202:1234/v1/chat/completions",
                "model_name": "llama-3.3-70b-instruct",
                "temperature": 0.85,
                "top_p": 0.3,
                "max_tokens": 2000
            }
        }