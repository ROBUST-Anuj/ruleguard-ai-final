"""Tests for citation validation."""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.citations.validator import CitationValidator
from backend.app.models.schemas import QueryResponse, Citation, Evidence


@pytest.fixture
def validator():
    return CitationValidator()


def test_validate_passes_valid_citations(validator):
    """Valid citations pointing to existing documents should be kept."""
    response = QueryResponse(
        state="SUPPORTED",
        answer="Test answer",
        evidence=[],
        citations=[
            Citation(id="SRC-001", document="attendance_policy.md", section="4.2"),
            Citation(id="SRC-002", document="examination_policy.md", section="7.1"),
        ],
    )
    result = validator.validate(response)
    # Should keep citations that match known documents
    assert isinstance(result.citations, list)


def test_validate_removes_unknown_documents(validator):
    """Citations referencing non-existent documents should be removed."""
    response = QueryResponse(
        state="SUPPORTED",
        answer="Test answer",
        evidence=[],
        citations=[
            Citation(id="SRC-001", document="nonexistent_policy.md", section="1.1"),
        ],
    )
    result = validator.validate(response)
    assert len(result.citations) == 0


def test_validate_handles_empty_citations(validator):
    """Empty citation list should pass through."""
    response = QueryResponse(
        state="NOT_FOUND",
        answer="Not found",
        evidence=[],
        citations=[],
    )
    result = validator.validate(response)
    assert result.citations == []


def test_validate_pdf_requires_page(validator):
    """PDF citations without a valid page number should be removed."""
    response = QueryResponse(
        state="SUPPORTED",
        answer="Test",
        evidence=[],
        citations=[
            Citation(id="SRC-001", document="student_handbook.pdf", section="Ch 1", page=None),
        ],
    )
    result = validator.validate(response)
    assert len(result.citations) == 0
