from typing import TypedDict


class ApplyState(TypedDict, total=False):
    job_url: str
    job_text: str
    job_parsed: dict
    fit_score: float
    fit_breakdown: dict
    human_approved: bool
    cv_latex: str
    cover_letter_latex: str
    review_critique: dict
    revision_count: int
    cv_pdf_path: str
    cover_letter_pdf_path: str
