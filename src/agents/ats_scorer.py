"""
ATS Scorer Agent - Evaluates resume-to-JD fit using 30-point rubric.

This LLM agent uses GPT-4o with structured output to score how well a
candidate's resume matches a job description across technical, experience,
and background dimensions. Provides detailed rationales and ATS keywords.
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_openai import ChatOpenAI
from ..utils.parser_utils import load_prompt, load_schema
from ..utils.config_utils import get_config

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "../../config/prompts/ats_scorer.txt")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../../config/schemas/ats_score_schema.json")

ATS_SCORER_PROMPT = load_prompt(PROMPT_PATH)
ATS_SCORER_SCHEMA = load_schema(SCHEMA_PATH)

# Load model config from config.json
config = get_config()
model_config = config.get("MODEL_CONFIG", {}).get(
    "ats_scorer", {"model_name": "gpt-4o", "temperature": 0}
)

# Pass all config parameters to ChatOpenAI
llm = ChatOpenAI(**model_config)
structured_llm = llm.with_structured_output(ATS_SCORER_SCHEMA)


def _calculate_total_score(ats_result: Dict[str, Any]) -> int:
    """
    Deterministically recalculate the total ATS score from component scores.
    
    This prevents LLM arithmetic errors by using simple Python addition.
    
    Total = Technical (13) + Experience (8) + Background (9) = 30 points
    - Technical: technical_capabilities + technology_stack + applied_experience
    - Experience: years_experience + seniority_match
    - Background: domain + education + role_type
    
    Args:
        ats_result: ATS scoring result dictionary from LLM
        
    Returns:
        Correct total score as integer
    """
    technical_total = (
        ats_result.get("technical_capabilities_score", 0) +
        ats_result.get("technology_stack_score", 0) +
        ats_result.get("applied_experience_score", 0)
    )
    
    experience_total = (
        ats_result.get("years_experience_score", 0) +
        ats_result.get("seniority_match_score", 0)
    )
    
    background_total = (
        ats_result.get("domain_score", 0) +
        ats_result.get("education_score", 0) +
        ats_result.get("role_type_score", 0)
    )
    
    return technical_total + experience_total + background_total


def _determine_ats_category(total_score: int) -> str:
    """
    Deterministically determine ATS category based on total score.
    
    This prevents LLM inconsistency by using fixed thresholds:
    - 24-30 (80%+): ✅ ATS Pass
    - 17-23 (57-80%): ⚠️ ATS Borderline
    - 0-16 (<57%): ❌ ATS Reject
    
    Args:
        total_score: Total ATS score (0-30)
        
    Returns:
        ATS category string with emoji
    """
    if total_score >= 24:
        return "✅ ATS Pass"
    elif total_score >= 17:
        return "⚠️ ATS Borderline"
    else:
        return "❌ ATS Reject"


def score_resume_against_jd(
    resume: str,
    job_description: str,
    company: Optional[str] = None,
    title: Optional[str] = None,
    job_uid: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Score resume against job description using LLM with structured output.

    Args:
        resume: Candidate's resume text
        job_description: Job description text
        company: Company name for tracking (optional)
        title: Job title for tracking (optional)
        job_uid: Job UID for tracking (optional)

    Returns:
        ATSScore dictionary or None if scoring fails

    Raises:
        Exception: Logs errors but returns None instead of raising
    """
    if not resume or not job_description:
        logging.warning(f"Empty resume or job description for job {job_uid or 'unknown'}")
        return None

    try:
        system_prompt = ATS_SCORER_PROMPT
        user_prompt = (
            "Score the following resume against the job description using the rubric in the system prompt. "
            "Return structured output as specified.\n\n"
            f"RESUME:\n{resume}\n\nJOB DESCRIPTION:\n{job_description}"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        result = structured_llm.invoke(messages)
        
        # Validate and provide defaults for required fields that LLM might omit
        if result:
            # Ensure technical_gaps is present
            if "technical_gaps" not in result or result.get("technical_gaps") is None:
                logging.warning(f"LLM omitted technical_gaps for job {job_uid}, setting to empty list")
                result["technical_gaps"] = []
            
            # Ensure strengths is present
            if "strengths" not in result or result.get("strengths") is None:
                logging.warning(f"LLM omitted strengths for job {job_uid}, setting to empty list")
                result["strengths"] = []
            
            # Ensure skills_for_ats is present
            if "skills_for_ats" not in result or result.get("skills_for_ats") is None:
                logging.warning(f"LLM omitted skills_for_ats for job {job_uid}, setting to empty list")
                result["skills_for_ats"] = []
        
        # Deterministically recalculate total score and category to prevent LLM errors
        if result:
            total_score = _calculate_total_score(result)
            result["ats_total_score"] = total_score
            result["ats_category"] = _determine_ats_category(total_score)
        
        return result
    except Exception as e:
        logging.error(f"ATS scoring failed for job {job_uid or 'unknown'}: {type(e).__name__}: {e}")
        return None
