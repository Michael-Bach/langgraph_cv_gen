from unittest.mock import patch, MagicMock
from apply.nodes.fetch_job import fetch_job


def test_fetch_job_is_callable():
    assert callable(fetch_job)


def test_fetch_job_passthrough_when_no_url():
    state = {"job_url": "", "job_text": "We are hiring.", "revision_count": 0}
    result = fetch_job(state)
    assert result == {"job_text": "We are hiring."}


def test_fetch_job_passthrough_when_url_key_missing():
    state = {"job_text": "Job description here.", "revision_count": 0}
    result = fetch_job(state)
    assert result == {"job_text": "Job description here."}


def test_fetch_job_fetches_and_strips_html():
    state = {"job_url": "https://example.com/job", "revision_count": 0}
    mock_response = MagicMock()
    mock_response.text = (
        "<html><body><p>ML Engineer at Acme.</p>"
        "<script>ga()</script><style>body{}</style></body></html>"
    )
    mock_response.raise_for_status.return_value = None

    with patch("apply.nodes.fetch_job.httpx.get", return_value=mock_response) as mock_get:
        result = fetch_job(state)

    mock_get.assert_called_once()
    assert "job_text" in result
    assert "ML Engineer" in result["job_text"]
    assert "ga()" not in result["job_text"]


def test_fetch_job_falls_back_on_exception():
    state = {"job_url": "https://blocked.com/job", "job_text": "Fallback text", "revision_count": 0}

    with patch("apply.nodes.fetch_job.httpx.get", side_effect=Exception("403 Forbidden")):
        result = fetch_job(state)

    assert result == {"job_text": "Fallback text"}


def test_fetch_job_falls_back_when_raise_for_status_fails():
    state = {"job_url": "https://example.com/job", "job_text": "Fallback", "revision_count": 0}
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("404")

    with patch("apply.nodes.fetch_job.httpx.get", return_value=mock_response):
        result = fetch_job(state)

    assert result == {"job_text": "Fallback"}
