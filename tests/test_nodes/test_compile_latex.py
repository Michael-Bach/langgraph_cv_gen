import pytest
from apply.nodes.compile_latex import compile_latex


def test_compile_latex_is_callable():
    assert callable(compile_latex)


def test_compile_latex_raises_not_implemented():
    state = {
        "cv_latex": r"\documentclass{moderncv}...",
        "cover_letter_latex": r"\documentclass{cover}...",
        "job_parsed": {"company": "Acme", "role": "ML Engineer"},
        "revision_count": 0,
    }
    with pytest.raises(NotImplementedError):
        compile_latex(state)
