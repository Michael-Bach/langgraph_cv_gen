# LangGraph CV Generator

A rewrite of [Mads Lorentzen's CV generator](https://github.com/MadsLorentzen/ai-job-search) in the LangGraph + FastAPI stack. All credit for the original concept, pipeline design, and document generation approach goes to him — this repo is purely a re-implementation in the LangGraph environment.

Given a job URL or pasted description, the pipeline scores candidate fit across five dimensions, waits for human approval, drafts a CV and cover letter in parallel, runs a structured reviewer agent, and compiles both to PDF — with up to two automated revision cycles before final output.

## Pipeline

```
START → fetch_job → parse_job → evaluate_fit
      → [interrupt: human approves fit score]
      → draft_cv ──────────────────┐
      → draft_cover_letter ────────┤ (parallel via Send())
                                   ↓
                                 review
                                   │
                     ┌─────────────┘
                     │ needs_revision AND revision_count < 2
                     ↓
                   revise → review (loop, max 2 revisions)
                     │
                     │ otherwise
                     ↓
               compile_latex → END
```

## Setup

### 1. Install dependencies

```bash
pip install -e ".[dev]"
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set ANTHROPIC_API_KEY (required)
# Optionally set LANGCHAIN_TRACING_V2=true and LANGCHAIN_API_KEY for LangSmith tracing
```

### 3. Fill in your profile

Edit the files in `src/apply/prompts/` — replace `[PLACEHOLDER]` tokens with your actual information. These files are loaded as raw strings and injected into every LLM prompt:

| File | Purpose |
|------|---------|
| `01-candidate-profile.md` | Work history, education, skills, awards |
| `02-behavioral-profile.md` | Behavioral assessment and working style |
| `03-writing-style.md` | Tone and style rules for drafting |
| `04-job-evaluation.md` | Scoring dimensions and career goals |
| `05-cv-templates.md` | LaTeX moderncv template structure |
| `06-cover-letter-templates.md` | LaTeX cover.cls template structure |

### 4. Install LaTeX (required for PDF compilation)

```bash
# Ubuntu/Debian
sudo apt install texlive-full

# macOS
brew install --cask mactex
```

The `compile_latex` node calls `pdflatex` (for the CV) and `xelatex` (for the cover letter). Both must be on `PATH`.

## Run

```bash
uvicorn apply.api:app --reload
```

## API

### POST /apply

Start the pipeline with a job URL or pasted description. Runs until the human-approval interrupt.

**Request:**
```json
{ "job_url": "https://company.com/jobs/ml-engineer" }
```
or
```json
{ "job_text": "We are hiring an ML Engineer..." }
```

**Response:**
```json
{
  "thread_id": "uuid",
  "status": "awaiting_approval",
  "fit_score": 72.5,
  "fit_breakdown": { "verdict": "Good Fit", "technical_skills": { "score": 75, "notes": "..." }, "..." : "..." }
}
```

---

### POST /apply/{thread_id}/resume

Resume after reviewing the fit score. `approved: false` aborts cleanly.

**Request:**
```json
{ "approved": true }
```

**Response (approved):**
```json
{
  "thread_id": "uuid",
  "status": "complete",
  "cv_pdf_path": "outputs/company_role_cv.pdf",
  "cover_letter_pdf_path": "outputs/company_role_cover_letter.pdf"
}
```

**Response (rejected):**
```json
{ "thread_id": "uuid", "status": "aborted" }
```

---

### GET /apply/{thread_id}/result

Get the full current state for any thread.

**Response:**
```json
{
  "thread_id": "uuid",
  "state": { "fit_score": 72.5, "cv_latex": "...", "..." : "..." }
}
```

Returns 404 if the thread does not exist.

## LangSmith Tracing

Set these environment variables — no code changes needed:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=langgraph-cv-gen
```

## Run Tests

```bash
pytest
```

Tests use mocked LLM calls — no API key required.

## Project Structure

```
src/apply/
├── state.py          # ApplyState TypedDict
├── models.py         # Pydantic output schemas
├── profile.py        # Profile loader (reads prompts/)
├── graph.py          # LangGraph pipeline
├── api.py            # FastAPI endpoints
├── nodes/
│   ├── fetch_job.py
│   ├── parse_job.py
│   ├── evaluate_fit.py
│   ├── draft.py      # draft_cv + draft_cover_letter
│   ├── review.py
│   ├── revise.py
│   └── compile_latex.py
└── prompts/          # Markdown skill files (fill in placeholders)
    ├── 01-candidate-profile.md
    ├── 02-behavioral-profile.md
    ├── 03-writing-style.md
    ├── 04-job-evaluation.md
    ├── 05-cv-templates.md
    └── 06-cover-letter-templates.md
```

