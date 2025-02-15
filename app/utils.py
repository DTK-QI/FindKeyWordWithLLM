from fastapi import HTTPException
from app.models import SearchRequest, SearchRequest_remote, SearchResult,SearchRequest_test_prompt
from app.config import model_config
from typing import List
import warnings
import json
import re
import aiohttp
from app.prompts import get_keyword_extraction_prompt
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

    
    
async def search_report_test_prompt(request: SearchRequest_test_prompt) -> List[SearchResult]:

    try:
        response = model_config.generate_response(request.prompt,temperature=request.temperature,top_p=request.top_p)
        
        try:
            # 先找最後一個 code block
            matches = re.findall(r'```(?:json)?\s*(.*?)\s*```', response, re.DOTALL)
            if matches:
                json_content = matches[-1].strip()
            else:
                # 如果沒有 code block，從後面找最後一組 JSON 陣列
                last_close_bracket = response.rfind(']')
                if last_close_bracket != -1:
                    # 從最後一個 ] 往前找對應的 [
                    temp_response = response[:last_close_bracket]
                    last_open_bracket = temp_response.rfind('[')
                    
                    if last_open_bracket != -1:
                        json_content = response[last_open_bracket:last_close_bracket + 1].strip()
                        print(f"從最後面找到的 JSON 字串: {json_content}")
                    else:
                        print("無法找到完整的 JSON 陣列結構")
                        return []
                else:
                    print("無法找到 JSON 結構")
                    return []
            
            results = json.loads(json_content)
            
            if not isinstance(results, list):
                print("回應格式無效 - 預期為列表")
                return []
                
            return results
            
        except json.JSONDecodeError as e:
            print(f"無法解析 JSON 回應: {response}")
            print(f"JSON 解析錯誤: {str(e)}")
            return []
            
    except Exception as e:
        print(f"查詢過程發生錯誤: {str(e)}")
        results = []
    
    return results
    
async def search_report(request: SearchRequest) -> List[SearchResult]:
    report = request.report
    if not report:
        raise HTTPException(status_code=400, detail="Report text is required")
    
    prompt = get_keyword_extraction_prompt(KEYWORDS, report)
    
    try:
        response = model_config.generate_response(prompt)
        
        try:
            print(f"回應: {response}")
            # 先找最後一個 code block
            matches = re.findall(r'```(?:json)?\s*(.*?)\s*```', response, re.DOTALL)
            if matches:
                json_content = matches[-1].strip()
            else:
                # 如果沒有 code block，從後面找最後一組 JSON 陣列
                last_close_bracket = response.rfind(']')
                if last_close_bracket != -1:
                    # 從最後一個 ] 往前找對應的 [
                    temp_response = response[:last_close_bracket]
                    last_open_bracket = temp_response.rfind('[')
                    
                    if last_open_bracket != -1:
                        json_content = response[last_open_bracket:last_close_bracket + 1].strip()
                        print(f"從最後面找到的 JSON 字串: {json_content}")
                    else:
                        print("無法找到完整的 JSON 陣列結構")
                        return []
                else:
                    print("無法找到 JSON 結構")
                    return []
            
            results = json.loads(json_content)
            
            if not isinstance(results, list):
                print("回應格式無效 - 預期為列表")
                return []
                
            return results
            
        except json.JSONDecodeError as e:
            print(f"無法解析 JSON 回應: {response}")
            print(f"JSON 解析錯誤: {str(e)}")
            return []
            
        if not isinstance(results, list):
            print("回應格式無效 - 預期為列表")
            results = []
            
    except Exception as e:
        print(f"查詢過程發生錯誤: {str(e)}")
        results = []
    
    return results

async def search_report_remote(request: SearchRequest_remote) -> List[SearchResult]:
    if not request.report:
        raise HTTPException(status_code=400, detail="Report text is required")
    
    prompt = get_keyword_extraction_prompt(KEYWORDS, request.report)
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": request.model_name,  # 確保與 LM Studio 中的模型名稱相符
                "messages": [
                    {"role": "system", "content": "You are an information extraction system."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": request.temperature,
                # "top_p": request.top_p,
                "max_tokens": request.max_tokens,
                "stream": False  # 設為 True 可獲取逐步回應
}

            
            headers = {
                "Content-Type": "application/json"
            }
            
            async with session.post(
                request.api_url, 
                json=payload, 
                headers=headers
            ) as response:
                if response.status != 200:
                    raise Exception(f"API 呼叫失敗: {response.status}")
                    
                data = await response.json()
                llm_response = data['choices'][0]['message']['content']
                
                print(f"LLM 回應: {llm_response}")
                
                # 使用現有的 JSON 解析邏輯
                matches = re.findall(r'```(?:json)?\s*(.*?)\s*```', llm_response, re.DOTALL)
                if matches:
                    json_content = matches[-1].strip()
                else:
                    last_close_bracket = llm_response.rfind(']')
                    if last_close_bracket != -1:
                        temp_response = llm_response[:last_close_bracket]
                        last_open_bracket = temp_response.rfind('[')
                        
                        if last_open_bracket != -1:
                            json_content = llm_response[last_open_bracket:last_close_bracket + 1].strip()
                        else:
                            return []
                    else:
                        return []
                
                results = json.loads(json_content)
                
                if not isinstance(results, list):
                    return []
                    
                return results
                
    except Exception as e:
        print(f"遠端 LLM 查詢錯誤: {str(e)}")
        return []
