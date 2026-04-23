from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Send

from .state import ApplyState
from .nodes.fetch_job import fetch_job
from .nodes.parse_job import parse_job
from .nodes.evaluate_fit import evaluate_fit
from .nodes.draft import draft_cv, draft_cover_letter
from .nodes.review import review
from .nodes.revise import revise
from .nodes.compile_latex import compile_latex


def _human_approval_node(state: ApplyState) -> dict:
    """Pause execution and wait for human to approve or reject the fit score.

    Resumes when graph.invoke(Command(resume=bool), config) is called.
    Returns: {"human_approved": bool}
    """
    approved = interrupt(
        {"fit_score": state.get("fit_score"), "fit_breakdown": state.get("fit_breakdown")}
    )
    return {"human_approved": bool(approved)}


def should_revise(state: ApplyState) -> str:
    """Routing function: decide whether to revise or compile after review.

    Returns "revise" if needs_revision is True and revision_count < 2.
    Returns "compile" otherwise.
    """
    critique = state.get("review_critique") or {}
    if critique.get("needs_revision") and (state.get("revision_count") or 0) < 2:
        return "revise"
    return "compile"


def _route_after_approval(state: ApplyState):
    """Fan out to parallel drafting if approved; route to END if rejected."""
    if state.get("human_approved"):
        return [Send("draft_cv", state), Send("draft_cover_letter", state)]
    return END


def build_graph():
    """Build and compile the apply graph with MemorySaver checkpointer."""
    builder = StateGraph(ApplyState)

    builder.add_node("fetch_job", fetch_job)
    builder.add_node("parse_job", parse_job)
    builder.add_node("evaluate_fit", evaluate_fit)
    builder.add_node("human_approval", _human_approval_node)
    builder.add_node("draft_cv", draft_cv)
    builder.add_node("draft_cover_letter", draft_cover_letter)
    builder.add_node("review", review)
    builder.add_node("revise", revise)
    builder.add_node("compile_latex", compile_latex)

    builder.add_edge(START, "fetch_job")
    builder.add_edge("fetch_job", "parse_job")
    builder.add_edge("parse_job", "evaluate_fit")
    builder.add_edge("evaluate_fit", "human_approval")

    builder.add_conditional_edges(
        "human_approval",
        _route_after_approval,
        ["draft_cv", "draft_cover_letter", END],
    )

    builder.add_edge("draft_cv", "review")
    builder.add_edge("draft_cover_letter", "review")

    builder.add_conditional_edges(
        "review",
        should_revise,
        {"revise": "revise", "compile": "compile_latex"},
    )

    builder.add_edge("revise", "review")
    builder.add_edge("compile_latex", END)

    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)


graph = build_graph()
