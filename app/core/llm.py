from llama_index import ServiceContext
from llama_index.llms import HuggingFaceLLM
from llama_index.embeddings import HuggingFaceEmbedding
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from app.core.config import settings

def init_llm():
    tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        settings.MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    llm = HuggingFaceLLM(
        model=model,
        tokenizer=tokenizer,
        context_window=2048,
        max_new_tokens=256
    )
    
    embed_model = HuggingFaceEmbedding(model_name=settings.EMBEDDING_MODEL)
    return ServiceContext.from_defaults(llm=llm, embed_model=embed_model)