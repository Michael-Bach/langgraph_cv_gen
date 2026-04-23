import pytest
from apply.nodes.fetch_job import fetch_job


def test_fetch_job_is_callable():
    assert callable(fetch_job)


def test_fetch_job_raises_not_implemented():
    state = {"job_url": "https://example.com/job", "revision_count": 0}
    with pytest.raises(NotImplementedError):
        fetch_job(state)


def test_fetch_job_with_pasted_text_raises_not_implemented():
    state = {"job_url": "", "job_text": "We are hiring a ML engineer.", "revision_count": 0}
    with pytest.raises(NotImplementedError):
        fetch_job(state)
