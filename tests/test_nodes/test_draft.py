from unittest.mock import patch, MagicMock
from apply.nodes.draft import draft_cv, draft_cover_letter

_JOB_PARSED = {
    "company": "Acme", "role": "ML Engineer", "language": "en",
    "requirements": ["Python"], "nice_to_have": [], "location": "CPH",
    "raw_text": "We are hiring...", "department": None,
}


def test_draft_cv_is_callable():
    assert callable(draft_cv)


def test_draft_cover_letter_is_callable():
    assert callable(draft_cover_letter)


def test_draft_cv_returns_cv_latex():
    state = {"job_parsed": _JOB_PARSED, "revision_count": 0}
    mock_response = MagicMock()
    mock_response.content = r"\documentclass[11pt,a4paper,sans]{moderncv}..."
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = mock_response

    with patch("apply.nodes.draft.ChatAnthropic", return_value=mock_llm):
        result = draft_cv(state)

    assert "cv_latex" in result
    assert isinstance(result["cv_latex"], str)
    assert len(result["cv_latex"]) > 0


def test_draft_cv_invokes_llm_once():
    state = {"job_parsed": _JOB_PARSED, "revision_count": 0}
    mock_response = MagicMock()
    mock_response.content = "some latex"
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = mock_response

    with patch("apply.nodes.draft.ChatAnthropic", return_value=mock_llm):
        draft_cv(state)

    mock_llm.invoke.assert_called_once()


def test_draft_cv_prompt_contains_company_and_role():
    state = {"job_parsed": _JOB_PARSED, "revision_count": 0}
    mock_response = MagicMock()
    mock_response.content = "latex"
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = mock_response

    with patch("apply.nodes.draft.ChatAnthropic", return_value=mock_llm):
        draft_cv(state)

    prompt = mock_llm.invoke.call_args[0][0]
    assert "Acme" in prompt
    assert "ML Engineer" in prompt


def test_draft_cover_letter_returns_cover_letter_latex():
    state = {"job_parsed": _JOB_PARSED, "revision_count": 0}
    mock_response = MagicMock()
    mock_response.content = r"\documentclass[]{cover}..."
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = mock_response

    with patch("apply.nodes.draft.ChatAnthropic", return_value=mock_llm):
        result = draft_cover_letter(state)

    assert "cover_letter_latex" in result
    assert isinstance(result["cover_letter_latex"], str)
    assert len(result["cover_letter_latex"]) > 0


def test_draft_cover_letter_invokes_llm_once():
    state = {"job_parsed": _JOB_PARSED, "revision_count": 0}
    mock_response = MagicMock()
    mock_response.content = "some latex"
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = mock_response

    with patch("apply.nodes.draft.ChatAnthropic", return_value=mock_llm):
        draft_cover_letter(state)

    mock_llm.invoke.assert_called_once()


def test_draft_cover_letter_da_prompt_mentions_danish():
    da_job = {**_JOB_PARSED, "language": "da"}
    state = {"job_parsed": da_job, "revision_count": 0}
    mock_response = MagicMock()
    mock_response.content = "latex"
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = mock_response

    with patch("apply.nodes.draft.ChatAnthropic", return_value=mock_llm):
        draft_cover_letter(state)

    prompt = mock_llm.invoke.call_args[0][0]
    assert "Danish" in prompt or "da" in prompt
