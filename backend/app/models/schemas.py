"""Pydantic models for RuleGuard API."""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any


class Chunk(BaseModel):
    """A chunk of text from a corpus document."""
    chunk_id: str
    text: str
    document: str
    section: Optional[str] = None
    page: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QueryRequest(BaseModel):
    """Incoming query from the user."""
    question: str = Field(..., min_length=1, max_length=2000)


class Evidence(BaseModel):
    """A piece of evidence retrieved from the corpus."""
    document: str
    section: Optional[str] = None
    page: Optional[int] = None
    text: str
    relevance_score: Optional[float] = None


class Citation(BaseModel):
    """A citation reference for an answer."""
    id: str
    document: str
    section: Optional[str] = None
    page: Optional[int] = None


class Conflict(BaseModel):
    """A pair of conflicting provisions."""
    evidence_a: str
    citation_a: Citation
    evidence_b: str
    citation_b: Citation
    reason: str


class EvidenceAnalysisResult(BaseModel):
    """Result of evidence analysis stage."""
    state: Literal["SUPPORTED", "NOT_FOUND", "CONTRADICTION"]
    relevant_evidence: List[Evidence]
    conflicts: Optional[List[Conflict]] = None
    reasoning: str
    answer: Optional[str] = None


class QueryResponse(BaseModel):
    """Full API response to a user query."""
    state: Literal["SUPPORTED", "NOT_FOUND", "CONTRADICTION"]
    answer: str
    evidence: List[Evidence]
    citations: List[Citation]
    conflicts: Optional[List[Conflict]] = None
    query_analysis: Optional[Dict[str, Any]] = None
    reasoning: Optional[str] = None
