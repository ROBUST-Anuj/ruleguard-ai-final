"""Tests for the API endpoints."""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.models.schemas import QueryRequest


def test_query_request_validation():
    """QueryRequest should validate the question field."""
    req = QueryRequest(question="What is the attendance requirement?")
    assert req.question == "What is the attendance requirement?"


def test_query_request_rejects_empty():
    """QueryRequest should reject empty questions."""
    with pytest.raises(Exception):
        QueryRequest(question="")


def test_query_request_rejects_too_long():
    """QueryRequest should reject questions exceeding max length."""
    with pytest.raises(Exception):
        QueryRequest(question="x" * 2001)


def test_query_request_accepts_max_length():
    """QueryRequest should accept questions at max length."""
    req = QueryRequest(question="x" * 2000)
    assert len(req.question) == 2000
