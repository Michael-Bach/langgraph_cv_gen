from unittest.mock import patch, MagicMock
from apply.nodes.evaluate_fit import evaluate_fit
from apply.models import FitEvaluation, FitDimension


def test_evaluate_fit_is_callable():
    assert callable(evaluate_fit)


def _make_evaluation(score: float = 75.0) -> FitEvaluation:
    dim = FitDimension(score=score, notes="Good match")
    return FitEvaluation(
        technical_skills=dim,
        experience_match=dim,
        behavioral_fit=dim,
        location="PASS",
        location_notes="Copenhagen",
        career_alignment=dim,
        overall_score=score,
        verdict="Good Fit",
        key_strengths=["RL experience"],
        gaps=["No frontend"],
        recommendation="Apply.",
    )


def test_evaluate_fit_returns_fit_score_and_breakdown():
    state = {
        "job_parsed": {
            "company": "Acme", "role": "ML Engineer", "location": "Copenhagen",
            "language": "en", "requirements": ["Python"], "nice_to_have": [],
            "raw_text": "We are hiring...", "department": None,
        },
        "revision_count": 0,
    }
    evaluation = _make_evaluation(75.0)
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = evaluation
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.evaluate_fit.ChatAnthropic", return_value=mock_llm):
        result = evaluate_fit(state)

    assert "fit_score" in result
    assert "fit_breakdown" in result
    assert result["fit_score"] == 75.0
    assert result["fit_breakdown"]["overall_score"] == 75.0
    assert result["fit_breakdown"]["verdict"] == "Good Fit"


def test_evaluate_fit_uses_fit_evaluation_schema():
    state = {
        "job_parsed": {
            "company": "Acme", "role": "ML Engineer", "location": "Copenhagen",
            "language": "en", "requirements": [], "nice_to_have": [],
            "raw_text": "...", "department": None,
        },
        "revision_count": 0,
    }
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = _make_evaluation()
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.evaluate_fit.ChatAnthropic", return_value=mock_llm):
        evaluate_fit(state)

    mock_llm.with_structured_output.assert_called_once_with(FitEvaluation)


def test_evaluate_fit_includes_profile_in_prompt():
    state = {
        "job_parsed": {
            "company": "Acme", "role": "ML Engineer", "location": "Copenhagen",
            "language": "en", "requirements": [], "nice_to_have": [],
            "raw_text": "...", "department": None,
        },
        "revision_count": 0,
    }
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = _make_evaluation()
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.evaluate_fit.ChatAnthropic", return_value=mock_llm):
        evaluate_fit(state)

    prompt_arg = mock_structured.invoke.call_args[0][0]
    assert "Acme" in prompt_arg
    assert "ML Engineer" in prompt_arg
