from fastapi import HTTPException
from llama_index import VectorStoreIndex, Document
from app.models import SearchRequest, SearchResult
from app.config import model_config
from typing import List
import warnings
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
    
    service_context = model_config.get_service_context()
    sentences = report.split('.')
    results = []
    
    for keyword in KEYWORDS:
        matches = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if keyword.lower() in sentence.lower():
                matches.append(sentence)
            else:
                query_engine = VectorStoreIndex.from_documents(
                    [Document(text=sentence)], 
                    service_context=service_context
                ).as_query_engine()
                response = query_engine.query(keyword)
                if response.source_nodes and response.source_nodes[0].score > 0.5:
                    matches.append(sentence)
        
        if matches:
            results.append(SearchResult(
                keyword=keyword,
                matches=matches
            ))
    
    return results