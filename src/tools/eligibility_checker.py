from typing import Dict, Any

# Use relative imports since this is within the src package
from ..models.scoring import EligibilityReport
from ..utils.distance_calculator import is_within_commute_range


def check_eligibility(jd: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic eligibility checker for hard/soft blockers.

    Evaluates job requirements against candidate profile to identify:
    - Hard blockers: Deal-breakers that make the job unsuitable
    - Soft blockers: Concerns that can potentially be addressed

    This is rule-based logic (NOT an LLM) to ensure consistent, explainable results
    for compliance-critical factors like clearance, location, and certifications.

    Args:
        jd: Parsed job description dictionary
        profile: Candidate profile dictionary with preferences and constraints

    Returns:
        EligibilityReport dictionary with blockers, eligible status, and notes
    """
    hard_blockers = []
    soft_blockers = []
    notes = []

    # Company/title presence
    if not jd.get("company") or not jd.get("role"):
        hard_blockers.append("Missing company or job title in job description.")

    # Security clearance
    clearance_required = jd.get("clearance_required", "None")
    clearance_current = profile.get("current_clearance")
    clearance_willing = profile.get("willing_to_obtain_clearance", False)
    if clearance_required not in ["None", "", None]:
        if not clearance_current and not clearance_willing:
            hard_blockers.append(f"Requires {clearance_required} clearance, candidate unwilling.")

    # Work model compatibility
    work_model = jd.get("work_model", "")
    onsite_acceptable = profile.get("onsite_acceptable", False)
    hybrid_acceptable = profile.get("hybrid_acceptable", False)
    if work_model == "Onsite" and not onsite_acceptable:
        hard_blockers.append("Job is onsite but candidate is not open to onsite roles.")
    if work_model == "Hybrid" and not (hybrid_acceptable or onsite_acceptable):
        hard_blockers.append("Job is hybrid but candidate is not open to hybrid or onsite roles.")
    if work_model == "Remote" and not profile.get("remote_only", True):
        notes.append("Job is remote but candidate is open to onsite/hybrid.")

    # Commute distance
    location = jd.get("location")
    candidate_location = profile.get("current_location")
    max_commute = profile.get("max_commute_miles", 0)
    target_locations = profile.get("target_locations", [])

    if work_model in ["Onsite", "Hybrid"] and location and candidate_location:
        # Use distance calculator to check commute feasibility
        is_acceptable, distance, reason = is_within_commute_range(
            job_location=location,
            candidate_location=candidate_location,
            max_commute_miles=max_commute,
            acceptable_long_commute_cities=target_locations,
        )

        if not is_acceptable:
            if distance is not None:
                # We have a distance - it exceeds max commute
                hard_blockers.append(
                    f"Location too far: {distance:.1f} miles (max: {max_commute} miles)"
                )
            else:
                # Could not calculate distance - treat as soft blocker
                soft_blockers.append(f"Could not verify commute distance to {location}")
        else:
            # Within range - add as a note
            if distance is not None:
                notes.append(f"Commute distance: {distance:.1f} miles")
            else:
                notes.append(reason)

    # Travel percentage
    max_travel = profile.get("max_travel_percent", 0)
    # Placeholder: assume JD has 'travel_percent' field
    travel_percent = jd.get("travel_percent", 0)
    if travel_percent > max_travel:
        hard_blockers.append(
            f"Job requires {travel_percent}% travel, exceeds candidate max of {max_travel}%."
        )

    # Required certifications
    required_certs = jd.get("certifications_required", [])
    current_certs = profile.get("certifications_current", [])
    willing_certs = profile.get("certifications_willing", [])
    for cert in required_certs:
        if cert not in current_certs:
            if cert in willing_certs:
                soft_blockers.append(
                    f"Missing required cert {cert}, but candidate is willing to obtain."
                )
            else:
                hard_blockers.append(f"Missing required cert {cert} and not willing to obtain.")

    # Relocation requirement
    willing_to_relocate = profile.get("willing_to_relocate", False)
    # Placeholder: assume JD has 'relocation_required' field
    relocation_required = jd.get("relocation_required", False)
    if relocation_required and not willing_to_relocate:
        hard_blockers.append("Job requires relocation but candidate is unwilling.")

    eligible = len(hard_blockers) == 0
    return EligibilityReport(
        company=jd.get("company"),
        title=jd.get("role"),
        hard_blockers=hard_blockers,
        soft_blockers=soft_blockers,
        eligible=eligible,
        notes="; ".join(notes) if notes else None,
    ).model_dump()
