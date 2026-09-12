"""Citation validator: ensures all citations map to real documents."""
import os
from backend.app.models.schemas import QueryResponse, Citation
from backend.app.config import settings


class CitationValidator:
    """Validates that citations reference real documents and sections."""

    def __init__(self):
        self._known_documents: set[str] | None = None

    def _load_known_documents(self) -> set[str]:
        """Scan data directory for known document filenames."""
        if self._known_documents is not None:
            return self._known_documents

        known: set[str] = set()
        for subdir in ("corpus", "pdf"):
            path = os.path.join(settings.DATA_DIR, subdir)
            if os.path.exists(path):
                for f in os.listdir(path):
                    if f.endswith(('.md', '.pdf')):
                        known.add(f)
        self._known_documents = known
        return known

    def validate(self, response: QueryResponse) -> QueryResponse:
        """Validate and filter citations in the response."""
        if not response.citations:
            return response

        known = self._load_known_documents()
        valid_citations: list[Citation] = []

        for cite in response.citations:
            # Check document exists
            if cite.document not in known:
                continue

            # For PDF sources, require a valid page number
            if cite.document.endswith('.pdf') and (cite.page is None or cite.page < 1):
                continue

            valid_citations.append(cite)

        response.citations = valid_citations
        return response
