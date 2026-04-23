from apply.state import ApplyState


def draft_cv(state: ApplyState) -> dict:
    """Draft a tailored CV as a LaTeX string.

    Uses ChatAnthropic with the CV template guide (profile["cv_templates"]),
    candidate profile (profile["candidate_profile"]), and writing style
    (profile["writing_style"]) to produce a complete moderncv/banking LaTeX document.

    CV is always in English. Hard 2-page limit. Compile with pdflatex.
    Any mention of agentic coding must reference Claude Code by name.

    Model: claude-sonnet-4-5
    Returns: {"cv_latex": str}
    """
    raise NotImplementedError


def draft_cover_letter(state: ApplyState) -> dict:
    """Draft a tailored cover letter as a LaTeX string.

    Uses ChatAnthropic with the cover letter template (profile["cover_letter_templates"]),
    candidate profile, and writing style to produce a complete cover.cls LaTeX document.

    Language matches state["job_parsed"]["language"] (en/da/other).
    Hard 1-page / 250-300 word limit. Compile with xelatex.
    No em-dashes, no cliches. Forward-looking framing.

    Model: claude-sonnet-4-5
    Returns: {"cover_letter_latex": str}
    """
    raise NotImplementedError
