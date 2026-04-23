from apply.state import ApplyState


def test_applystate_has_all_required_fields():
    hints = ApplyState.__annotations__
    expected = {
        "job_url", "job_text", "job_parsed",
        "fit_score", "fit_breakdown", "human_approved",
        "cv_latex", "cover_letter_latex",
        "review_critique", "revision_count",
        "cv_pdf_path", "cover_letter_pdf_path",
    }
    assert expected.issubset(hints.keys())


def test_applystate_can_be_constructed_partially():
    state: ApplyState = {"job_url": "https://example.com/job", "revision_count": 0}
    assert state["job_url"] == "https://example.com/job"
