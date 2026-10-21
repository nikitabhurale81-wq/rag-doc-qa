"""Retrieval logic — fetches relevant chunks and formats them as context."""
from app.core.vectorstore import VectorStoreManager


def retrieve_context(question: str, store: VectorStoreManager) -> str:
    docs = store.search(question)
    return "\n\n".join(
        f"[{d.metadata.get('source', 'doc')} | chunk {d.metadata.get('chunk_id', '?')}]\n"
        f"{d.page_content}"
        for d in docs
    )
