"""Tests for document chunking."""
from langchain_core.documents import Document

from app.core.chunking import split_documents


def test_long_document_is_split_into_multiple_chunks():
    chunks = split_documents([Document(page_content="word " * 500)])
    assert len(chunks) > 1
    assert all("chunk_id" in c.metadata for c in chunks)


def test_short_document_stays_one_chunk():
    chunks = split_documents([Document(page_content="Short text.")])
    assert len(chunks) == 1
