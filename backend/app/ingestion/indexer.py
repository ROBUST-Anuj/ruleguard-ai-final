import os
import pickle
import faiss
import numpy as np
from typing import List
from backend.app.models.schemas import Chunk
from rank_bm25 import BM25Okapi

class Indexer:
    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)
        self.vector_index_path = os.path.join(index_dir, "faiss.index")
        self.bm25_index_path = os.path.join(index_dir, "bm25.pkl")
        self.chunks_path = os.path.join(index_dir, "chunks.pkl")
        
        self.vector_index = None
        self.bm25 = None
        self.chunks: List[Chunk] = []

    def build_indexes(self, chunks: List[Chunk], embeddings: np.ndarray):
        self.chunks = chunks
        if len(chunks) == 0:
            return
            
        dimension = embeddings.shape[1]
        self.vector_index = faiss.IndexFlatL2(dimension)
        faiss.normalize_L2(embeddings)
        self.vector_index.add(embeddings)
        
        tokenized_corpus = [chunk.text.lower().split() for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
        self.save()

    def save(self):
        if self.vector_index is not None:
            faiss.write_index(self.vector_index, self.vector_index_path)
        if self.bm25 is not None:
            with open(self.bm25_index_path, 'wb') as f:
                pickle.dump(self.bm25, f)
        if self.chunks:
            with open(self.chunks_path, 'wb') as f:
                pickle.dump(self.chunks, f)

    def load(self):
        if os.path.exists(self.vector_index_path):
            self.vector_index = faiss.read_index(self.vector_index_path)
        if os.path.exists(self.bm25_index_path):
            with open(self.bm25_index_path, 'rb') as f:
                self.bm25 = pickle.load(f)
        if os.path.exists(self.chunks_path):
            with open(self.chunks_path, 'rb') as f:
                self.chunks = pickle.load(f)
        
        return self.vector_index is not None and self.bm25 is not None
