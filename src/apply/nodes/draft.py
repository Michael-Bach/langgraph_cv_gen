import json
from langchain_anthropic import ChatAnthropic
from apply.state import ApplyState
from apply.profile import load_profile

_MODEL = "claude-sonnet-4-5"


def draft_cv(state: ApplyState) -> dict:
    """Draft a tailored CV as a LaTeX string.

    Uses the CV template guide, candidate profile, and writing style to produce
    a complete moderncv/banking LaTeX document. CV is always in English.
    Compile with pdflatex. Hard 2-page limit.
    Any mention of agentic coding must reference Claude Code by name.

    Model: claude-sonnet-4-5
    Returns: {"cv_latex": str}
    """
    profile = load_profile()
    llm = ChatAnthropic(model=_MODEL)

    job = state.get("job_parsed", {})
    prompt = f"""Draft a complete, compilable LaTeX CV targeting this specific role.

## Candidate Profile
{profile["candidate_profile"]}

## CV Template and Guidelines (follow exactly)
{profile["cv_templates"]}

## Writing Style Guide
{profile["writing_style"]}

## Target Role
Company: {job.get("company", "Unknown")}
Role: {job.get("role", "Unknown")}
Required skills: {json.dumps(job.get("requirements", []))}
Nice to have: {json.dumps(job.get("nice_to_have", []))}

Instructions:
- Replace ALL [PLACEHOLDER] tokens with content from the candidate profile
- Tailor the profile statement and experience bullets to the target role
- Follow the moderncv/banking LaTeX format exactly as shown in the template guide
- Hard 2-page limit when compiled with pdflatex
- If mentioning agentic coding or AI tooling, reference Claude Code by name
- Return ONLY the complete LaTeX source — no explanation, no markdown fences
"""
    response = llm.invoke(prompt)
    return {"cv_latex": response.content}


def draft_cover_letter(state: ApplyState) -> dict:
    """Draft a tailored cover letter as a LaTeX string.

    Uses the cover.cls template, candidate profile, and writing style.
    Language matches state["job_parsed"]["language"] (en/da/other).
    Compile with xelatex. Hard 1-page / 250-300 word limit.
    No em-dashes. No cliches. Forward-looking framing.

    Model: claude-sonnet-4-5
    Returns: {"cover_letter_latex": str}
    """
    profile = load_profile()
    llm = ChatAnthropic(model=_MODEL)

    job = state.get("job_parsed", {})
    language = job.get("language", "en")
    language_name = "Danish" if language == "da" else "English"

    prompt = f"""Draft a complete, compilable LaTeX cover letter targeting this specific role.

## Candidate Profile
{profile["candidate_profile"]}

## Cover Letter Template and Guidelines (follow exactly)
{profile["cover_letter_templates"]}

## Writing Style Guide
{profile["writing_style"]}

## Target Role
Company: {job.get("company", "Unknown")}
Role: {job.get("role", "Unknown")}
Language: {language} — write the letter in {language_name}
Required skills: {json.dumps(job.get("requirements", []))}

Instructions:
- Replace ALL [PLACEHOLDER] tokens with content from the candidate profile
- Write the entire letter in {language_name}
- Follow the cover.cls LaTeX format exactly as shown in the template guide
- Hard 1-page limit, 250-300 words of body text maximum
- No em-dashes. No cliches. Forward-looking framing (focus on what you will do for them)
- If mentioning agentic coding or AI tooling, reference Claude Code by name
- Return ONLY the complete LaTeX source — no explanation, no markdown fences
"""
    response = llm.invoke(prompt)
    return {"cover_letter_latex": response.content}
