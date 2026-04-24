# tests/test_nodes/test_parse_job.py
from unittest.mock import patch, MagicMock
from apply.nodes.parse_job import parse_job
from apply.models import ParsedJob


def test_parse_job_is_callable():
    assert callable(parse_job)


def test_parse_job_returns_job_parsed_dict():
    state = {"job_text": "Acme is hiring an ML Engineer in Copenhagen.", "revision_count": 0}

    parsed = ParsedJob(
        company="Acme",
        role="ML Engineer",
        location="Copenhagen",
        language="en",
        requirements=["Python", "PyTorch"],
        raw_text="Acme is hiring an ML Engineer in Copenhagen.",
    )
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = parsed
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.parse_job.ChatAnthropic", return_value=mock_llm):
        result = parse_job(state)

    assert "job_parsed" in result
    assert result["job_parsed"]["company"] == "Acme"
    assert result["job_parsed"]["role"] == "ML Engineer"
    assert result["job_parsed"]["language"] == "en"
    assert isinstance(result["job_parsed"]["requirements"], list)


def test_parse_job_uses_structured_output_with_parsed_job():
    state = {"job_text": "Some job text.", "revision_count": 0}
    parsed = ParsedJob(
        company="X", role="Y", location="Z", language="en", requirements=[], raw_text="Some job text."
    )
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = parsed
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.parse_job.ChatAnthropic", return_value=mock_llm):
        parse_job(state)

    mock_llm.with_structured_output.assert_called_once_with(ParsedJob)


def test_parse_job_includes_job_text_in_prompt():
    state = {"job_text": "UNIQUE_JOB_TEXT_MARKER", "revision_count": 0}
    parsed = ParsedJob(
        company="X", role="Y", location="Z", language="en", requirements=[], raw_text="UNIQUE_JOB_TEXT_MARKER"
    )
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = parsed
    mock_llm.with_structured_output.return_value = mock_structured

    with patch("apply.nodes.parse_job.ChatAnthropic", return_value=mock_llm):
        parse_job(state)

    prompt_arg = mock_structured.invoke.call_args[0][0]
    assert "UNIQUE_JOB_TEXT_MARKER" in prompt_arg
