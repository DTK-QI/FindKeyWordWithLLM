from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    report: str = "This is a sample report text. It mentions colon metastasis."
    
    class Config:
        schema_extra = {
            "example": {
                "report": "The patient, a 62-year-old male, was diagnosed with bone metastasis originating from colon cancer, as evidenced by PET-CT findings showing increased uptake in the femur and vertebrae."
            }
        }

class SearchRequest_test_prompt(BaseModel):
    temperature : float = 0.85
    top_p : float = 0.3
    prompt: str = """Analyze the report for specified keywords and extract relevant sentences. Return results in JSON format.

        Keywords:
        - Colon cancer with bone metastasis, liver metastasis, lung metastasis, liver and lung metastases, peritoneal tumor seeding, Consider local recurrent tumor involving left seminal vesicle and rectum, Consider residual/recurrent tumor at the rectal region abutting the seminal vesicle, Consider residual/recurrent tumor with peri-rectal invasion, Enlarged change in size of the peritoneal seeding tumor, Favor recurrent rectal cancer, Favoring metastasis from colon cecum cancer, Metastatic adenocarcinoma of colon origin, Metastatic carcinoma of colonic origin, Metastatic carcinoma of colorectal origin, Metastatic lymphadenopathies in the pericolonic region, Rectal cancer adenocarcinoma with liver metastasis, Rectal mucinous adenocarcinoma, Rectosigmoid colon adenocarcinoma, Recurrent colon cancer, Sigmoid colon cancer with recurrence, Recurrent rectal cancer, Suspect recurrent tumor

        Report:
        - This is a sample report text. It mentions liver metastasis and lung metastasis.

        Respond with:

        [
            {
                "keyword": "keyword",
                "matches": "matches"
            },
            ...
        ]

        Exclude keywords with no matches.

        Example:

        **Input:**
        - Keywords: `["bone metastasis", "liver metastasis", "colon cancer"]`
        - Report: `"The patient, a 62-year-old male, was diagnosed with bone metastasis originating from colon cancer. PET-CT confirmed liver metastasis."`

        **Output:**
        ```json
        [
            {
                "keyword": "bone metastasis",
                "matches": "The patient, a 62-year-old male, was diagnosed with bone metastasis originating from colon cancer."
            },
            {
                "keyword": "liver metastasis",
                "matches": "PET-CT confirmed liver metastasis."
            }
        ]
        ```"""
    
class SearchResult(BaseModel):
    keyword: str
    matches: str

class SearchRequest_remote(BaseModel):
    report: str
    api_url: str = "http://192.168.0.202:1234/v1/chat/completions"
    model_name: str = "llama-3.3-70b-instruct"  # 新增模型名稱
    temperature: float = 0.85
    top_p: float = 0.3
    max_tokens: int = 2000      # 新增最大 token 數
    
    class Config:
        schema_extra = {
            "example": {
                "report": "The patient shows signs of liver metastasis.",
                "api_url": "http://192.168.0.202:1234/v1/chat/completions",
                "model_name": "llama-3.3-70b-instruct",  # 範例模型名稱
                "temperature": 0.85,
                "top_p": 0.3,
                "max_tokens": 2000
            }
        }