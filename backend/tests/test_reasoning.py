"""Tests for state classification and reasoning components."""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.models.schemas import (
    EvidenceAnalysisResult, Evidence, Conflict, Citation,
    QueryResponse, Chunk,
)


def test_evidence_analysis_result_supported():
    """EvidenceAnalysisResult can represent a SUPPORTED state."""
    result = EvidenceAnalysisResult(
        state="SUPPORTED",
        relevant_evidence=[
            Evidence(document="test.md", section="1.1", page=None, text="Test text"),
        ],
        reasoning="Evidence directly answers the question.",
    )
    assert result.state == "SUPPORTED"
    assert len(result.relevant_evidence) == 1
    assert result.conflicts is None


def test_evidence_analysis_result_not_found():
    """EvidenceAnalysisResult can represent a NOT_FOUND state."""
    result = EvidenceAnalysisResult(
        state="NOT_FOUND",
        relevant_evidence=[],
        reasoning="No relevant evidence found.",
    )
    assert result.state == "NOT_FOUND"
    assert len(result.relevant_evidence) == 0


def test_evidence_analysis_result_contradiction():
    """EvidenceAnalysisResult can represent a CONTRADICTION state."""
    result = EvidenceAnalysisResult(
        state="CONTRADICTION",
        relevant_evidence=[
            Evidence(document="policy_a.md", section="4.2", page=None,
                     text="Must maintain 75% attendance. No exceptions."),
            Evidence(document="policy_b.md", section="3.1", page=None,
                     text="Medical exemption allows attendance as low as 60%."),
        ],
        reasoning="Two provisions conflict on minimum attendance threshold.",
        conflicts=[
            Conflict(
                evidence_a="Must maintain 75% attendance. No exceptions.",
                citation_a=Citation(id="SRC-001", document="policy_a.md", section="4.2"),
                evidence_b="Medical exemption allows attendance as low as 60%.",
                citation_b=Citation(id="SRC-002", document="policy_b.md", section="3.1"),
                reason="One categorically prohibits exceptions, the other permits one.",
            ),
        ],
    )
    assert result.state == "CONTRADICTION"
    assert len(result.conflicts) == 1
    assert result.conflicts[0].citation_a.document == "policy_a.md"
    assert result.conflicts[0].citation_b.document == "policy_b.md"


def test_query_response_supported():
    """QueryResponse models a complete SUPPORTED API response."""
    response = QueryResponse(
        state="SUPPORTED",
        answer="The minimum attendance is 75%. [SRC-001]",
        evidence=[
            Evidence(document="attendance.md", section="4.2", page=None,
                     text="Students must maintain 75% attendance."),
        ],
        citations=[
            Citation(id="SRC-001", document="attendance.md", section="4.2"),
        ],
    )
    assert response.state == "SUPPORTED"
    assert "75%" in response.answer
    assert len(response.citations) == 1


def test_query_response_not_found():
    """QueryResponse models a complete NOT_FOUND API response."""
    response = QueryResponse(
        state="NOT_FOUND",
        answer="The regulations do not cover this topic.",
        evidence=[],
        citations=[],
    )
    assert response.state == "NOT_FOUND"
    assert len(response.evidence) == 0


def test_invalid_state_rejected():
    """Invalid state values should be rejected by the model."""
    with pytest.raises(Exception):
        EvidenceAnalysisResult(
            state="MAYBE",
            relevant_evidence=[],
            reasoning="Invalid state",
        )


def test_chunk_model():
    """Chunk model stores document metadata."""
    chunk = Chunk(
        chunk_id="test_001",
        text="Test content",
        document="policy.md",
        section="Section 1",
        page=None,
    )
    assert chunk.chunk_id == "test_001"
    assert chunk.document == "policy.md"
    assert chunk.section == "Section 1"
    assert chunk.page is None
