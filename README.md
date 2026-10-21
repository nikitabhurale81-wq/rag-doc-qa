# RAG Document Q&A Assistant

A production-structured **Retrieval-Augmented Generation (RAG)** application that lets you chat with your own documents. Documents are chunked, embedded and indexed into a FAISS vector store; questions are answered by an LLM using **only** the retrieved context — keeping answers grounded and reducing hallucinations.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Flask](https://img.shields.io/badge/Flask-REST%20API-green) ![LangChain](https://img.shields.io/badge/LangChain-RAG-orange) ![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-purple) ![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## Features

- 📄 **Multi-format ingestion** — PDF, TXT and Markdown through a single loader layer
- ✂️ **Configurable chunking** — recursive splitting, size/overlap driven by env config
- 🔍 **Semantic retrieval** — OpenAI embeddings + FAISS top-k similarity search with source tracing
- 💬 **Grounded answers** — strict prompt: answer from context or admit you don't know
- 🧩 **Clean layered architecture** — API → Services → Core → Loaders, fully decoupled
- 🌐 **REST API + Web UI** — Flask endpoints plus a lightweight chat frontend
- 🐳 **Docker support** — Dockerfile and docker-compose included
- ✅ **Tested** — pytest suite covering chunking, loaders and API behaviour

## Architecture

```
            ┌────────────┐      ┌──────────────┐      ┌─────────────────┐
Documents ─►│  Loaders   │─────►│   Chunking   │─────►│   Embeddings    │
            └────────────┘      └──────────────┘      └────────┬────────┘
                                                             ▼
Question ─► API ─► QA Service ─► Retriever ─► FAISS Vector Store
                              │
                              ▼
                     Prompt + Context ─► LLM ─► Answer
```

## Tech Stack

| Layer      | Tools                              |
| ---------- | ---------------------------------- |
| Language   | Python 3.10+                       |
| API        | Flask (Blueprints, app factory)    |
| LLM / RAG  | LangChain, OpenAI GPT-4o-mini      |
| Embeddings | OpenAI `text-embedding-3-small`    |
| Vector DB  | FAISS                              |
| Config     | python-dotenv, dataclass settings  |
| Testing    | pytest                             |
| DevOps     | Docker, docker-compose             |

## Project Structure

```
rag-doc-qa/
├── run.py                    # Entry point
├── config/
│   └── settings.py           # Env-based central configuration
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── api/
│   │   ├── routes.py         # /health, /ingest, /ask, /documents
│   │   └── schemas.py        # Request validation
│   ├── core/
│   │   ├── chunking.py       # Text splitting
│   │   ├── embeddings.py     # Embedding model factory
│   │   ├── llm.py            # LLM client factory
│   │   ├── vectorstore.py    # FAISS store manager
│   │   ├── retriever.py      # Context retrieval + formatting
│   │   └── prompts.py        # Prompt templates
│   ├── services/
│   │   ├── ingest_service.py # Ingestion pipeline
│   │   └── qa_service.py     # Question answering
│   ├── loaders/
│   │   └── document_loader.py
│   └── utils/
│       ├── logger.py
│       └── exceptions.py
├── frontend/
│   └── index.html            # Minimal chat UI
├── scripts/
│   └── ingest_data.py        # CLI bulk ingestion
├── data/
│   └── sample.txt
├── tests/
│   ├── test_chunking.py
│   ├── test_loaders.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Getting Started

```bash
git clone https://github.com/<your-username>/rag-doc-qa.git
cd rag-doc-qa

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # add your OPENAI_API_KEY
```

**With Docker:**

```bash
docker compose up --build
```

## Usage

```bash
# 1. Index documents placed in ./data
python -m scripts.ingest_data

# 2. Start the API
python run.py

# 3. Ask a question
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

**API reference**

| Method | Endpoint     | Description                          |
| ------ | ------------ | ------------------------------------ |
| GET    | `/health`    | Service status + active model        |
| POST   | `/ingest`    | Index a file: `{"file_path": "..."}` |
| POST   | `/ask`       | Ask a question: `{"question": "..."}`|
| GET    | `/documents` | List files available in `data/`      |

Open `frontend/index.html` in a browser for the chat UI (API must be running).

## Running Tests

```bash
pytest -v
# tests/test_chunking.py, tests/test_loaders.py, tests/test_api.py
```

## Configuration

All settings live in `config/settings.py` and can be overridden via `.env`:

| Variable           | Default                  | Purpose                    |
| ------------------ | ------------------------ | -------------------------- |
| `OPENAI_API_KEY`   | —                        | OpenAI API key             |
| `OPENAI_MODEL`     | `gpt-4o-mini`            | Chat model                 |
| `EMBEDDING_MODEL`  | `text-embedding-3-small` | Embedding model            |
| `CHUNK_SIZE`       | `800`                    | Chunk size (characters)    |
| `CHUNK_OVERLAP`    | `120`                    | Chunk overlap              |
| `TOP_K`            | `4`                      | Chunks retrieved per query |

## Future Improvements

- [ ] DOCX / web-page ingestion
- [ ] Streaming answers + conversation memory
- [ ] Persistent vector DB (Chroma / Pinecone)
- [ ] JWT auth and rate limiting on the API

## Author

**Nikita B** — Python Developer | AI/ML Engineer
Focused on Python, Machine Learning, Generative AI and building practical LLM-powered applications.
