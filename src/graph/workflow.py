from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, List, Dict, Any
import logging

# Use relative imports since this is within the src package
from ..tools.eligibility_checker import check_eligibility
from ..agents.jd_parser import parse_job_description
from ..agents.ats_scorer import score_resume_against_jd


class WorkflowState(TypedDict):
    """
    State dictionary for the job processing workflow.

    Contains all data that flows through the workflow nodes:
    - Input data: job details, resume, profile
    - Intermediate results: parsed JD, eligibility report
    - Final outputs: ATS score
    - Metadata: errors, processing flags
    """

    job_uid: str
    job_url: str  # Cleaned URL
    job_portal: Optional[str]  # Portal name (LinkedIn, Greenhouse, etc.)
    job_description: str  # Cleaned description
    date_saved: str
    resume: Optional[str]
    personal_statement: Optional[str]
    candidate_profile: Optional[Dict[str, Any]]
    parsed_jd: Optional[Dict[str, Any]]
    eligibility_report: Optional[Dict[str, Any]]
    ats_score: Optional[Dict[str, Any]]
    company_report: Optional[Dict[str, Any]]  # Future use
    coach_recommendation: Optional[Dict[str, Any]]  # Future use
    skip_scoring: bool
    errors: List[str]
    processing_time_seconds: Optional[float]


# --- Node Functions ---


def parse_jd_node(state: WorkflowState) -> WorkflowState:
    """
    Parse job description to extract structured data.

    Calls the JD Parser LLM agent to extract company, role, skills, etc.
    """
    if not state.get("job_description") or not state["job_description"].strip():
        error_msg = f"Empty job description for job_uid {state.get('job_uid')}"
        logging.error(error_msg)
        state.setdefault("errors", []).append(error_msg)
        return state

    try:
        state["parsed_jd"] = parse_job_description(state["job_description"])
    except Exception as e:
        logging.error(f"Error in parse_jd_node for job_uid {state.get('job_uid')}: {e}")
        state.setdefault("errors", []).append(f"parse_jd_node: {e}")
    return state


def check_eligibility_node(state: WorkflowState) -> WorkflowState:
    """
    Check eligibility using rule-based logic.

    Evaluates hard/soft blockers (clearance, location, etc.) and sets
    skip_scoring flag if ineligible to avoid unnecessary LLM calls.
    """
    if not state.get("parsed_jd"):
        error_msg = f"Missing parsed_jd for job_uid {state.get('job_uid')}"
        logging.error(error_msg)
        state.setdefault("errors", []).append(error_msg)
        state["skip_scoring"] = True
        return state

    try:
        result = check_eligibility(state["parsed_jd"], state["candidate_profile"])
        state["eligibility_report"] = result
        state["skip_scoring"] = not result.get("eligible", True)
    except Exception as e:
        logging.error(f"Error in check_eligibility_node for job_uid {state.get('job_uid')}: {e}")
        state.setdefault("errors", []).append(f"check_eligibility_node: {e}")
    return state


def score_ats_node(state: WorkflowState) -> WorkflowState:
    """
    Score resume against job description using ATS Scorer LLM agent.

    Generates 30-point ATS score with detailed breakdown and rationale.
    Only called if candidate is eligible (no hard blockers).
    """
    if not state.get("resume") or not state["resume"].strip():
        error_msg = f"Empty resume for job_uid {state.get('job_uid')}"
        logging.error(error_msg)
        state.setdefault("errors", []).append(error_msg)
        return state

    try:
        state["ats_score"] = score_resume_against_jd(
            resume=state["resume"],
            job_description=state["job_description"],
            company=state["parsed_jd"].get("company") if state["parsed_jd"] else None,
            title=state["parsed_jd"].get("role") if state["parsed_jd"] else None,
            job_uid=state["job_uid"],
        )
    except Exception as e:
        logging.error(f"Error in score_ats_node for job_uid {state.get('job_uid')}: {e}")
        state.setdefault("errors", []).append(f"score_ats_node: {e}")
    return state


# --- Routing ---
def route_after_eligibility(state: WorkflowState) -> str:
    """
    Route based on eligibility check results.

    If ineligible (hard blockers), skip scoring to save API costs.
    If eligible, proceed to ATS scoring.
    """
    if state.get("skip_scoring", False):
        return END
    return "score_ats"


# --- Graph Definition ---
def create_workflow() -> StateGraph:
    """
    Create the LangGraph workflow for job processing.

    Flow:
    1. parse_jd (LLM) - Extract structured data from job description
    2. check_eligibility (rule-based) - Identify blockers
    3. score_ats (LLM) - Generate 30-point ATS score (if eligible)

    Returns:
        Compiled StateGraph workflow

    Example:
        >>> workflow = create_workflow()
        >>> initial_state = {
        ...     "job_uid": "JD-001",
        ...     "job_description": "Software Engineer role at Acme...",
        ...     "resume": "Experienced engineer with...",
        ...     "candidate_profile": {...},
        ...     "errors": []
        ... }
        >>> result = workflow.invoke(initial_state)
        >>> print(result.get("ats_total_score"))
        24
    """
    workflow = StateGraph(WorkflowState)

    # Add nodes
    workflow.add_node("parse_jd", parse_jd_node)
    workflow.add_node("check_eligibility", check_eligibility_node)
    workflow.add_node("score_ats", score_ats_node)

    # Set entry point
    workflow.set_entry_point("parse_jd")

    # Define edges
    workflow.add_edge("parse_jd", "check_eligibility")
    workflow.add_conditional_edges(
        "check_eligibility", route_after_eligibility, {"score_ats": "score_ats", END: END}
    )
    workflow.add_edge("score_ats", END)

    return workflow.compile()
