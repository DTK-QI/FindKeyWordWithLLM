import signal
import sys
import torch
import gc
from fastapi import FastAPI, HTTPException, Query
from app.models import SearchRequest, SearchResult, SearchRequest_test_prompt, SearchRequest_remote
from app.utils import search_report, search_report_test_prompt, search_report_remote
from typing import List
import requests

def cleanup_gpu():
    """清理 GPU 記憶體的函數"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()
        print("GPU 記憶體已清理")

def signal_handler(signum, frame):
    """處理程式終止信號"""
    print("\n接收到終止信號，正在清理資源...")
    cleanup_gpu()
    sys.exit(0)

# 註冊信號處理器
signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # 終止信號

app = FastAPI(
    title="Cancer Report Analysis API",
    description="API for analyzing cancer reports using Llama 3.2 3B",
    on_shutdown=[cleanup_gpu]  # 註冊清理函數
)

@app.post("/search/", response_model=List[SearchResult])
async def search(request: SearchRequest):
    return await search_report(request)

@app.post("/search_test_prompt/", response_model=List[SearchResult])
async def search_test_prompt(request: SearchRequest_test_prompt):
    return await search_report_test_prompt(request)

@app.post("/search_remote/", response_model=List[SearchResult])
async def search_remote(request: SearchRequest_remote):
    return await search_report_remote(request)

@app.get("/model/list")
async def get_models(api_url: str = Query(..., description="LM Studio API URL")):
    try:
        # 向LM Studio API發送請求獲取模型列表
        response = requests.get(f"http://{api_url}/v1/models")
        if response.status_code == 200:
            data = response.json()
            # LM Studio API返回的模型列表格式可能需要轉換
            models = [model["id"] for model in data["data"]]
            return {"models": models}
        else:
            # 如果請求失敗，返回空模型
            return {"models": [""]}
    except Exception as e:
        # 如果發生錯誤，返回默認模型並記錄錯誤
        print(f"Error fetching models: {str(e)}")
        return {"models": [""]}

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(app, host="localhost", port=8080)
    finally:
        cleanup_gpu()