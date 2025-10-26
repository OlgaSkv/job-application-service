# Candidate Data Directory

This directory contains local candidate information files used by the job processing pipeline.

## Files

### `candidate_profile.json` (Required)
Your personal candidate profile with preferences, qualifications, and requirements. This file is used by the eligibility checker to filter jobs based on your criteria.

**⚠️ This file is excluded from version control (.gitignore) to protect your personal information.**

**Structure:**
```json
{
  "name": "Your Name",
  "current_location": "Your City, State",
  "target_locations": ["Remote", "City 1, State"],
  "work_authorization_status": "US Citizen",
  "requires_sponsorship": false,
  "current_clearance": null,
  "willing_to_obtain_clearance": false,
  "willing_to_relocate": false,
  "remote_only": true,
  "hybrid_acceptable": false,
  "onsite_acceptable": false,
  "max_commute_miles": 0,
  "acceptable_long_commute_cities": [],
  "max_travel_percent": 0,
  "salary_minimum": 100000,
  "salary_currency": "USD",
  "certifications_current": [],
  "certifications_willing": []
}
```

### `candidate_profile.template.json` (Reference)
A template file showing the expected structure. Copy this to `candidate_profile.json` and fill in your information.

## Setup Instructions

1. **Copy the template:**
   ```bash
   cp data/candidate_profile.template.json data/candidate_profile.json
   ```

2. **Edit with your information:**
   - Open `data/candidate_profile.json`
   - Replace placeholder values with your actual information
   - Update preferences, skills, and requirements
   - Set your compensation expectations

3. **Keep it updated:**
   - Update this file as your preferences change
   - Changes will be reflected in the next job processing run

## Security Notes

- `candidate_profile.json` is in `.gitignore` - won't be committed
- `candidate_profile.template.json` is tracked - safe placeholder values
- **Important:** Don't commit your actual profile with personal information
- **Important:** Keep salary expectations and personal details private
