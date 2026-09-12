"""Tests for the document chunker."""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.ingestion.document_loader import Document
from backend.app.ingestion.chunker import Chunker


@pytest.fixture
def chunker():
    return Chunker(max_chunk_words=100, overlap_words=10)


@pytest.fixture
def sample_md_doc():
    return Document(
        filename="test_policy.md",
        content="""# Test Policy

## 1. Introduction

This is the introduction to the test policy. It contains enough words to form a meaningful chunk that the chunker should handle properly.

## 2. Requirements

2.1. Students must maintain a minimum attendance of 75% in each course.

2.2. Late submissions will be penalized at 5% per day.

## 3. Exceptions

3.1. Medical exemptions may be granted for documented illness.
""",
        doc_type='md',
    )


@pytest.fixture
def sample_pdf_doc():
    return Document(
        filename="test_handbook.pdf",
        content="This is page content from a PDF.\n\nIt has multiple paragraphs.\n\nEach paragraph should be preserved.",
        doc_type='pdf_page',
        metadata={"page": 3},
    )


def test_chunk_markdown_produces_chunks(chunker, sample_md_doc):
    """Chunker should produce non-empty chunks from markdown."""
    chunks = chunker.chunk_documents([sample_md_doc])
    assert len(chunks) > 0


def test_chunk_preserves_document_name(chunker, sample_md_doc):
    """All chunks should retain the source document filename."""
    chunks = chunker.chunk_documents([sample_md_doc])
    for chunk in chunks:
        assert chunk.document == "test_policy.md"


def test_chunk_preserves_sections(chunker, sample_md_doc):
    """Chunks should have section headings from the markdown."""
    chunks = chunker.chunk_documents([sample_md_doc])
    sections = [c.section for c in chunks if c.section]
    assert len(sections) > 0
    # Should capture at least some of the headings
    section_texts = set(sections)
    assert any("Introduction" in s or "Requirements" in s or "Exceptions" in s
               for s in section_texts)


def test_chunk_ids_are_unique(chunker, sample_md_doc):
    """Each chunk should have a unique ID."""
    chunks = chunker.chunk_documents([sample_md_doc])
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))


def test_chunk_ids_are_deterministic(chunker, sample_md_doc):
    """Chunking the same document twice should produce the same IDs."""
    chunks1 = chunker.chunk_documents([sample_md_doc])
    chunks2 = chunker.chunk_documents([sample_md_doc])
    ids1 = [c.chunk_id for c in chunks1]
    ids2 = [c.chunk_id for c in chunks2]
    assert ids1 == ids2


def test_chunk_pdf_preserves_page(chunker, sample_pdf_doc):
    """PDF chunks should retain the page number."""
    chunks = chunker.chunk_documents([sample_pdf_doc])
    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk.page == 3
        assert chunk.document == "test_handbook.pdf"


def test_empty_document_produces_no_chunks(chunker):
    """An empty document should produce no chunks."""
    doc = Document(filename="empty.md", content="", doc_type='md')
    chunks = chunker.chunk_documents([doc])
    assert len(chunks) == 0


def test_chunk_text_not_empty(chunker, sample_md_doc):
    """No chunk should have empty text."""
    chunks = chunker.chunk_documents([sample_md_doc])
    for chunk in chunks:
        assert chunk.text.strip() != ""
