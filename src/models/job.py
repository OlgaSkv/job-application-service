from pydantic import BaseModel, Field
from typing import Optional, List


from typing import Literal


class JDRecord(BaseModel):
    """
    Normalized job description data for resume gap and skill analysis.
    Matches the schema in config/schemas/jd_record_schema.json and the extraction prompt.
    """

    company: str = Field(..., description="Company name (normalized, no legal suffixes).")
    role: str = Field(..., description="Job title or role as stated in the posting.")
    role_type: Optional[str] = Field(
        None,
        description="Functional role based on core responsibilities and technical focus (e.g., 'Applied Data Science', 'ML Engineering').",
    )
    industry_domain: Optional[str] = Field(
        None,
        description="Primary industry or business domain (e.g., 'Healthcare', 'Financial Services').",
    )
    location: Optional[str] = Field(
        None, description="Normalized job location in 'City, ST' format."
    )
    compensation: Optional[str] = Field(
        None, description="Normalized compensation range (e.g., '$95,000 - $150,000/year')."
    )
    job_descr_summary: str = Field(
        ..., description="3-5 sentence summary of what the person does every day."
    )
    job_descr_full: str = Field(
        ...,
        description="Comprehensive, rewritten job description covering responsibilities, team, deliverables, required background, and experience expectations.",
    )
    skills_required: Optional[List[str]] = Field(
        default_factory=list,
        description="Core technologies essential to daily work (languages, frameworks, cloud, data tools, etc.).",
    )
    skills_preferred: Optional[List[str]] = Field(
        default_factory=list, description="Secondary or 'nice-to-have' technologies."
    )
    soft_skills: Optional[List[str]] = Field(
        default_factory=list,
        description="Behavioral and interpersonal competencies (4-8, e.g., 'communication', 'collaboration').",
    )
    seniority: Optional[Literal["Entry", "Mid", "Senior", "Principal", ""]] = Field(
        "", description="Seniority level inferred from posting."
    )
    employment_type: Optional[Literal["FT", "PT", "Contract", "Internship", ""]] = Field(
        "", description="Employment type: FT, PT, Contract, Internship, or blank."
    )
    work_model: Optional[Literal["Remote", "Hybrid", "Onsite", ""]] = Field(
        "", description="Work model: Remote, Hybrid, Onsite, or blank."
    )
    clearance_required: Optional[str] = Field(
        "None",
        description="Government clearance required (e.g., 'Secret', 'Top Secret', or 'None').",
    )
    years_experience: Optional[str] = Field(
        None, description="Required years of experience (e.g., '3-5', '5+', '2')."
    )
    domain_knowledge_required: Optional[List[str]] = Field(
        default_factory=list,
        description="Subject-matter expertise explicitly required (≤4 words each, lowercase).",
    )
    domain_knowledge_preferred: Optional[List[str]] = Field(
        default_factory=list,
        description="Subject-matter expertise mentioned as preferred (≤4 words each, lowercase).",
    )
    education_required: Optional[
        Literal["High School", "Associate", "Bachelor's", "Master's", "PhD", "Unspecified"]
    ] = Field("Unspecified", description="Minimum required degree level.")
    education_preferred: Optional[
        Literal["High School", "Associate", "Bachelor's", "Master's", "PhD", "Unspecified", ""]
    ] = Field("", description="Preferred or target degree level if stated.")
    education_specs: Optional[List[str]] = Field(
        default_factory=list,
        description="Degree disciplines/fields explicitly named (lowercase, ≤3-4 words each).",
    )
