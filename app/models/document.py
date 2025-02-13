from llama_index import Document
from typing import List, Optional

class KeywordCollection:
    def __init__(self):
        self.documents: List[Document] = []

    def add_keywords(self, keywords: List[str]):
        self.documents = [Document(text=keyword) for keyword in keywords]

    def get_documents(self) -> List[Document]:
        return self.documents

class SearchResult:
    def __init__(self, keyword: str, matches: List[dict]):
        self.keyword = keyword
        self.matches = matches