from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent / "prompts"

_FILES = {
    "candidate_profile": "01-candidate-profile.md",
    "behavioral_profile": "02-behavioral-profile.md",
    "writing_style": "03-writing-style.md",
    "job_evaluation": "04-job-evaluation.md",
    "cv_templates": "05-cv-templates.md",
    "cover_letter_templates": "06-cover-letter-templates.md",
}


def load_profile() -> dict[str, str]:
    """Load all skill markdown files as raw strings. Populate [PLACEHOLDER] tokens before use."""
    return {key: (_PROMPTS_DIR / filename).read_text(encoding="utf-8")
            for key, filename in _FILES.items()}
