import json
from langchain_anthropic import ChatAnthropic
from apply.state import ApplyState
from apply.models import FitEvaluation
from apply.profile import load_profile

_MODEL = "claude-sonnet-4-5"


def evaluate_fit(state: ApplyState) -> dict:
    """Score the job posting across 5 dimensions and produce an overall fit score.

    Uses the evaluation framework from profile["job_evaluation"].
    Weighting: Technical 30%, Experience 25%, Behavioral 15%, Career Alignment 30%.
    Thresholds: Strong >=75, Good 60-74, Moderate 45-59, Weak 30-44, Poor <30.

    Model: claude-sonnet-4-5
    Returns: {"fit_score": float, "fit_breakdown": dict}  (FitEvaluation.model_dump())
    """
    profile = load_profile()
    llm = ChatAnthropic(model=_MODEL)
    structured = llm.with_structured_output(FitEvaluation)

    job = state.get("job_parsed", {})
    prompt = f"""Evaluate the fit between the candidate and this job posting.

## Candidate Profile
{profile["candidate_profile"]}

## Behavioral Profile
{profile["behavioral_profile"]}

## Evaluation Framework (follow this exactly)
{profile["job_evaluation"]}

## Job Details
Company: {job.get("company", "Unknown")}
Role: {job.get("role", "Unknown")}
Location: {job.get("location", "Unknown")}
Required: {json.dumps(job.get("requirements", []))}
Nice to have: {json.dumps(job.get("nice_to_have", []))}
Full posting:
{job.get("raw_text", "")}

Score each dimension 0-100 following the framework. Compute overall_score as:
  technical_skills.score * 0.30
+ experience_match.score * 0.25
+ behavioral_fit.score  * 0.15
+ career_alignment.score * 0.30
Location is pass/fail — not included in overall_score.
"""
    result: FitEvaluation = structured.invoke(prompt)
    return {"fit_score": result.overall_score, "fit_breakdown": result.model_dump()}
