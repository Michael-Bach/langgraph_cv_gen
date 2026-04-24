from langchain_anthropic import ChatAnthropic
from apply.state import ApplyState
from apply.models import ReviewCritique
from apply.profile import load_profile

_MODEL = "claude-sonnet-4-5"


def review(state: ApplyState) -> dict:
    """Review the drafted CV and cover letter and produce structured critique.

    Acts as a hiring manager proxy using all six skill files as context.
    quality_score = passing_checklist_items / 11.
    needs_revision = True if quality_score < 0.8.

    CRITICAL: Never suggest fabricating skills or experience.

    Model: claude-sonnet-4-5
    Returns: {"review_critique": dict}  (ReviewCritique.model_dump())
    """
    profile = load_profile()
    llm = ChatAnthropic(model=_MODEL)
    structured = llm.with_structured_output(ReviewCritique)

    job = state.get("job_parsed", {})
    prompt = f"""You are a hiring manager proxy reviewing a job application for quality and fit.

## Candidate Profile
{profile["candidate_profile"]}

## Behavioral Profile
{profile["behavioral_profile"]}

## Writing Style Guide
{profile["writing_style"]}

## Evaluation Framework
{profile["job_evaluation"]}

## CV Template Guide
{profile["cv_templates"]}

## Cover Letter Template Guide
{profile["cover_letter_templates"]}

## Job Posting
Company: {job.get("company")}
Role: {job.get("role")}
Full posting:
{job.get("raw_text", "")}

## CV to Review
{state.get("cv_latex", "")}

## Cover Letter to Review
{state.get("cover_letter_latex", "")}

Review both documents and produce structured feedback with these exact fields:

1. missed_keywords: requirements from the posting not addressed in the documents
2. company_angles: company-specific angles to strengthen the application
3. reframing_suggestions: passive or generic statements with suggested active rewrites
4. tone_issues: violations of the writing style guide (em-dashes, cliches, passive voice)

5. checklist — run each item, report pass/fail + brief notes:
   1. All claims match actual candidate profile — no fabricated skills or experience
   2. Job titles, dates, company names, and locations are correct
   3. Contact details are present and formatted correctly
   4. Profile statement is tailored to this specific role (not generic)
   5. Key job requirements are addressed in the documents
   6. No LaTeX syntax errors (balanced braces, correct commands)
   7. No spelling or grammar errors
   8. Agentic coding / AI tooling references mention Claude Code by name (if mentioned at all)
   9. Cover letter is addressed correctly (named person or appropriate salutation)
   10. Cover letter fits approximately one page (250-300 words of body text)
   11. CV follows 2-page moderncv/banking format

6. quality_score: (number of PASS items) / 11, as a float 0.0-1.0
7. needs_revision: true if quality_score < 0.8

CRITICAL: Only suggest improvements grounded in the actual candidate profile. Never suggest fabricating skills, experience, or achievements the candidate does not have.
"""
    result: ReviewCritique = structured.invoke(prompt)
    return {"review_critique": result.model_dump()}
