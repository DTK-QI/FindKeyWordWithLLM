from fastapi import FastAPI, HTTPException
from llama_index import Document, ServiceContext
from llama_index.llms import HuggingFaceLLM
from llama_index.embeddings import HuggingFaceEmbedding
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from app.schemas.search import ReportList
from app.core.config import settings

app = FastAPI(title="Keyword Similarity Search API",
             description="API for finding similar phrases using Llama 3.3 8B and LlamaIndex")

# Initialize global variables
keyword_documents = [Document(text=keyword) for keyword in settings.PREDEFINED_KEYWORDS]

# Initialize Llama model and embeddings
def init_llm():
    model_name = "meta-llama/Llama-2-8b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    llm = HuggingFaceLLM(
        model=model,
        tokenizer=tokenizer,
        context_window=2048,
        max_new_tokens=256
    )
    
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    return service_context

@app.post("/search/")
async def search_reports(reports: ReportList, similarity_threshold: float = 0.7, max_results: int = 10):
    if not keyword_documents:
        raise HTTPException(status_code=400, detail="System not properly initialized")
    
    service_context = init_llm()
    
    # Create a temporary index for the reports
    documents = [Document(text=report.content) for report in reports.reports]
    temp_index = VectorStoreIndex.from_documents(
        documents,
        service_context=service_context
    )
    
    results = []
    for keyword_doc in keyword_documents:
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
    
    return {"results": results}