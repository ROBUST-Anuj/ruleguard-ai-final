"""FastAPI routes for RuleGuard API."""
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

# Initialize components
indexer = Indexer(settings.INDEX_DIR)
_index_loaded = indexer.load()

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


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process a question about university regulations."""
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if len(question) > 2000:
        raise HTTPException(status_code=400, detail="Question is too long (max 2000 chars).")

    if not indexer.chunks:
        raise HTTPException(
            status_code=503,
            detail="Index not loaded. Run 'python scripts/ingest.py' first.",
        )

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
    }


@router.get("/sources")
async def sources():
    """List available source documents."""
    if not indexer.chunks:
        return {"documents": []}
    docs = sorted(set(c.document for c in indexer.chunks))
    return {"documents": docs}
