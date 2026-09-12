"""Full reasoning pipeline: retrieval → analysis → answer generation → validation."""
from backend.app.models.schemas import QueryRequest, QueryResponse
from backend.app.retrieval.hybrid import HybridRetriever
from backend.app.reasoning.evidence_analyzer import EvidenceAnalyzer
from backend.app.reasoning.answer_generator import AnswerGenerator
from backend.app.citations.validator import CitationValidator
from backend.app.config import settings


class ReasoningPipeline:
    """Orchestrates the full query processing pipeline."""

    def __init__(
        self,
        retriever: HybridRetriever,
        analyzer: EvidenceAnalyzer,
        generator: AnswerGenerator,
        validator: CitationValidator,
    ):
        self.retriever = retriever
        self.analyzer = analyzer
        self.generator = generator
        self.validator = validator

    def process(self, request: QueryRequest) -> QueryResponse:
        """
        Full pipeline:
        question → hybrid retrieval → evidence analysis
        → answer generation → citation validation → response
        """
        # 1. Retrieve relevant chunks
        chunks = self.retriever.search(request.question, top_k=settings.TOP_K)

        # 2. Analyze evidence (determine state)
        analysis = self.analyzer.analyze(request.question, chunks)

        # 3. Generate grounded answer
        response = self.generator.generate(request.question, analysis)

        # 4. Validate citations
        response = self.validator.validate(response)

        return response
