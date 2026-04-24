from apply.models import ParsedJob, FitDimension, FitEvaluation, ChecklistItem, ReviewCritique


def test_parsed_job_minimal():
    job = ParsedJob(
        company="Acme",
        role="ML Engineer",
        location="Copenhagen",
        language="en",
        requirements=["Python", "PyTorch"],
        raw_text="We are hiring...",
    )
    assert job.company == "Acme"
    assert job.department is None
    assert job.nice_to_have == []


def test_fit_evaluation_overall_score():
    dim = FitDimension(score=80.0, notes="Good match")
    ev = FitEvaluation(
        technical_skills=dim,
        experience_match=dim,
        behavioral_fit=dim,
        location="PASS",
        location_notes="Copenhagen office",
        career_alignment=dim,
        overall_score=80.0,
        verdict="Good Fit",
        key_strengths=["RL experience"],
        gaps=["No frontend"],
        recommendation="Apply.",
    )
    assert ev.overall_score == 80.0


def test_review_critique_needs_revision_flag():
    checklist = [ChecklistItem(item="Claims match profile", passed=True)]
    critique = ReviewCritique(
        missed_keywords=["Kubernetes"],
        company_angles=[],
        reframing_suggestions=[],
        tone_issues=[],
        checklist=checklist,
        quality_score=0.6,
        needs_revision=True,
    )
    assert critique.needs_revision is True
    assert critique.quality_score == 0.6


def test_revised_documents_model():
    from apply.models import RevisedDocuments
    doc = RevisedDocuments(
        cv_latex=r"\documentclass{moderncv}...",
        cover_letter_latex=r"\documentclass{cover}...",
    )
    assert doc.cv_latex.startswith(r"\documentclass")
    assert doc.cover_letter_latex.startswith(r"\documentclass")
