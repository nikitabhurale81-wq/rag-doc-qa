"""Document loaders — one entry point for every supported file type."""
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from app.utils.exceptions import DocumentLoadError
from app.utils.logger import get_logger

logger = get_logger(__name__)

LOADERS = {".pdf": PyPDFLoader, ".txt": TextLoader, ".md": TextLoader}


def load_document(file_path: str) -> list[Document]:
    ext = os.path.splitext(file_path)[1].lower()
    loader_cls = LOADERS.get(ext)
    if loader_cls is None:
        raise DocumentLoadError(f"Unsupported file type '{ext}': {file_path}")
    logger.info("Loading %s", file_path)
    try:
        return loader_cls(file_path).load()
    except Exception as exc:
        raise DocumentLoadError(f"Failed to load {file_path}: {exc}") from exc
