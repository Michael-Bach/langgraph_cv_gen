import pytest
from apply.nodes.review import review


def test_review_is_callable():
    assert callable(review)


def test_review_raises_not_implemented():
    state = {
        "job_parsed": {"company": "Acme", "role": "ML Engineer", "raw_text": "...",
                       "language": "en", "requirements": [], "nice_to_have": [],
                       "location": "CPH", "department": None},
        "cv_latex": r"\documentclass{moderncv}...",
        "cover_letter_latex": r"\documentclass{cover}...",
        "revision_count": 0,
    }
    with pytest.raises(NotImplementedError):
        review(state)
