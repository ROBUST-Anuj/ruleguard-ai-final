"""Document loader for markdown and PDF files with metadata preservation."""
import os
import re
import fitz  # PyMuPDF
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Document:
    """Represents a loaded document or document page."""
    filename: str
    content: str
    doc_type: str  # 'md' or 'pdf_page'
    metadata: Dict[str, Any] = field(default_factory=dict)


class DocumentLoader:
    """Loads markdown and PDF documents from the data directory."""

    CORPUS_SUBDIRS = ["corpus", "pdf"]  # Only scan these subdirectories

    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_all(self) -> List[Document]:
        """Load all documents from corpus and pdf subdirectories."""
        docs = []
        if not os.path.exists(self.data_dir):
            print(f"Data directory not found: {self.data_dir}")
            return docs

        for subdir in self.CORPUS_SUBDIRS:
            subdir_path = os.path.join(self.data_dir, subdir)
            if not os.path.exists(subdir_path):
                continue
            for root, _, files in os.walk(subdir_path):
                for filename in sorted(files):
                    filepath = os.path.join(root, filename)
                    if filename.endswith('.md'):
                        doc = self._load_markdown(filepath)
                        if doc:
                            docs.append(doc)
                    elif filename.endswith('.pdf'):
                        pdf_docs = self._load_pdf(filepath)
                        docs.extend(pdf_docs)

        print(f"Loaded {len(docs)} document(s) from {self.data_dir}")
        return docs

    def _load_markdown(self, filepath: str) -> Optional[Document]:
        """Load a markdown file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return Document(
                filename=os.path.basename(filepath),
                content=content,
                doc_type='md',
                metadata={"source_path": filepath}
            )
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None

    def _load_pdf(self, filepath: str) -> List[Document]:
        """Load a PDF file, producing one Document per page."""
        docs = []
        filename = os.path.basename(filepath)
        try:
            pdf_doc = fitz.open(filepath)
            for page_num in range(len(pdf_doc)):
                page = pdf_doc.load_page(page_num)
                text = page.get_text()
                if text.strip():
                    docs.append(Document(
                        filename=filename,
                        content=text,
                        doc_type='pdf_page',
                        metadata={
                            "page": page_num + 1,
                            "source_path": filepath,
                        }
                    ))
            pdf_doc.close()
            print(f"  Loaded PDF: {filename} ({len(docs)} pages)")
        except Exception as e:
            print(f"Error loading PDF {filepath}: {e}")
        return docs
