import pytest
from apply.nodes.draft import draft_cv, draft_cover_letter


def test_draft_cv_is_callable():
    assert callable(draft_cv)


def test_draft_cover_letter_is_callable():
    assert callable(draft_cover_letter)


def test_draft_cv_raises_not_implemented():
    state = {
        "job_parsed": {"company": "Acme", "role": "ML Engineer", "language": "en",
                       "requirements": ["Python"], "nice_to_have": [], "location": "CPH",
                       "raw_text": "...", "department": None},
        "revision_count": 0,
    }
    with pytest.raises(NotImplementedError):
        draft_cv(state)


def test_draft_cover_letter_raises_not_implemented():
    state = {
        "job_parsed": {"company": "Acme", "role": "ML Engineer", "language": "en",
                       "requirements": ["Python"], "nice_to_have": [], "location": "CPH",
                       "raw_text": "...", "department": None},
        "revision_count": 0,
    }
    with pytest.raises(NotImplementedError):
        draft_cover_letter(state)
