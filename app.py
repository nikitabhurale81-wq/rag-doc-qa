"""Flask API around the RAG pipeline.

Endpoints:
  POST /ingest   {"file_path": "data/doc.pdf"}  -> {"chunks_indexed": n}
  POST /ask      {"question": "..."}            -> {"answer": "..."}
  GET  /health                                  -> {"status": "ok"}
"""
from flask import Flask, jsonify, request

from rag_pipeline import RAGPipeline

app = Flask(__name__)
pipeline = RAGPipeline()


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/ingest")
def ingest():
    path = (request.get_json() or {}).get("file_path")
    if not path:
        return jsonify(error="file_path is required"), 400
    try:
        n = pipeline.ingest(path)
    except Exception as exc:  # surface loader/embedding errors to the caller
        return jsonify(error=str(exc)), 500
    return jsonify(chunks_indexed=n)


@app.post("/ask")
def ask():
    question = (request.get_json() or {}).get("question")
    if not question:
        return jsonify(error="question is required"), 400
    return jsonify(answer=pipeline.ask(question))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
