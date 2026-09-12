from typing import List, Tuple
from backend.app.models.schemas import Chunk
from backend.app.retrieval.semantic import SemanticRetriever
from backend.app.retrieval.lexical import LexicalRetriever
from backend.app.config import settings

class HybridRetriever:
    def __init__(self, semantic: SemanticRetriever, lexical: LexicalRetriever):
        self.semantic = semantic
        self.lexical = lexical
        self.semantic_weight = settings.SEMANTIC_WEIGHT
        self.lexical_weight = settings.LEXICAL_WEIGHT

    def search(self, query: str, top_k: int = 10) -> List[Chunk]:
        semantic_results = self.semantic.search(query, top_k=top_k*2)
        lexical_results = self.lexical.search(query, top_k=top_k*2)
        
        chunk_scores = {}
        
        if lexical_results:
            max_lex = max(score for _, score in lexical_results)
            min_lex = min(score for _, score in lexical_results)
            lex_range = max_lex - min_lex if max_lex > min_lex else 1.0
        else:
            max_lex, min_lex, lex_range = 1.0, 0.0, 1.0

        for chunk, score in semantic_results:
            chunk_scores[chunk.chunk_id] = {
                'chunk': chunk,
                'sem_score': score,
                'lex_score': 0.0
            }
            
        for chunk, score in lexical_results:
            norm_score = (score - min_lex) / lex_range if lex_range > 0 else 0
            if chunk.chunk_id in chunk_scores:
                chunk_scores[chunk.chunk_id]['lex_score'] = norm_score
            else:
                chunk_scores[chunk.chunk_id] = {
                    'chunk': chunk,
                    'sem_score': 0.0,
                    'lex_score': norm_score
                }
                
        final_results = []
        for v in chunk_scores.values():
            hybrid_score = (self.semantic_weight * v['sem_score']) + (self.lexical_weight * v['lex_score'])
            final_results.append((v['chunk'], hybrid_score))
            
        final_results.sort(key=lambda x: x[1], reverse=True)
        return [chunk for chunk, score in final_results[:top_k]]
