"""LLM client factory."""
from langchain_openai import ChatOpenAI

from config.settings import settings


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model=settings.llm_model, temperature=0)
