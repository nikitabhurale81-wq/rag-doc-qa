"""Ingestion service: file -> chunks -> vector store."""
from app.core.chunking import split_documents
from app.core.vectorstore import VectorStoreManager
from app.loaders.document_loader import load_document
from app.utils.logger import get_logger

logger = get_logger(__name__)


class IngestService:
    def __init__(self, store: VectorStoreManager | None = None):
        self.store = store or VectorStoreManager()

    def ingest_file(self, file_path: str) -> dict:
        documents = load_document(file_path)
        chunks = split_documents(documents)
        self.store.add(chunks)
        logger.info("Ingested %s -> %d chunks", file_path, len(chunks))
        return {"file": file_path, "documents": len(documents), "chunks": len(chunks)}
