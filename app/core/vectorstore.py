"""FAISS vector-store manager: create, extend, persist and load."""
import os

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.core.embeddings import get_embeddings
from app.utils.exceptions import VectorStoreError
from app.utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)


class VectorStoreManager:
    def __init__(self, path: str | None = None):
        self.path = path or settings.vectorstore_path
        self._store: FAISS | None = None

    def add(self, chunks: list[Document]) -> int:
        embeddings = get_embeddings()
        if self._store is None and os.path.exists(self.path):
            self.load()
        if self._store is None:
            self._store = FAISS.from_documents(chunks, embeddings)
        else:
            self._store.add_documents(chunks)
        self._store.save_local(self.path)
        logger.info("Indexed %d chunks into %s", len(chunks), self.path)
        return len(chunks)

    def load(self) -> FAISS:
        if not os.path.exists(self.path):
            raise VectorStoreError(
                f"No vector store at '{self.path}' — ingest documents first."
            )
        self._store = FAISS.load_local(
            self.path, get_embeddings(), allow_dangerous_deserialization=True
        )
        return self._store

    def search(self, query: str, k: int | None = None) -> list[Document]:
        store = self._store or self.load()
        return store.similarity_search(query, k=k or settings.top_k)
