from pathlib import Path
from apply.state import ApplyState

_OUTPUT_DIR = Path(__file__).parents[3] / "outputs"


def compile_latex(state: ApplyState) -> dict:
    """Compile CV and cover letter LaTeX sources to PDF.

    Writes .tex source files to outputs/ then compiles:
      - CV:           subprocess call to `pdflatex`  (moderncv/banking format)
      - Cover letter: subprocess call to `xelatex`   (cover.cls format)

    Output filenames: outputs/{company}_{role}_cv.pdf
                      outputs/{company}_{role}_cover_letter.pdf

    Requires pdflatex and xelatex on PATH (install texlive-full or miktex).
    Raises subprocess.CalledProcessError if compilation fails.

    Returns: {"cv_pdf_path": str, "cover_letter_pdf_path": str}
    """
    raise NotImplementedError
