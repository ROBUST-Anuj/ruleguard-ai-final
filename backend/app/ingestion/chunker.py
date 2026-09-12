"""Structure-aware document chunker with metadata preservation."""
import re
import hashlib
from typing import List, Optional
from backend.app.models.schemas import Chunk
from backend.app.ingestion.document_loader import Document


class Chunker:
    """Splits documents into chunks preserving structure and metadata."""

    def __init__(self, max_chunk_words: int = 300, overlap_words: int = 30):
        self.max_chunk_words = max_chunk_words
        self.overlap_words = overlap_words

    def chunk_documents(self, documents: List[Document]) -> List[Chunk]:
        all_chunks = []
        for doc in documents:
            if doc.doc_type == 'md':
                all_chunks.extend(self._chunk_markdown(doc))
            elif doc.doc_type == 'pdf_page':
                all_chunks.extend(self._chunk_pdf_page(doc))
        print(f"Created {len(all_chunks)} chunks from {len(documents)} document(s)")
        return all_chunks

    def _chunk_markdown(self, doc: Document) -> List[Chunk]:
        """Split markdown by heading-delimited sections."""
        chunks = []
        lines = doc.content.split('\n')

        # Parse into sections based on headings
        sections: list[tuple[str | None, list[str]]] = []
        current_section: Optional[str] = None
        current_lines: list[str] = []

        for line in lines:
            heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
            if heading_match:
                # Save previous section
                if current_lines:
                    sections.append((current_section, current_lines))
                current_section = heading_match.group(2).strip()
                current_lines = [line]
            else:
                current_lines.append(line)

        # Don't forget the last section
        if current_lines:
            sections.append((current_section, current_lines))

        # Create chunks from each section
        for section_name, section_lines in sections:
            section_text = '\n'.join(section_lines).strip()
            if not section_text:
                continue

            words = section_text.split()
            if len(words) <= self.max_chunk_words:
                # Section fits in one chunk
                chunk_id = self._make_chunk_id(doc.filename, section_name, 0)
                chunks.append(Chunk(
                    chunk_id=chunk_id,
                    text=section_text,
                    document=doc.filename,
                    section=section_name,
                    page=None,
                ))
            else:
                # Split large sections into overlapping chunks
                start = 0
                part = 0
                while start < len(words):
                    end = min(start + self.max_chunk_words, len(words))
                    chunk_text = ' '.join(words[start:end])
                    chunk_id = self._make_chunk_id(doc.filename, section_name, part)
                    chunks.append(Chunk(
                        chunk_id=chunk_id,
                        text=chunk_text,
                        document=doc.filename,
                        section=section_name,
                        page=None,
                    ))
                    start = end - self.overlap_words if end < len(words) else end
                    part += 1

        return chunks

    def _chunk_pdf_page(self, doc: Document) -> List[Chunk]:
        """Split a single PDF page into paragraph-based chunks."""
        chunks = []
        page_num = doc.metadata.get('page', 1)
        text = doc.content.strip()
        if not text:
            return chunks

        # Try to detect section headings in PDF text
        section_name = self._detect_pdf_section(text)

        # Split by double newlines (paragraphs)
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

        current_text_parts: list[str] = []
        current_word_count = 0
        part = 0

        for para in paragraphs:
            para_words = len(para.split())
            if current_word_count + para_words > self.max_chunk_words and current_text_parts:
                chunk_text = '\n\n'.join(current_text_parts)
                chunk_id = self._make_chunk_id(doc.filename, f"page_{page_num}", part)
                chunks.append(Chunk(
                    chunk_id=chunk_id,
                    text=chunk_text,
                    document=doc.filename,
                    section=section_name,
                    page=page_num,
                ))
                current_text_parts = [para]
                current_word_count = para_words
                part += 1
            else:
                current_text_parts.append(para)
                current_word_count += para_words

        if current_text_parts:
            chunk_text = '\n\n'.join(current_text_parts)
            chunk_id = self._make_chunk_id(doc.filename, f"page_{page_num}", part)
            chunks.append(Chunk(
                chunk_id=chunk_id,
                text=chunk_text,
                document=doc.filename,
                section=section_name,
                page=page_num,
            ))

        return chunks

    def _detect_pdf_section(self, text: str) -> Optional[str]:
        """Try to detect the main section heading from PDF page text."""
        lines = text.strip().split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            # Look for numbered section headers or short capitalized lines
            if re.match(r'^\d+\.', line) and len(line) < 80:
                return line
            if line.isupper() and len(line) < 60:
                return line
        return None

    def _make_chunk_id(self, filename: str, section: Optional[str], part: int) -> str:
        """Create a deterministic chunk ID."""
        base = filename.replace('.md', '').replace('.pdf', '')
        section_slug = re.sub(r'[^a-z0-9]+', '_', (section or 'none').lower()).strip('_')
        raw_id = f"{base}_{section_slug}_{part}"
        # Keep it short but unique
        short_hash = hashlib.md5(raw_id.encode()).hexdigest()[:6]
        return f"{base}_{section_slug}_{part}_{short_hash}"
