"""Custom exceptions used across the application."""


class DocumentLoadError(Exception):
    """Raised when a document cannot be loaded or parsed."""


class VectorStoreError(Exception):
    """Raised when the vector store is missing or unreadable."""


class EmptyQuestionError(ValueError):
    """Raised when an empty question is submitted."""
