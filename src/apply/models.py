from typing import Optional
from pydantic import BaseModel


class ParsedJob(BaseModel):
    company: str
    role: str
    department: Optional[str] = None
    location: str
    language: str  # "en", "da", or "other"
    requirements: list[str]
    nice_to_have: list[str] = []
    raw_text: str


class FitDimension(BaseModel):
    score: float  # 0–100
    notes: str


class FitEvaluation(BaseModel):
    technical_skills: FitDimension
    experience_match: FitDimension
    behavioral_fit: FitDimension
    location: str  # "PASS" or "FAIL"
    location_notes: str
    career_alignment: FitDimension
    overall_score: float  # weighted: technical 30%, experience 25%, behavioral 15%, career 30%
    verdict: str  # "Strong Fit" | "Good Fit" | "Moderate Fit" | "Weak Fit" | "Poor Fit"
    key_strengths: list[str]
    gaps: list[str]
    recommendation: str


class ChecklistItem(BaseModel):
    item: str
    passed: bool
    notes: str = ""


class ReviewCritique(BaseModel):
    missed_keywords: list[str]
    company_angles: list[str]
    reframing_suggestions: list[str]
    tone_issues: list[str]
    checklist: list[ChecklistItem]
    quality_score: float  # 0.0–1.0; below 0.8 triggers revision
    needs_revision: bool
