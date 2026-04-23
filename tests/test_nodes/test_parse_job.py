import pytest
from apply.nodes.parse_job import parse_job


def test_parse_job_is_callable():
    assert callable(parse_job)


def test_parse_job_raises_not_implemented():
    state = {
        "job_text": "We are hiring an ML Engineer at Acme in Copenhagen.",
        "revision_count": 0,
    }
    with pytest.raises(NotImplementedError):
        parse_job(state)
