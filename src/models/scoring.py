from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class ATSScore(BaseModel):
    """
    ATS Scoring Report - Objective resume-to-JD match analysis.
    Scoring rubric: 13 technical, 8 experience, 9 background (30 points total).
    Includes detailed rationales, strengths, gaps, and ATS optimization keywords.
    """

    # Technical Assessment (13 points)
    technical_capabilities_score: int = Field(
        ..., ge=0, le=6, description="Technical capabilities score (0-6)"
    )
    technical_capabilities_rationale: str = Field(
        ..., description="Rationale for technical capabilities score"
    )

    technology_stack_score: int = Field(..., ge=0, le=4, description="Technology stack score (0-4)")
    technology_stack_rationale: str = Field(..., description="Rationale for technology stack score")

    applied_experience_score: int = Field(
        ..., ge=0, le=3, description="Applied experience score (0-3)"
    )
    applied_experience_rationale: str = Field(
        ..., description="Rationale for applied experience score"
    )

    # Experience Assessment (8 points)
    years_calculation: str = Field(
        ..., description="Calculation/explanation of years of experience"
    )
    years_experience_score: int = Field(
        ..., ge=0, le=4, description="Years of experience score (0-4)"
    )
    years_experience_rationale: str = Field(
        ..., description="Rationale for years of experience score"
    )

    seniority_calculation: str = Field(
        ..., description="Calculation/explanation of seniority match"
    )
    seniority_match_score: int = Field(..., ge=0, le=4, description="Seniority match score (0-4)")
    seniority_match_rationale: str = Field(..., description="Rationale for seniority match score")

    # Background Assessment (9 points)
    domain_score: int = Field(..., ge=0, le=3, description="Domain knowledge score (0-3)")
    domain_rationale: str = Field(..., description="Rationale for domain knowledge score")

    education_score: int = Field(..., ge=0, le=3, description="Education score (0-3)")
    education_rationale: str = Field(..., description="Rationale for education score")

    role_type_score: int = Field(..., ge=0, le=3, description="Role type score (0-3)")
    role_type_rationale: str = Field(..., description="Rationale for role type score")

    # Overall Scoring
    ats_total_score: int = Field(..., ge=0, le=30, description="Sum of all dimension scores")
    ats_category: Literal["✅ ATS Pass", "⚠️ ATS Borderline", "❌ ATS Reject"] = Field(
        ..., description="ATS category result"
    )
    ats_summary: str = Field(..., description="Overall match assessment with dimensional breakdown")

    # Detailed Analysis
    strengths: List[str] = Field(default_factory=list, description="Key strengths matching JD")
    technical_gaps: List[str] = Field(
        default_factory=list, description="Required skills not on resume"
    )

    # Workday ATS Optimization
    skills_for_ats: List[str] = Field(
        default_factory=list,
        description="ATS-ready skills for manual entry: ONLY skills from candidate's resume that match this JD, phrased for ATS optimization. Ready to copy-paste into Workday (comma-separated)",
    )


class EligibilityReport(BaseModel):
    """
    Eligibility report for a candidate/job pair, indicating blockers and eligibility status.
    """

    hard_blockers: List[str] = Field(
        ..., description="List of hard blockers (deal-breakers) that make the candidate ineligible."
    )
    soft_blockers: List[str] = Field(
        ...,
        description="List of soft blockers (concerns) that may affect fit but are not deal-breakers.",
    )
    eligible: bool = Field(
        ..., description="True if the candidate is eligible for the job (no hard blockers)."
    )
    notes: Optional[str] = Field(
        None, description="Additional notes or recommendations from the eligibility checker."
    )
