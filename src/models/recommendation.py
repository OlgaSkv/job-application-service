from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class RecommendationType(str, Enum):
    APPLY = "APPLY"
    APPLY_WITH_COVER_LETTER = "APPLY_WITH_COVER_LETTER"
    PASS = "PASS"


class PriorityLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class CareerCoachRecommendation(BaseModel):
    """
    Final recommendation and rationale from the Career Coach agent.
    Includes decision, priority, supporting details, and metadata.
    """

    # Identification and tracking fields
    job_uid: Optional[str] = Field(
        None, description="Deterministic unique identifier for the job record."
    )
    company: Optional[str] = Field(None, description="Company name for tracking.")
    title: Optional[str] = Field(None, description="Job title for tracking.")
    recommendation: RecommendationType = Field(
        ..., description="Final decision: APPLY, APPLY_WITH_COVER_LETTER, or PASS."
    )
    rationale: str = Field(..., description="Explanation for the recommendation.")
    priority: PriorityLevel = Field(..., description="Priority level: High, Medium, or Low.")

    action_items: Optional[List[str]] = Field(
        default=None, description="Recommended next steps or actions."
    )
    cover_letter_needed: Optional[bool] = Field(
        default=None, description="Whether a cover letter is needed."
    )
    deal_breakers: Optional[List[str]] = Field(
        default=None, description="List of hard blockers or deal-breakers."
    )
    considerations: Optional[List[str]] = Field(
        default=None, description="Other considerations or soft blockers."
    )

    confidence: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Confidence score (0.0 to 1.0)."
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the recommendation was created.",
    )

    @classmethod
    def validate_pass_fields(cls, values):
        rec = values.get("recommendation")
        deal_breakers = values.get("deal_breakers")
        considerations = values.get("considerations")
        if rec == RecommendationType.PASS:
            if not (deal_breakers or considerations):
                raise ValueError(
                    "If recommendation is PASS, at least one of deal_breakers or considerations must be provided."
                )
        return values

    # Pydantic v1: use root_validator; v2: use model_validator
    from pydantic import root_validator

    _validate_pass_fields = root_validator(allow_reuse=True)(validate_pass_fields)
