import numpy as np
from typing import List, Tuple
from backend.app.ingestion.indexer import Indexer
from backend.app.ingestion.embeddings import EmbeddingsProvider
from backend.app.models.schemas import Chunk

try:
    import faiss
    FAISS_AVAILABLE = True
except (ImportError, Exception):
    faiss = None
    FAISS_AVAILABLE = False


class SemanticRetriever:
    def __init__(self, indexer: Indexer, embeddings_provider: EmbeddingsProvider):
        self.indexer = indexer
        self.embeddings_provider = embeddings_provider

    def search(self, query: str, top_k: int = 10) -> List[Tuple[Chunk, float]]:
        if not self.indexer.vector_index or not self.indexer.chunks:
            return []

        try:
            query_embedding = self.embeddings_provider.get_embedding(query)
            query_embedding = np.array([query_embedding], dtype=np.float32)

            if FAISS_AVAILABLE and faiss is not None:
                faiss.normalize_L2(query_embedding)
            else:
                norm = np.linalg.norm(query_embedding)
                if norm > 0:
                    query_embedding = query_embedding / norm

            k = min(top_k, len(self.indexer.chunks))
            distances, indices = self.indexer.vector_index.search(query_embedding, k)

            results = []
            for i, idx in enumerate(indices[0]):
                if idx != -1 and idx < len(self.indexer.chunks):
                    sim = 1.0 - (distances[0][i] / 2.0)
                    results.append((self.indexer.chunks[idx], float(sim)))

            return results
        except Exception:
            # Fallback when embeddings provider is unavailable or provider lacks embeddings endpoint (e.g. Groq)
            return []
