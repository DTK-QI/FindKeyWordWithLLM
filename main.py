import signal
import sys
import torch
import gc
from fastapi import FastAPI, HTTPException
from app.models import SearchRequest, SearchResult
from app.utils import search_report
from typing import List

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

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(app, host="localhost", port=8080)
    finally:
        cleanup_gpu()