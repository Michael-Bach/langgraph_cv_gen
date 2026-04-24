from unittest.mock import patch, MagicMock
from apply.nodes.review import review
from apply.models import ReviewCritique, ChecklistItem


def test_review_is_callable():
    assert callable(review)


def _make_critique(quality_score: float = 0.9) -> ReviewCritique:
    checklist = [
        ChecklistItem(item=f"item {i}", passed=(quality_score >= 0.5))
        for i in range(11)
    ]
    return ReviewCritique(
        missed_keywords=[],
        company_angles=["Mention defence focus"],
        reframing_suggestions=[],
        tone_issues=[],
        checklist=checklist,
        quality_score=quality_score,
        needs_revision=quality_score < 0.8,
    )


def test_review_returns_review_critique_dict():
    state = {
        "job_parsed": {
            "company": "Acme", "role": "ML Engineer", "raw_text": "We are hiring...",
            "language": "en", "requirements": [], "nice_to_have": [],
            "location": "CPH", "department": None,
        },
        "cv_latex": r"\documentclass{moderncv}...",
        "cover_letter_latex": r"\documentclass{cover}...",
        "revision_count": 0,
    }
    critique = _make_critique(0.9)
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = critique
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.review.ChatAnthropic", return_value=mock_llm):
        result = review(state)

    assert "review_critique" in result
    assert result["review_critique"]["quality_score"] == 0.9
    assert result["review_critique"]["needs_revision"] is False


def test_review_needs_revision_when_quality_low():
    state = {
        "job_parsed": {
            "company": "Acme", "role": "ML Engineer", "raw_text": "...",
            "language": "en", "requirements": [], "nice_to_have": [],
            "location": "CPH", "department": None,
        },
        "cv_latex": "...", "cover_letter_latex": "...", "revision_count": 0,
    }
    critique = _make_critique(0.6)
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = critique
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.review.ChatAnthropic", return_value=mock_llm):
        result = review(state)

    assert result["review_critique"]["needs_revision"] is True


def test_review_uses_review_critique_schema():
    state = {
        "job_parsed": {
            "company": "Acme", "role": "ML Engineer", "raw_text": "...",
            "language": "en", "requirements": [], "nice_to_have": [],
            "location": "CPH", "department": None,
        },
        "cv_latex": "...", "cover_letter_latex": "...", "revision_count": 0,
    }
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = _make_critique()
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.review.ChatAnthropic", return_value=mock_llm):
        review(state)

    mock_llm.with_structured_output.assert_called_once_with(ReviewCritique)


def test_review_passes_cv_and_cover_letter_to_prompt():
    state = {
        "job_parsed": {
            "company": "Acme", "role": "ML Engineer", "raw_text": "...",
            "language": "en", "requirements": [], "nice_to_have": [],
            "location": "CPH", "department": None,
        },
        "cv_latex": "UNIQUE_CV_MARKER",
        "cover_letter_latex": "UNIQUE_CL_MARKER",
        "revision_count": 0,
    }
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = _make_critique()
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.review.ChatAnthropic", return_value=mock_llm):
        review(state)

    prompt = mock_structured.invoke.call_args[0][0]
    assert "UNIQUE_CV_MARKER" in prompt
    assert "UNIQUE_CL_MARKER" in prompt
