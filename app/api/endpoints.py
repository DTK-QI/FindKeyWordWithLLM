from fastapi import APIRouter, HTTPException
from app.services.search_service import SearchService
from app.schemas.search import SearchResponse, ReportList
from app.core.config import settings

router = APIRouter()
search_service = SearchService()

@router.get("/keywords/")
async def get_keywords():
    """獲取當前系統中預設的關鍵詞列表"""
    return {"keywords": settings.PREDEFINED_KEYWORDS}

@router.post("/search/", response_model=SearchResponse)
async def search_reports(reports: ReportList, similarity_threshold: float = 0.7, max_results: int = 10):
    results = search_service.search_reports(
        reports=reports.reports,
        similarity_threshold=similarity_threshold,
        max_results=max_results
    )
    
    if not results:
        raise HTTPException(status_code=400, detail="No matching results found")
    
    return {"results": results}