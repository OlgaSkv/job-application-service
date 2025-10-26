# Candidate Profile Field Guide

This document explains each field in the `candidate_profile.json` file and how it's used by the eligibility checker.

## Optional Fields

### `name` (string, optional)
Your full name. This field is not used by the eligibility checker but can be helpful for identification.
- **Example:** `"Jane Smith"`
- **Used for:** Identification only (not used in processing)
- **Can be omitted:** Yes, defaults to `null`

## Required Fields

### `current_location` (string)
Your current city and state.
- **Example:** `"Philadelphia, PA"`
- **Used for:** Checking location requirements and commute distance

### `work_authorization_status` (string)
Your current work authorization status in the US.
- **Examples:** `"US Citizen"`, `"Green Card"`, `"H1B"`, `"EAD"`, `"F1 OPT"`
- **Used for:** Filtering jobs that require specific work authorization

### `requires_sponsorship` (boolean)
Whether you need visa sponsorship for employment.
- **Values:** `true` or `false`
- **Used for:** Future use - not currently enforced by eligibility checker
- **Note:** Currently informational only

### `willing_to_relocate` (boolean)
Whether you're willing to relocate for a job.
- **Values:** `true` or `false`
- **Used for:** Filtering onsite/hybrid jobs in other locations

### `remote_only` (boolean)
Whether you only accept fully remote positions.
- **Values:** `true` or `false`
- **Used for:** Information only - not currently enforced as hard blocker
- **Note:** Set work model preferences using `onsite_acceptable` and `hybrid_acceptable` instead

### `hybrid_acceptable` (boolean)
Whether you accept hybrid work arrangements.
- **Values:** `true` or `false`
- **Used for:** Filtering hybrid positions

### `onsite_acceptable` (boolean)
Whether you accept fully onsite positions.
- **Values:** `true` or `false`
- **Used for:** Filtering onsite positions

### `max_commute_miles` (integer)
Maximum one-way commute distance you're willing to travel (in miles).
- **Example:** `25`
- **Used for:** Calculating if job location is within acceptable commute range

### `max_travel_percent` (integer)
Maximum percentage of time willing to travel for work (0-100).
- **Example:** `10` (for 10%)
- **Used for:** Hard blocker - filters jobs with travel percentage exceeding this value

### `salary_minimum` (integer)
Your minimum acceptable salary.
- **Example:** `120000`
- **Used for:** Future use - not currently enforced by eligibility checker
- **Note:** Currently informational only

### `salary_currency` (string)
Currency for your salary requirements.
- **Example:** `"USD"`
- **Used for:** Currency validation

## Optional Fields

### `target_locations` (array of strings or null)
List of cities/states you're interested in working, or `["Remote"]`.
- **Example:** `["Remote", "New York, NY", "Boston, MA"]`
- **Used for:** Special case - cities in this list are checked for acceptable long commute via `is_within_commute_range`
- **Set to:** `null` or `[]` if no preferences

### `current_clearance` (string or null)
Your current security clearance level, if any.
- **Examples:** `"Secret"`, `"Top Secret"`, `"TS/SCI"`, `null`
- **Used for:** Matching jobs that require clearance
- **Set to:** `null` if you don't have clearance

### `willing_to_obtain_clearance` (boolean)
Whether you're willing to undergo clearance process.
- **Values:** `true` or `false`
- **Used for:** Jobs that require clearance but accept candidates who can obtain it

### `acceptable_long_commute_cities` (array of strings or null)
Cities where you'd accept a longer commute than `max_commute_miles`.
- **Example:** `["San Francisco, CA", "Oakland, CA"]`
- **Used for:** Special case location flexibility
- **Set to:** `null` or `[]` if none

### `certifications_current` (array of strings or null)
Certifications you currently hold.
- **Example:** `["AWS Certified Solutions Architect", "PMP"]`
- **Used for:** Matching jobs that require specific certifications
- **Set to:** `null` or `[]` if none

