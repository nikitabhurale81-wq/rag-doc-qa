"""Prompt templates used by the QA chain."""
from langchain_core.prompts import ChatPromptTemplate

QA_PROMPT = ChatPromptTemplate.from_template(
    """You are a helpful assistant. Answer the question using ONLY the
context below. If the answer is not present in the context, reply:
"I don't have that information in the provided documents."

Context:
{context}

Question: {question}

Answer:"""
)
