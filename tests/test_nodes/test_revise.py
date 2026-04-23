import pytest
from apply.nodes.revise import revise


def test_revise_is_callable():
    assert callable(revise)


def test_revise_raises_not_implemented():
    state = {
        "cv_latex": r"\documentclass{moderncv}...",
        "cover_letter_latex": r"\documentclass{cover}...",
        "review_critique": {
            "missed_keywords": ["Kubernetes"],
            "company_angles": [],
            "reframing_suggestions": [],
            "tone_issues": [],
            "checklist": [],
            "quality_score": 0.6,
            "needs_revision": True,
        },
        "revision_count": 0,
    }
    with pytest.raises(NotImplementedError):
        revise(state)