### `certifications_willing` (array of strings or null)
Certifications you're willing to obtain if required.
- **Example:** `["Security+", "CISSP"]`
- **Used for:** Jobs that require certifications you don't yet have
- **Set to:** `null` or `[]` if none

## Example Profiles

### Remote-Only Software Engineer
```json
{
  "name": "Jane Smith",
  "current_location": "Philadelphia, PA",
  "target_locations": ["Remote"],
  "work_authorization_status": "US Citizen",
  "requires_sponsorship": false,
  "current_clearance": null,
  "willing_to_obtain_clearance": false,
  "willing_to_relocate": false,
  "remote_only": true,
  "hybrid_acceptable": false,
  "onsite_acceptable": false,
  "max_commute_miles": 0,
  "acceptable_long_commute_cities": null,
  "max_travel_percent": 10,
  "salary_minimum": 140000,
  "salary_currency": "USD",
  "certifications_current": ["AWS Certified Developer"],
  "certifications_willing": ["AWS Solutions Architect"]
}
```

### Flexible Local Candidate
```json
{
  "name": "John Doe",
  "current_location": "Austin, TX",
  "target_locations": ["Austin, TX", "Dallas, TX", "Remote"],
  "work_authorization_status": "Green Card",
  "requires_sponsorship": false,
  "current_clearance": null,
  "willing_to_obtain_clearance": true,
  "willing_to_relocate": true,
  "remote_only": false,
  "hybrid_acceptable": true,
  "onsite_acceptable": true,
  "max_commute_miles": 30,
  "acceptable_long_commute_cities": ["Dallas, TX"],
  "max_travel_percent": 25,
  "salary_minimum": 120000,
  "salary_currency": "USD",
  "certifications_current": null,
  "certifications_willing": ["Security+"]
}
```

## How Fields Are Used in Eligibility Checking

### Hard Blockers (Auto-reject)
- Missing company or job title in job description
- `current_clearance: null` + Job requires clearance AND `willing_to_obtain_clearance: false`
- `onsite_acceptable: false` + Job is onsite
- `hybrid_acceptable: false` AND `onsite_acceptable: false` + Job is hybrid
- Job location outside `max_commute_miles` (with calculable distance) + Not in `acceptable_long_commute_cities`
- Job `travel_percent` exceeds `max_travel_percent`
- Job requires certifications you don't have AND not in `certifications_willing`
- `relocation_required: true` + `willing_to_relocate: false`

### Soft Blockers (Flags/warnings)
- Job requires certifications in `certifications_willing` but not in `certifications_current` (willing to obtain)
- Could not calculate commute distance to job location (location verification issue)

### Notes (Information only)
- Job is remote but candidate is open to onsite/hybrid
- Commute distance when within acceptable range
- Other informational messages

## Tips

1. **Be realistic:** Set `max_commute_miles` based on actual driving time, not just distance
2. **Update regularly:** Review and update your profile as your preferences change
3. **Use null wisely:** Use `null` for truly optional fields, `[]` for "none" answers
4. **Target locations:** Put "Remote" first if that's your priority
5. **Salary:** Set `salary_minimum` to your actual walk-away number, not your ideal

## Validation

The JSON must match the `CandidateProfile` Pydantic model in `src/models/candidate.py`. Test validation with:

**PowerShell:**
```powershell
python -c "import json; from src.models.candidate import CandidateProfile; profile = json.load(open('data/candidate_profile.json')); CandidateProfile(**profile); print('Valid')"
```

**Linux/Mac (bash):**
```bash
python -c "import json; from src.models.candidate import CandidateProfile; profile = json.load(open('data/candidate_profile.json')); CandidateProfile(**profile); print('Valid')"
```

**Alternative (create a test file):**

Create `test_profile.py`:
```python
import json
from src.models.candidate import CandidateProfile

with open('data/candidate_profile.json') as f:
    profile = json.load(f)

CandidateProfile(**profile)
print("✓ Candidate profile is valid")
```

Run it:
```powershell
python test_profile.py
```
