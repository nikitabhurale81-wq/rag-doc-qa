"""Embedding model factory."""
from langchain_openai import OpenAIEmbeddings

from config.settings import settings


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=settings.embedding_model)
