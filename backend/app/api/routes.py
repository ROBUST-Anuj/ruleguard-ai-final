"""FastAPI routes for RuleGuard API."""
import os
from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import QueryRequest, QueryResponse
from backend.app.config import settings
from backend.app.ingestion.indexer import Indexer
from backend.app.ingestion.embeddings import EmbeddingsProvider
from backend.app.retrieval.semantic import SemanticRetriever
from backend.app.retrieval.lexical import LexicalRetriever
from backend.app.retrieval.hybrid import HybridRetriever
from backend.app.reasoning.evidence_analyzer import EvidenceAnalyzer
from backend.app.reasoning.answer_generator import AnswerGenerator
from backend.app.reasoning.pipeline import ReasoningPipeline
from backend.app.citations.validator import CitationValidator

router = APIRouter()

# Resolve data and index directories relative to project root
def _resolve_path(rel_path: str) -> str:
    if os.path.isabs(rel_path):
        return rel_path
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    return os.path.join(base_dir, rel_path)

index_dir = _resolve_path(settings.INDEX_DIR)
data_dir = _resolve_path(settings.DATA_DIR)

# Initialize components
indexer = Indexer(index_dir)
indexer.load()

embeddings = EmbeddingsProvider()
semantic_retriever = SemanticRetriever(indexer, embeddings)
lexical_retriever = LexicalRetriever(indexer)
hybrid_retriever = HybridRetriever(semantic_retriever, lexical_retriever)

evidence_analyzer = EvidenceAnalyzer()
answer_generator = AnswerGenerator()
citation_validator = CitationValidator()
pipeline = ReasoningPipeline(
    hybrid_retriever, evidence_analyzer, answer_generator, citation_validator
)


def ensure_index_loaded():
    """Ensure chunks and indexes are loaded, attempting automatic on-demand ingestion if needed."""
    if indexer.chunks and (indexer.vector_index is not None or indexer.bm25 is not None):
        return True

    # Try loading from disk
    if indexer.load():
        return True

    # Ingest from data directory if available
    try:
        from backend.app.ingestion.document_loader import DocumentLoader
        from backend.app.ingestion.chunker import Chunker

        if os.path.exists(data_dir):
            loader = DocumentLoader(data_dir)
            docs = loader.load_all()
            if docs:
                chunker = Chunker()
                chunks = chunker.chunk_documents(docs)

                # If LLM_API_KEY is available, compute embeddings
                if settings.LLM_API_KEY and settings.LLM_API_KEY != "sk-placeholder":
                    embs = embeddings.get_embeddings([c.text for c in chunks])
                    indexer.build_indexes(chunks, embs)
                else:
                    from rank_bm25 import BM25Okapi
                    indexer.chunks = chunks
                    tokenized = [c.text.lower().split() for c in chunks]
                    indexer.bm25 = BM25Okapi(tokenized)
                return True
    except Exception as e:
        print(f"Index initialization notice: {e}")

    return bool(indexer.chunks)


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process a question about university regulations."""
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if len(question) > 2000:
        raise HTTPException(status_code=400, detail="Question is too long (max 2000 chars).")

    if not indexer.chunks:
        ensure_index_loaded()

    if not indexer.chunks:
        raise HTTPException(
            status_code=503,
            detail="Index not loaded. Please configure LLM_API_KEY in environment or run 'python scripts/ingest.py' first.",
        )

    # If vector index is not yet built but API key is present, build it once
    if indexer.vector_index is None and settings.LLM_API_KEY and settings.LLM_API_KEY != "sk-placeholder":
        try:
            embs = embeddings.get_embeddings([c.text for c in indexer.chunks])
            indexer.build_indexes(indexer.chunks, embs)
        except Exception as e:
            print(f"Vector index build notice: {e}")

    try:
        response = pipeline.process(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "index_loaded": bool(indexer.chunks),
        "num_chunks": len(indexer.chunks) if indexer.chunks else 0,
        "has_vector_index": indexer.vector_index is not None,
        "has_bm25": indexer.bm25 is not None,
    }


@router.get("/sources")
async def sources():
    """List available source documents."""
    if not indexer.chunks:
        ensure_index_loaded()
    if not indexer.chunks:
        return {"documents": []}
    docs = sorted(set(c.document for c in indexer.chunks))
    return {"documents": docs}
