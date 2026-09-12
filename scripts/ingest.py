import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.config import settings
from backend.app.ingestion.document_loader import DocumentLoader
from backend.app.ingestion.chunker import Chunker
from backend.app.ingestion.embeddings import EmbeddingsProvider
from backend.app.ingestion.indexer import Indexer

def main():
    print("Starting ingestion pipeline...")
    
    loader = DocumentLoader(settings.DATA_DIR)
    docs = loader.load_all()
    print(f"Loaded {len(docs)} documents.")
    
    if not docs:
        print("No documents found to ingest.")
        return

    chunker = Chunker()
    chunks = chunker.chunk_documents(docs)
    print(f"Created {len(chunks)} chunks.")
    
    embeddings_provider = EmbeddingsProvider()
    print("Generating embeddings...")
    embeddings = embeddings_provider.get_embeddings([c.text for c in chunks])
    print(f"Generated {embeddings.shape[0]} embeddings.")
    
    indexer = Indexer(settings.INDEX_DIR)
    print("Building indexes...")
    indexer.build_indexes(chunks, embeddings)
    print(f"Indexes built and saved to {settings.INDEX_DIR}.")
    print("Ingestion complete!")

if __name__ == "__main__":
    main()
