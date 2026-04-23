import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def mock_graph():
    with patch("apply.api.graph") as m:
        yield m


@pytest.fixture
def client(mock_graph):
    from apply.api import app
    return TestClient(app), mock_graph


def test_post_apply_with_url_returns_thread_id(client):
    tc, mock_graph = client
    mock_graph.invoke.return_value = {}
    mock_graph.get_state.return_value.values = {
        "fit_score": 72.0,
        "fit_breakdown": {"verdict": "Good Fit"},
    }
    response = tc.post("/apply", json={"job_url": "https://example.com/job"})
    assert response.status_code == 200
    data = response.json()
    assert "thread_id" in data
    assert data["status"] == "awaiting_approval"
    assert data["fit_score"] == 72.0


def test_post_apply_with_text_returns_thread_id(client):
    tc, mock_graph = client
    mock_graph.invoke.return_value = {}
    mock_graph.get_state.return_value.values = {
        "fit_score": 55.0,
        "fit_breakdown": {},
    }
    response = tc.post("/apply", json={"job_text": "We are hiring..."})
    assert response.status_code == 200
    assert "thread_id" in response.json()


def test_post_apply_missing_input_returns_422(client):
    tc, _ = client
    response = tc.post("/apply", json={})
    assert response.status_code == 422


def test_post_resume_approved_returns_complete(client):
    tc, mock_graph = client
    mock_graph.invoke.return_value = {}
    mock_graph.get_state.return_value.values = {
        "cv_pdf_path": "outputs/acme_ml_cv.pdf",
        "cover_letter_pdf_path": "outputs/acme_ml_cover.pdf",
    }
    response = tc.post("/apply/test-thread-123/resume", json={"approved": True})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "complete"
    assert data["thread_id"] == "test-thread-123"


def test_post_resume_rejected_returns_aborted(client):
    tc, mock_graph = client
    mock_graph.invoke.return_value = {}
    response = tc.post("/apply/test-thread-123/resume", json={"approved": False})
    assert response.status_code == 200
    assert response.json()["status"] == "aborted"


def test_get_result_returns_state(client):
    tc, mock_graph = client
    mock_graph.get_state.return_value.values = {
        "fit_score": 80.0,
        "cv_pdf_path": "outputs/acme_cv.pdf",
    }
    response = tc.get("/apply/test-thread-123/result")
    assert response.status_code == 200
    data = response.json()
    assert "state" in data
    assert data["thread_id"] == "test-thread-123"


def test_get_result_thread_not_found(client):
    tc, mock_graph = client
    mock_graph.get_state.return_value = None
    response = tc.get("/apply/nonexistent-thread/result")
    assert response.status_code == 404
