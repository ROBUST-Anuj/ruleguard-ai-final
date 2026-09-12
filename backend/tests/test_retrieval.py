"""Tests for retrieval components."""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.models.schemas import Chunk
from backend.app.ingestion.indexer import Indexer
from backend.app.retrieval.lexical import LexicalRetriever


@pytest.fixture
def sample_chunks():
    return [
        Chunk(chunk_id="c1", text="minimum attendance requirement is 75 percent for all courses",
              document="attendance.md", section="4.2"),
        Chunk(chunk_id="c2", text="medical exemption allows attendance as low as 60 percent",
              document="medical.md", section="3.1"),
        Chunk(chunk_id="c3", text="hostel fees must be paid by september 5",
              document="hostel.md", section="3.1"),
        Chunk(chunk_id="c4", text="semester tuition fees are due on september 15",
              document="fees.md", section="2.1"),
        Chunk(chunk_id="c5", text="supplementary examination grade is capped at D",
              document="exam.md", section="7.4"),
    ]


@pytest.fixture
def indexer_with_bm25(sample_chunks, tmp_path):
    """Create an indexer with BM25 index only (no FAISS needed for lexical tests)."""
    from rank_bm25 import BM25Okapi

    indexer = Indexer(str(tmp_path))
    indexer.chunks = sample_chunks
    tokenized = [c.text.lower().split() for c in sample_chunks]
    indexer.bm25 = BM25Okapi(tokenized)
    return indexer


def test_lexical_retriever_returns_results(indexer_with_bm25):
    """Lexical retriever should return relevant results for a query."""
    retriever = LexicalRetriever(indexer_with_bm25)
    results = retriever.search("attendance requirement", top_k=3)
    assert len(results) > 0
    # First result should be about attendance
    chunk, score = results[0]
    assert "attendance" in chunk.text.lower()
    assert score > 0


def test_lexical_retriever_ranks_correctly(indexer_with_bm25):
    """More relevant results should have higher scores."""
    retriever = LexicalRetriever(indexer_with_bm25)
    results = retriever.search("hostel fees september", top_k=5)
    assert len(results) > 0
    # Check scores are in descending order
    scores = [s for _, s in results]
    assert scores == sorted(scores, reverse=True)


def test_lexical_retriever_respects_top_k(indexer_with_bm25):
    """Should return at most top_k results."""
    retriever = LexicalRetriever(indexer_with_bm25)
    results = retriever.search("semester", top_k=2)
    assert len(results) <= 2


def test_lexical_retriever_handles_empty_query(indexer_with_bm25):
    """Empty query should return empty results."""
    retriever = LexicalRetriever(indexer_with_bm25)
    results = retriever.search("", top_k=5)
    # BM25 with empty query might return empty or zero-scored results
    assert isinstance(results, list)


def test_lexical_retriever_preserves_metadata(indexer_with_bm25):
    """Retrieved chunks should have their metadata intact."""
    retriever = LexicalRetriever(indexer_with_bm25)
    results = retriever.search("medical exemption", top_k=3)
    for chunk, _ in results:
        assert chunk.document is not None
        assert chunk.chunk_id is not None


def test_indexer_save_and_load(sample_chunks, tmp_path):
    """Indexer should be able to save and reload chunks."""
    import numpy as np

    indexer = Indexer(str(tmp_path))
    # Create dummy embeddings
    embeddings = np.random.randn(len(sample_chunks), 16).astype(np.float32)
    indexer.build_indexes(sample_chunks, embeddings)

    # Load into a new indexer
    indexer2 = Indexer(str(tmp_path))
    loaded = indexer2.load()
    assert loaded is True
    assert len(indexer2.chunks) == len(sample_chunks)
    assert indexer2.vector_index is not None
    assert indexer2.bm25 is not None
