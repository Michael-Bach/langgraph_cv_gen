import pytest
from apply.nodes.evaluate_fit import evaluate_fit


def test_evaluate_fit_is_callable():
    assert callable(evaluate_fit)


def test_evaluate_fit_raises_not_implemented():
    state = {
        "job_parsed": {
            "company": "Acme",
            "role": "ML Engineer",
            "location": "Copenhagen",
            "language": "en",
            "requirements": ["Python", "PyTorch"],
            "nice_to_have": [],
            "raw_text": "We are hiring...",
        },
        "revision_count": 0,
    }
    with pytest.raises(NotImplementedError):
        evaluate_fit(state)
