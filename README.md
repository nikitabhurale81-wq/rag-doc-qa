# RAG Document Q&A Assistant

A Retrieval-Augmented Generation (RAG) application that lets you chat with your own documents. Upload PDFs or text files, and the system indexes them into a vector store and answers questions using only the retrieved content — reducing hallucinations and keeping answers grounded in your data.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Flask](https://img.shields.io/badge/Flask-API-green) ![LangChain](https://img.shields.io/badge/LangChain-RAG-orange) ![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-purple)

## Features

- 📄 **Multi-format ingestion** — index PDF and TXT documents in one call
- ✂️ **Smart chunking** — recursive character splitting with configurable size/overlap
- 🔍 **Semantic search** — OpenAI embeddings + FAISS similarity retrieval (top-k)
- 💬 **Grounded answers** — the LLM answers strictly from retrieved context and says "I don't know" when the answer isn't in the document
- 🌐 **REST API** — simple Flask endpoints for ingest, ask, and health checks
- ✅ **Tested** — unit tests for chunking behaviour included

## How It Works

```
Document ──► Loader ──► Text Splitter ──► Embeddings ──► FAISS Vector Store
                                                              │
Question ─────────────────────────────────────► Retriever ────┤
                                                              ▼
                                          Prompt + Context ──► LLM ──► Answer
```

## Tech Stack

| Layer      | Tools                                   |
| ---------- | --------------------------------------- |
| Language   | Python 3.10+                            |
| Framework  | Flask                                   |
| LLM / RAG  | LangChain, OpenAI (GPT-4o-mini)         |
| Embeddings | OpenAI Embeddings                       |
| Vector DB  | FAISS                                   |
| Testing    | pytest                                  |

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/rag-doc-qa.git
cd rag-doc-qa

# 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure your API key
cp .env.example .env             # then add your OPENAI_API_KEY
```

## Usage

**Index documents** (place files in `data/`, then run):

```bash
python ingest.py
```

**Start the API server:**

```bash
python app.py
```

**Ask questions:**

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG and how does it reduce hallucinations?"}'
```

```json
{ "answer": "RAG combines a retriever with a language model..." }
```

**API endpoints**

| Method | Endpoint  | Body / Response                                  |
| ------ | --------- | ------------------------------------------------ |
| GET    | `/health` | `{"status": "ok"}`                               |
| POST   | `/ingest` | `{"file_path": "data/doc.pdf"}` → chunk count   |
| POST   | `/ask`    | `{"question": "..."}` → `{"answer": "..."}`      |

## Project Structure

```
rag-doc-qa/
├── app.py               # Flask REST API
├── rag_pipeline.py      # Core RAG pipeline (ingest + retrieval + QA)
├── ingest.py            # CLI to index all documents in ./data
├── requirements.txt
├── .env.example
├── data/
│   └── sample.txt       # Sample document to try out
└── tests/
    └── test_pipeline.py # Unit tests for chunking
```

## Running Tests

```bash
pytest
```

## Future Improvements

- [ ] Support for DOCX and web-page ingestion
- [ ] Streamlit chat UI
- [ ] Swap FAISS with a persistent vector DB (Chroma / Pinecone)
- [ ] Conversation memory for follow-up questions

## Author

**Nikita B** — Python Developer | AI/ML Engineer
Focused on Python, Machine Learning, Generative AI and building practical LLM-powered applications.
