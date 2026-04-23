from apply.state import ApplyState


def revise(state: ApplyState) -> dict:
    """Revise CV and cover letter based on reviewer critique.

    Incorporates reviewer suggestions that improve the application:
      - Adds missed keywords where they fit naturally
      - Adds company-specific angles
      - Rewrites passive statements to active voice
      - Fixes tone/style issues and checklist failures

    Does NOT fabricate skills or experience not in the candidate profile.
    Increments revision_count by 1.

    Model: claude-sonnet-4-5
    Returns: {"cv_latex": str, "cover_letter_latex": str, "revision_count": int}
    """
    raise NotImplementedError
