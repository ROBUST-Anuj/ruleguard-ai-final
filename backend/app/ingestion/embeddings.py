from typing import List
from openai import OpenAI
from backend.app.config import settings
import numpy as np

class EmbeddingsProvider:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )
        self.model = settings.EMBEDDING_MODEL

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        texts = [text.replace("\n", " ") for text in texts]
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            response = self.client.embeddings.create(input=batch, model=self.model)
            embeddings = [data.embedding for data in response.data]
            all_embeddings.extend(embeddings)
            
        return np.array(all_embeddings, dtype=np.float32)
    
    def get_embedding(self, text: str) -> np.ndarray:
        return self.get_embeddings([text])[0]
