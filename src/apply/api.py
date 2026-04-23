from uuid import uuid4

from fastapi import FastAPI, HTTPException
from langgraph.types import Command
from pydantic import BaseModel

from .graph import graph

app = FastAPI(title="LangGraph CV Generator", version="0.1.0")


class ApplyRequest(BaseModel):
    job_url: str = ""
    job_text: str = ""


class ResumeRequest(BaseModel):
    approved: bool


@app.post("/apply")
def start_apply(request: ApplyRequest):
    """Start the apply pipeline for a job URL or pasted job description.

    Runs the graph until the human-approval interrupt.
    Returns thread_id, fit_score, and fit_breakdown for the human to review.
    """
    if not request.job_url and not request.job_text:
        raise HTTPException(status_code=422, detail="Provide job_url or job_text.")

    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "job_url": request.job_url,
        "job_text": request.job_text,
        "revision_count": 0,
    }

    graph.invoke(initial_state, config)

    current = graph.get_state(config)
    values = current.values if current else {}

    return {
        "thread_id": thread_id,
        "status": "awaiting_approval",
        "fit_score": values.get("fit_score"),
        "fit_breakdown": values.get("fit_breakdown"),
    }


@app.post("/apply/{thread_id}/resume")
def resume_apply(thread_id: str, request: ResumeRequest):
    """Resume the pipeline after human reviews the fit score.

    approved=true  -> continues to draft -> review -> revise -> compile
    approved=false -> aborts cleanly (graph routes to END)
    """
    config = {"configurable": {"thread_id": thread_id}}

    if not request.approved:
        graph.invoke(Command(resume=False), config)
        return {"thread_id": thread_id, "status": "aborted"}

    graph.invoke(Command(resume=True), config)

    current = graph.get_state(config)
    values = current.values if current else {}

    return {
        "thread_id": thread_id,
        "status": "complete",
        "cv_pdf_path": values.get("cv_pdf_path"),
        "cover_letter_pdf_path": values.get("cover_letter_pdf_path"),
    }


@app.get("/apply/{thread_id}/result")
def get_result(thread_id: str):
    """Return the current state for a thread."""
    config = {"configurable": {"thread_id": thread_id}}
    current = graph.get_state(config)
    if not current:
        raise HTTPException(status_code=404, detail="Thread not found.")
    return {"thread_id": thread_id, "state": current.values}
