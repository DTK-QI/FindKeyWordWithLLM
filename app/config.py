import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import warnings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore')

class ModelConfig:
    def __init__(self):
        self.model_name = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
        self.tokenizer = None
        self.model = None
        self.initialize_model()
    
    def initialize_model(self):
        try:
            if self.tokenizer is None:
                logger.info(f"正在載入 tokenizer: {self.model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    trust_remote_code=True
                )
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            if self.model is None:
                logger.info(f"正在載入模型: {self.model_name}")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    device_map="auto",
                    pad_token_id=self.tokenizer.eos_token_id,
                    trust_remote_code=True
                )
                logger.info("模型載入完成")
        except Exception as e:
            logger.error(f"模型初始化錯誤: {str(e)}")
            raise

    def generate_response(self, prompt: str, max_length: int = 256) -> str:
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            inputs = inputs.to(self.model.device)
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            logger.error(f"生成回應時發生錯誤: {str(e)}")
            raise
# Create a singleton instance
model_config = ModelConfig()