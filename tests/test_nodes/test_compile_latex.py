from pathlib import Path
from unittest.mock import patch, MagicMock
from apply.nodes.compile_latex import compile_latex


def test_compile_latex_is_callable():
    assert callable(compile_latex)


def test_compile_latex_returns_pdf_paths(tmp_path):
    state = {
        "cv_latex": r"\documentclass{moderncv}...",
        "cover_letter_latex": r"\documentclass{cover}...",
        "job_parsed": {"company": "Acme Corp", "role": "ML Engineer"},
        "revision_count": 0,
    }
    with patch("apply.nodes.compile_latex._OUTPUT_DIR", tmp_path), \
         patch("apply.nodes.compile_latex.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = compile_latex(state)

    assert "cv_pdf_path" in result
    assert "cover_letter_pdf_path" in result
    assert "acme_corp_ml_engineer_cv.pdf" in result["cv_pdf_path"]
    assert "acme_corp_ml_engineer_cover_letter.pdf" in result["cover_letter_pdf_path"]


def test_compile_latex_calls_pdflatex_then_xelatex(tmp_path):
    state = {
        "cv_latex": "cv content",
        "cover_letter_latex": "cl content",
        "job_parsed": {"company": "Acme", "role": "Engineer"},
        "revision_count": 0,
    }
    with patch("apply.nodes.compile_latex._OUTPUT_DIR", tmp_path), \
         patch("apply.nodes.compile_latex.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        compile_latex(state)

    calls = mock_run.call_args_list
    assert len(calls) == 2
    assert calls[0][0][0][0] == "pdflatex"
    assert calls[1][0][0][0] == "xelatex"


def test_compile_latex_writes_tex_files(tmp_path):
    state = {
        "cv_latex": "CV_LATEX_CONTENT",
        "cover_letter_latex": "CL_LATEX_CONTENT",
        "job_parsed": {"company": "Acme", "role": "Engineer"},
        "revision_count": 0,
    }
    with patch("apply.nodes.compile_latex._OUTPUT_DIR", tmp_path), \
         patch("apply.nodes.compile_latex.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        compile_latex(state)

    tex_files = list(tmp_path.glob("*.tex"))
    assert len(tex_files) == 2
    contents = {f.read_text() for f in tex_files}
    assert "CV_LATEX_CONTENT" in contents
    assert "CL_LATEX_CONTENT" in contents


def test_compile_latex_normalises_spaces_in_name(tmp_path):
    state = {
        "cv_latex": "...", "cover_letter_latex": "...",
        "job_parsed": {"company": "Acme Corp Ltd", "role": "Senior ML Engineer"},
        "revision_count": 0,
    }
    with patch("apply.nodes.compile_latex._OUTPUT_DIR", tmp_path), \
         patch("apply.nodes.compile_latex.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = compile_latex(state)

    assert "acme_corp_ltd_senior_ml_engineer_cv.pdf" in result["cv_pdf_path"]
