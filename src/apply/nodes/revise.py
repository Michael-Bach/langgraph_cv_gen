import json
from langchain_anthropic import ChatAnthropic
from apply.state import ApplyState
from apply.models import RevisedDocuments
from apply.profile import load_profile

_MODEL = "claude-sonnet-4-5"


def revise(state: ApplyState) -> dict:
    """Revise CV and cover letter based on reviewer critique.

    Incorporates suggestions that improve the application without fabricating
    skills or experience. Increments revision_count by 1.

    Model: claude-sonnet-4-5
    Returns: {"cv_latex": str, "cover_letter_latex": str, "revision_count": int}
    """
    profile = load_profile()
    llm = ChatAnthropic(model=_MODEL)
    structured = llm.with_structured_output(RevisedDocuments)

    critique = state.get("review_critique", {})
    failures = [
        item for item in critique.get("checklist", [])
        if not item.get("passed", True)
    ]

    prompt = f"""Revise this job application based on reviewer feedback.

## Writing Style Guide
{profile["writing_style"]}

## Reviewer Feedback
Missed keywords to add: {json.dumps(critique.get("missed_keywords", []))}
Company-specific angles to incorporate: {json.dumps(critique.get("company_angles", []))}
Reframing suggestions: {json.dumps(critique.get("reframing_suggestions", []))}
Tone issues to fix: {json.dumps(critique.get("tone_issues", []))}

Checklist failures to address:
{json.dumps(failures)}

## Current CV (LaTeX)
{state.get("cv_latex", "")}

## Current Cover Letter (LaTeX)
{state.get("cover_letter_latex", "")}

Revise both documents:
- Add missed keywords where they fit naturally in the existing content
- Incorporate company-specific angles where appropriate
- Rewrite passive or generic statements to be active and specific
- Fix tone and style issues flagged above
- Fix all checklist failures

Rules:
- Do NOT fabricate skills, experience, or achievements not in the candidate profile
- Preserve all LaTeX formatting commands and document structure
- CV must remain pdflatex-compatible, 2-page limit
- Cover letter must remain xelatex-compatible, 1-page limit
- Return complete LaTeX source for both documents
"""
    result: RevisedDocuments = structured.invoke(prompt)
    return {
        "cv_latex": result.cv_latex,
        "cover_letter_latex": result.cover_letter_latex,
        "revision_count": (state.get("revision_count") or 0) + 1,
    }
