# src/apply/nodes/parse_job.py
from langchain_anthropic import ChatAnthropic
from apply.state import ApplyState
from apply.models import ParsedJob

_MODEL = "claude-sonnet-4-5"


def parse_job(state: ApplyState) -> dict:
    """Parse job posting text into structured fields using an LLM.

    Uses ChatAnthropic.with_structured_output(ParsedJob) to extract:
    company, role, department, location, language, requirements, nice_to_have.

    Model: claude-sonnet-4-5
    Returns: {"job_parsed": dict}  (ParsedJob.model_dump())
    """
    llm = ChatAnthropic(model=_MODEL)
    structured = llm.with_structured_output(ParsedJob)

    prompt = f"""Extract structured information from this job posting.

Job posting:
{state.get("job_text", "")}

Instructions:
- language: "en" for English, "da" for Danish, "other" for anything else
- requirements: list of explicitly required qualifications, skills, or experience
- nice_to_have: list of preferred or bonus qualifications
- raw_text: copy the full job posting text verbatim
- department: extract if mentioned, otherwise leave as null
"""
    result: ParsedJob = structured.invoke(prompt)
    return {"job_parsed": result.model_dump()}
