from apply.state import ApplyState


def parse_job(state: ApplyState) -> dict:
    """Parse job posting text into structured fields.

    Uses ChatAnthropic with structured output (ParsedJob) to extract:
    company, role, department, location, language, requirements, nice_to_have.

    Model: claude-sonnet-4-5 via langchain_anthropic.ChatAnthropic
    Returns: {"job_parsed": dict}  (ParsedJob.model_dump())
    """
    raise NotImplementedError
