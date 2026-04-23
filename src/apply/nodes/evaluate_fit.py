from apply.state import ApplyState


def evaluate_fit(state: ApplyState) -> dict:
    """Score the job posting across 5 dimensions and produce an overall fit score.

    Uses ChatAnthropic with structured output (FitEvaluation) and the evaluation
    framework from profile["job_evaluation"] and profile["candidate_profile"].

    Weighting: Technical 30%, Experience 25%, Behavioral 15%, Career Alignment 30%.
    Thresholds: Strong >=75, Good 60-74, Moderate 45-59, Weak 30-44, Poor <30.

    Model: claude-sonnet-4-5
    Returns: {"fit_score": float, "fit_breakdown": dict}  (FitEvaluation.model_dump())
    """
    raise NotImplementedError
