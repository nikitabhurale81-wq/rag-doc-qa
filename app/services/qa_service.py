"""Question-answering service: question -> retrieve -> prompt -> LLM."""
from app.core.llm import get_llm
from app.core.prompts import QA_PROMPT
from app.core.retriever import retrieve_context
from app.core.vectorstore import VectorStoreManager
from app.utils.exceptions import EmptyQuestionError


class QAService:
    def __init__(self, store: VectorStoreManager | None = None):
        self.store = store or VectorStoreManager()
        self._chain = None  # built lazily so importing the app needs no API key

    @property
    def chain(self):
        if self._chain is None:
            self._chain = QA_PROMPT | get_llm()
        return self._chain

    def answer(self, question: str) -> dict:
        if not question or not question.strip():
            raise EmptyQuestionError("Question must not be empty.")
        context = retrieve_context(question, self.store)
        result = self.chain.invoke({"context": context, "question": question})
        return {"question": question, "answer": result.content}
