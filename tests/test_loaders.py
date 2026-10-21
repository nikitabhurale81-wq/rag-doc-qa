"""Tests for the document loader dispatch."""
import pytest

from app.loaders.document_loader import load_document
from app.utils.exceptions import DocumentLoadError


def test_unsupported_extension_raises():
    with pytest.raises(DocumentLoadError):
        load_document("archive.zip")


def test_sample_text_loads(tmp_path):
    f = tmp_path / "note.txt"
    f.write_text("Hello RAG", encoding="utf-8")
    docs = load_document(str(f))
    assert docs and "Hello RAG" in docs[0].page_content
