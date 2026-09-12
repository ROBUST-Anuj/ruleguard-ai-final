import os
import pickle
import numpy as np
from typing import List, Optional, Tuple
from backend.app.models.schemas import Chunk
from rank_bm25 import BM25Okapi
from backend.app.retrieval.tokenizer import tokenize

try:
    import faiss
    FAISS_AVAILABLE = True
except (ImportError, Exception):
    faiss = None
    FAISS_AVAILABLE = False


class NumpyVectorIndex:
    """Fallback vector index using NumPy cosine similarity when FAISS is unavailable."""

    def __init__(self, embeddings: np.ndarray):
        self.embeddings = np.array(embeddings, dtype=np.float32)
        # Normalize vectors for cosine similarity
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.embeddings = self.embeddings / norms

    def search(self, query_embedding: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
        q = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        q_norm = np.linalg.norm(q)
        if q_norm > 0:
            q = q / q_norm

        # Cosine similarity is dot product of normalized vectors
        cos_sim = np.dot(self.embeddings, q.T).flatten()
        # FlatL2 distance for normalized vectors: ||u - v||^2 = 2 - 2 * cos_sim
        distances = np.maximum(0.0, 2.0 - 2.0 * cos_sim)

        # Get top-k nearest (smallest distance / highest similarity)
        k_val = min(k, len(self.embeddings))
        indices = np.argsort(distances)[:k_val]
        sorted_distances = distances[indices]

        return np.array([sorted_distances]), np.array([indices])


class Indexer:
    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)
        self.vector_index_path = os.path.join(index_dir, "faiss.index")
        self.embeddings_path = os.path.join(index_dir, "embeddings.npy")
        self.bm25_index_path = os.path.join(index_dir, "bm25.pkl")
        self.chunks_path = os.path.join(index_dir, "chunks.pkl")

        self.vector_index = None
        self.embeddings: Optional[np.ndarray] = None
        self.bm25 = None
        self.chunks: List[Chunk] = []

    def build_indexes(self, chunks: List[Chunk], embeddings: np.ndarray):
        self.chunks = chunks
        if len(chunks) == 0:
            return

        self.embeddings = np.array(embeddings, dtype=np.float32)

        if FAISS_AVAILABLE and faiss is not None:
            dimension = self.embeddings.shape[1]
            self.vector_index = faiss.IndexFlatL2(dimension)
            emb_copy = self.embeddings.copy()
            faiss.normalize_L2(emb_copy)
            self.vector_index.add(emb_copy)
        else:
            self.vector_index = NumpyVectorIndex(self.embeddings)

        tokenized_corpus = [tokenize(chunk.text) for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)

        self.save()

    def save(self):
        try:
            if self.vector_index is not None and FAISS_AVAILABLE and faiss is not None:
                faiss.write_index(self.vector_index, self.vector_index_path)
            if self.embeddings is not None:
                np.save(self.embeddings_path, self.embeddings)
            if self.bm25 is not None:
                with open(self.bm25_index_path, "wb") as f:
                    pickle.dump(self.bm25, f)
            if self.chunks:
                with open(self.chunks_path, "wb") as f:
                    pickle.dump(self.chunks, f)
        except (OSError, IOError):
            # Read-only filesystems (e.g. serverless environments) - in-memory index remains active
            pass

    def load(self) -> bool:
        loaded_vector = False

        if FAISS_AVAILABLE and faiss is not None and os.path.exists(self.vector_index_path):
            try:
                self.vector_index = faiss.read_index(self.vector_index_path)
                loaded_vector = True
            except Exception:
                loaded_vector = False

        if not loaded_vector and os.path.exists(self.embeddings_path):
            try:
                self.embeddings = np.load(self.embeddings_path)
                self.vector_index = NumpyVectorIndex(self.embeddings)
                loaded_vector = True
            except Exception:
                loaded_vector = False

        if os.path.exists(self.bm25_index_path):
            try:
                with open(self.bm25_index_path, "rb") as f:
                    self.bm25 = pickle.load(f)
            except Exception:
                self.bm25 = None

        if os.path.exists(self.chunks_path):
            try:
                with open(self.chunks_path, "rb") as f:
                    self.chunks = pickle.load(f)
            except Exception:
                self.chunks = []

        return self.vector_index is not None and self.bm25 is not None and len(self.chunks) > 0
