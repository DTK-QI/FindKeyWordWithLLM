import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import ServiceContext
from llama_index.llms import HuggingFaceLLM
import warnings

warnings.filterwarnings('ignore')

class ModelConfig:
    def __init__(self):
        self.model_name = "meta-llama/Llama-3.2-3b"
        self.tokenizer = None
        self.model = None
        self.llm = None
        self.service_context = None
        self.initialize_model()
    
    def initialize_model(self):
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        if self.model is None:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                pad_token_id=self.tokenizer.eos_token_id
            )
            
        if self.llm is None:
            self.llm = HuggingFaceLLM(
                model=self.model,
                tokenizer=self.tokenizer,
                context_window=2048,
                max_new_tokens=256
            )
            
        if self.service_context is None:
            embed_model = HuggingFaceEmbedding(
                model_name="sentence-transformers/all-mpnet-base-v2"
            )
            self.service_context = ServiceContext.from_defaults(
                llm=self.llm,
                embed_model=embed_model
            )
    
    def get_service_context(self):
        return self.service_context

# Create a singleton instance
model_config = ModelConfig()