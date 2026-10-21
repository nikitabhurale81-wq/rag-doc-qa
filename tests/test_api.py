"""API smoke tests using Flask's test client (no external services needed)."""
import pytest

from app import create_app


@pytest.fixture()
def client():
    return create_app().test_client()


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_ask_requires_question(client):
    resp = client.post("/ask", json={})
    assert resp.status_code == 400


def test_ingest_requires_file_path(client):
    resp = client.post("/ingest", json={})
    assert resp.status_code == 400


def test_documents_endpoint_returns_list(client):
    resp = client.get("/documents")
    assert resp.status_code == 200
    assert isinstance(resp.get_json()["documents"], list)
