from fastapi import HTTPException
from app.models import SearchRequest, SearchResult
from app.config import model_config
from typing import List
import warnings
import json
warnings.filterwarnings('ignore')

# Predefined keywords for cancer report analysis
KEYWORDS = [
    "Colon cancer with bone metastasis", "liver metastasis", "lung metastasis", 
    "liver and lung metastases", "peritoneal tumor seeding",
    "Consider local recurrent tumor involving left seminal vesicle and rectum", 
    "Consider residual/recurrent tumor at the rectal region abutting the seminal vesicle",
    "Consider residual/recurrent tumor with peri-rectal invasion", 
    "Enlarged change in size of the peritoneal seeding tumor",
    "Favor recurrent rectal cancer", "Favoring metastasis from colon cecum cancer",
    "Metastatic adenocarcinoma of colon origin",
    "Metastatic carcinoma of colonic origin",
    "Metastatic carcinoma of colorectal origin",
    "Metastatic lymphadenopathies in the pericolonic region",
    "Rectal cancer adenocarcinoma with liver metastasis",
    "Rectal mucinous adenocarcinoma",
    "Rectosigmoid colon adenocarcinoma",
    "Recurrent colon cancer",
    "Sigmoid colon cancer with recurrence",
    "Recurrent rectal cancer",
    "Suspect recurrent tumor"
]

async def search_report(request: SearchRequest) -> List[SearchResult]:
    report = request.report
    if not report:
        raise HTTPException(status_code=400, detail="Report text is required")
    
    
    prompt = f"""
        Analyze the following report for the presence of the specified keywords. For each keyword, identify and return the sentences in the report where the keyword or its related context appears. The response format should prioritize the sentences from the report.

        Keywords:
        - {", ".join(KEYWORDS)}

        Report:
        - {report}

        Please respond with the following JSON structure:

        [{{"keyword": "keyword", "matches": "matches"}}, ...]

        If a keyword does not appear in the report, do not include it in the output.

        - "keyword": The keyword being analyzed (may differ slightly from the exact keyword in the report).
        - "matches": A list of sentences from the report that contain or are relevant to the keyword.
        - If a keyword has no matches, it should be excluded from the response.

        ### Example:

        **Input:**
        - Keywords: `["bone metastasis", "liver metastasis", "colon cancer"]`
        - Report: `"The patient, a 62-year-old male, was diagnosed with bone metastasis originating from colon cancer. PET-CT confirmed liver metastasis. No other significant findings were noted in the report."`

        **Output (Expected):**
        ```json
        [
            {{
                "keyword": "bone metastasis",
                "matches": "The patient, a 62-year-old male, was diagnosed with bone metastasis originating from colon cancer."
            }},
            {{
                "keyword": "liver metastasis",
                "matches": "PET-CT confirmed liver metastasis."
            }}
        ]
        ```
        """

    try:
        response = model_config.generate_response(prompt)
        
        try:
            start_index = response.find('```json')
            if start_index != -1:
                start_index = response.find('[', start_index)
                end_index = response.rfind(']')
                if start_index != -1 and end_index != -1:
                    json_str = response[start_index:end_index + 1].strip()
                    print(f"提取的 JSON 字串: {json_str}")
                    results = json.loads(json_str)
                else:
                    print("無法找到 JSON 結構")
                    results = []
        except json.JSONDecodeError as e:
            print(f"無法解析 JSON 回應: {response}")
            print(f"JSON 解析錯誤: {str(e)}")
            results = []
            
        if not isinstance(results, list):
            print("回應格式無效 - 預期為列表")
            results = []
            
    except Exception as e:
        print(f"查詢過程發生錯誤: {str(e)}")
        results = []
    
    return results