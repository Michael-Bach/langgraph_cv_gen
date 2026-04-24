# tests/test_nodes/test_revise.py
from unittest.mock import patch, MagicMock
from apply.nodes.revise import revise
from apply.models import RevisedDocuments


def test_revise_is_callable():
    assert callable(revise)


def test_revise_returns_revised_latex_and_increments_count():
    state = {
        "cv_latex": r"\documentclass{moderncv}original",
        "cover_letter_latex": r"\documentclass{cover}original",
        "review_critique": {
            "missed_keywords": ["Kubernetes"],
            "company_angles": ["Mention defence focus"],
            "reframing_suggestions": ["Reframe bullet X"],
            "tone_issues": [],
            "checklist": [{"item": "Profile tailored", "passed": False, "notes": "too generic"}],
            "quality_score": 0.6,
            "needs_revision": True,
        },
        "revision_count": 0,
    }
    revised = RevisedDocuments(
        cv_latex=r"\documentclass{moderncv}revised",
        cover_letter_latex=r"\documentclass{cover}revised",
    )
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = revised
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.revise.ChatAnthropic", return_value=mock_llm):
        result = revise(state)

    assert "cv_latex" in result
    assert "cover_letter_latex" in result
    assert result["revision_count"] == 1
    assert "revised" in result["cv_latex"]
    assert "revised" in result["cover_letter_latex"]


def test_revise_increments_existing_count():
    state = {
        "cv_latex": "...", "cover_letter_latex": "...",
        "review_critique": {
            "missed_keywords": [], "company_angles": [], "reframing_suggestions": [],
            "tone_issues": [], "checklist": [], "quality_score": 0.7, "needs_revision": True,
        },
        "revision_count": 1,
    }
    revised = RevisedDocuments(cv_latex="cv2", cover_letter_latex="cl2")
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = revised
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.revise.ChatAnthropic", return_value=mock_llm):
        result = revise(state)

    assert result["revision_count"] == 2


def test_revise_uses_revised_documents_schema():
    state = {
        "cv_latex": "cv", "cover_letter_latex": "cl",
        "review_critique": {
            "missed_keywords": [], "company_angles": [], "reframing_suggestions": [],
            "tone_issues": [], "checklist": [], "quality_score": 0.7, "needs_revision": True,
        },
        "revision_count": 0,
    }
    revised = RevisedDocuments(cv_latex="cv2", cover_letter_latex="cl2")
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = revised
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.revise.ChatAnthropic", return_value=mock_llm):
        revise(state)

    mock_llm.with_structured_output.assert_called_once_with(RevisedDocuments)


def test_revise_passes_current_drafts_to_prompt():
    state = {
        "cv_latex": "UNIQUE_CV_CONTENT",
        "cover_letter_latex": "UNIQUE_CL_CONTENT",
        "review_critique": {
            "missed_keywords": [], "company_angles": [], "reframing_suggestions": [],
            "tone_issues": [], "checklist": [], "quality_score": 0.7, "needs_revision": True,
        },
        "revision_count": 0,
    }
    revised = RevisedDocuments(cv_latex="cv2", cover_letter_latex="cl2")
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = revised
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.revise.ChatAnthropic", return_value=mock_llm):
        revise(state)

    prompt = mock_structured.invoke.call_args[0][0]
    assert "UNIQUE_CV_CONTENT" in prompt
    assert "UNIQUE_CL_CONTENT" in prompt
