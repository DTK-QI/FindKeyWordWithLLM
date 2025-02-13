from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Keyword Similarity Search API"
    PROJECT_DESCRIPTION: str = "API for finding similar phrases using Llama 3.3 8B and LlamaIndex"
    MODEL_NAME: str = "meta-llama/Llama-2-8b"
    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
    DEFAULT_SIMILARITY_THRESHOLD: float = 0.7
    DEFAULT_MAX_RESULTS: int = 10
    
    # 預定義的關鍵詞列表
    PREDEFINED_KEYWORDS: list[str] = [
        "肺腺癌",
        "肺鱗狀細胞癌",
        "小細胞肺癌",
        "胸腔積液",
        "淋巴結腫大",
        "轉移",
        "復發"
    ]

settings = Settings()