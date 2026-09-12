import re
from typing import List

def tokenize(text: str) -> List[str]:
    """Tokenize and stem text for BM25 retrieval."""
    if not text:
        return []
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    stemmed = []
    for w in words:
        for suffix in ('ing', 'tion', 'tions', 'ed', 'es', 's'):
            if len(w) > 4 and w.endswith(suffix):
                w = w[:-len(suffix)]
                break
        stemmed.append(w)
    return stemmed
