import subprocess
from pathlib import Path
from apply.state import ApplyState

_OUTPUT_DIR = Path(__file__).parents[3] / "outputs"


def compile_latex(state: ApplyState) -> dict:
    """Compile CV and cover letter LaTeX sources to PDF.

    Writes .tex source files to outputs/ then compiles:
      CV:           pdflatex  (moderncv/banking format)
      Cover letter: xelatex   (cover.cls format)

    Output: outputs/{company}_{role}_cv.pdf
            outputs/{company}_{role}_cover_letter.pdf

    Requires pdflatex and xelatex on PATH (install texlive-full or miktex).
    Raises subprocess.CalledProcessError if compilation fails.

    Returns: {"cv_pdf_path": str, "cover_letter_pdf_path": str}
    """
    job = state.get("job_parsed", {})
    company = job.get("company", "unknown").lower().replace(" ", "_")
    role = job.get("role", "unknown").lower().replace(" ", "_")

    _OUTPUT_DIR.mkdir(exist_ok=True)

    cv_stem = f"{company}_{role}_cv"
    cv_tex = _OUTPUT_DIR / f"{cv_stem}.tex"
    cv_tex.write_text(state.get("cv_latex", ""), encoding="utf-8")

    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(_OUTPUT_DIR), str(cv_tex)],
        check=True,
        capture_output=True,
    )

    cl_stem = f"{company}_{role}_cover_letter"
    cl_tex = _OUTPUT_DIR / f"{cl_stem}.tex"
    cl_tex.write_text(state.get("cover_letter_latex", ""), encoding="utf-8")

    subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-output-directory", str(_OUTPUT_DIR), str(cl_tex)],
        check=True,
        capture_output=True,
    )

    return {
        "cv_pdf_path": str(_OUTPUT_DIR / f"{cv_stem}.pdf"),
        "cover_letter_pdf_path": str(_OUTPUT_DIR / f"{cl_stem}.pdf"),
    }
