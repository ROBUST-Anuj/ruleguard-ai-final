from typing import List, Tuple
from backend.app.ingestion.indexer import Indexer
from backend.app.models.schemas import Chunk
from backend.app.retrieval.tokenizer import tokenize

class LexicalRetriever:
    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def search(self, query: str, top_k: int = 10) -> List[Tuple[Chunk, float]]:
        if not self.indexer.bm25 or not self.indexer.chunks:
            return []
            
        tokenized_query = tokenize(query)
        scores = self.indexer.bm25.get_scores(tokenized_query)
        
        top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for idx in top_n:
            if scores[idx] > 0:
                results.append((self.indexer.chunks[idx], float(scores[idx])))
                
        return results
