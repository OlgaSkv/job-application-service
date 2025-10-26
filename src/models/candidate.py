from pydantic import BaseModel
from typing import Optional, List


class CandidateProfile(BaseModel):
    name: Optional[str] = None
    current_location: str
    target_locations: Optional[List[str]]
    work_authorization_status: str
    requires_sponsorship: bool
    current_clearance: Optional[str]
    willing_to_obtain_clearance: bool
    willing_to_relocate: bool
    remote_only: bool
    hybrid_acceptable: bool
    onsite_acceptable: bool
    max_commute_miles: int
    acceptable_long_commute_cities: Optional[List[str]]
    max_travel_percent: int
    salary_minimum: int
    salary_currency: str
    certifications_current: Optional[List[str]]
    certifications_willing: Optional[List[str]]
