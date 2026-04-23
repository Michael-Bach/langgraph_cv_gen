from apply.state import ApplyState


def review(state: ApplyState) -> dict:
    """Review the drafted CV and cover letter and produce structured critique.

    Acts as a hiring manager proxy. Uses all six skill files as context.
    Produces a ReviewCritique with:
      - missed_keywords: requirements from posting not addressed in documents
      - company_angles: suggested company-specific additions
      - reframing_suggestions: passive to active rewrites
      - tone_issues: violations of the writing style guide
      - checklist: 11 pass/fail items
      - quality_score: 0.0-1.0 (fraction of checklist items passing)
      - needs_revision: True if quality_score < 0.8

    CRITICAL: Never suggest fabricating skills or experience.

    Model: claude-sonnet-4-5
    Returns: {"review_critique": dict}  (ReviewCritique.model_dump())
    """
    raise NotImplementedError
