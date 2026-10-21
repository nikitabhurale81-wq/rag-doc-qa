"""REST endpoints: /health, /ingest, /ask, /documents."""
import os

from flask import Blueprint, jsonify, request

from app.api.schemas import require_fields
from app.services.ingest_service import IngestService
from app.services.qa_service import QAService
from config.settings import settings

api = Blueprint("api", __name__)
ingest_service = IngestService()
qa_service = QAService()


@api.get("/health")
def health():
    return jsonify(status="ok", model=settings.llm_model)


@api.post("/ingest")
def ingest():
    err = require_fields(request.get_json(silent=True), "file_path")
    if err:
        return jsonify(error=err), 400
    try:
        return jsonify(ingest_service.ingest_file(request.get_json()["file_path"]))
    except Exception as exc:
        return jsonify(error=str(exc)), 500


@api.post("/ask")
def ask():
    err = require_fields(request.get_json(silent=True), "question")
    if err:
        return jsonify(error=err), 400
    try:
        return jsonify(qa_service.answer(request.get_json()["question"]))
    except Exception as exc:
        return jsonify(error=str(exc)), 500


@api.get("/documents")
def documents():
    if not os.path.isdir(settings.data_dir):
        return jsonify(documents=[])
    return jsonify(documents=sorted(os.listdir(settings.data_dir)))
