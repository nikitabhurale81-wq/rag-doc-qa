"""
Core RAG (Retrieval-Augmented Generation) pipeline.

Loads documents, splits them into chunks, embeds them into a FAISS
vector store and answers questions using retrieved context + an LLM.
"""
import os
from dataclasses import dataclass, field

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

PROMPT = ChatPromptTemplate.from_template(
    """Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}
Answer:"""
)


@dataclass
class RAGPipeline:
    persist_dir: str = "vectorstore"
    chunk_size: int = 800
    chunk_overlap: int = 120
    k: int = 4
    _store: FAISS = field(default=None, repr=False)

    def ingest(self, file_path: str) -> int:
        """Load a PDF/TXT file, chunk it, embed it and store the vectors."""
        loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        chunks = splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings()
        if self._store is None:
            self._store = FAISS.from_documents(chunks, embeddings)
        else:
            self._store.add_documents(chunks)
        self._store.save_local(self.persist_dir)
        return len(chunks)

    def load(self) -> None:
        """Load a previously saved vector store from disk."""
        self._store = FAISS.load_local(
            self.persist_dir, OpenAIEmbeddings(), allow_dangerous_deserialization=True
        )

    def ask(self, question: str) -> str:
        """Retrieve the top-k relevant chunks and answer with an LLM."""
        if self._store is None:
            self.load()
        docs = self._store.similarity_search(question, k=self.k)
        context = "\n\n".join(d.page_content for d in docs)
        llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
        return (PROMPT | llm).invoke({"context": context, "question": question}).content
