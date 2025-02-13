from llama_index import VectorStoreIndex, Document
from app.core.llm import init_llm
from app.models.document import KeywordCollection
from app.core.config import settings
from app.schemas.search import Report, ReportList
from typing import List, Dict, Any

class SearchService:
    def __init__(self):
        self.keyword_collection = KeywordCollection()
        self.service_context = init_llm()
        # 初始化時直接載入預定義的關鍵詞
        self.store_keywords(settings.PREDEFINED_KEYWORDS)

    def store_keywords(self, keywords: List[str]) -> int:
        self.keyword_collection.add_keywords(keywords)
        return len(self.keyword_collection.get_documents())

    def search_reports(
        self,
        reports: List[Report],
        similarity_threshold: float = settings.DEFAULT_SIMILARITY_THRESHOLD,
        max_results: int = settings.DEFAULT_MAX_RESULTS
    ) -> List[Dict[str, Any]]:
        if not self.keyword_collection.get_documents():
            return []

        # 創建報告的臨時索引
        documents = [Document(text=report.content) for report in reports]
        temp_index = VectorStoreIndex.from_documents(
            documents,
            service_context=self.service_context
        )

        results = []
        for keyword_doc in self.keyword_collection.get_documents():
            query_engine = temp_index.as_query_engine()
            response = query_engine.query(keyword_doc.text)
            
            similarity_results = []
            for node in response.source_nodes:
                if node.score >= similarity_threshold:
                    similarity_results.append({
                        "text": node.node.text,
                        "similarity_score": node.score
                    })
            
            if similarity_results:
                results.append({
                    "keyword": keyword_doc.text,
                    "matches": sorted(
                        similarity_results,
                        key=lambda x: x["similarity_score"],
                        reverse=True
                    )[:max_results]
                })
        
        return results