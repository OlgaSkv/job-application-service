# Job Tracker Columns

Complete reference for all columns in the Job_Tracker Google Sheet.

**Total Columns:** 52

---

## 1. Job Metadata & Source (11 columns)

| Column | Type | Description |
|--------|------|-------------|
| **job_uid** | String | Unique identifier for each job (for traceability and linking outputs) |
| **company** | String | Name of the hiring company |
| **role** | String | Job title as listed in the posting |
| **role_type** | String | Type of role (Full-time, Contract, Internship) |
| **industry_domain** | String | Industry or domain (Healthcare, Finance, Tech) |
| **location** | String | Job location (city, state, remote, etc.) |
| **compensation** | String | Salary or compensation details (if available) |
| **job_url** | String | Direct URL to the job posting |
| **job_portal** | String | Source portal (LinkedIn, Indeed, company site) |
| **date_saved** | Date | Date job was saved to the system |
| **date_applied** | Date | Date application was submitted |

---

## 2. Job Description & Skills (3 columns)

| Column | Type | Description |
|--------|------|-------------|
| **skills_for_ats** | Array | ATS-optimized skills extracted from resume |
| **job_descr_summary** | String | Short summary of the job description |
| **job_descr_full** | String | Full job description text |

---

## 3. Requirements & Qualifications (13 columns)

| Column | Type | Description |
|--------|------|-------------|
| **skills_required** | Array | List of required skills from the job description |
| **skills_preferred** | Array | List of preferred skills from the job description |
| **soft_skills** | Array | Required or preferred soft skills (max 8) |
| **seniority** | String | Seniority level (Entry, Mid, Senior, Principal) |
| **employment_type** | String | Employment type (FT, PT, Contract, Internship) |
| **work_model** | String | Work arrangement (Remote, Hybrid, Onsite) |
| **clearance_required** | String | Security clearance required for the job |
| **years_experience** | Number | Years of experience required |
| **domain_knowledge_required** | Array | Required domain knowledge (e.g., Healthcare, ML) |
| **domain_knowledge_preferred** | Array | Preferred domain knowledge |
| **education_required** | String | Required education level (High School, Associate, Bachelor's, Master's, PhD, Unspecified) |
| **education_preferred** | String | Preferred education level |
| **education_specs** | Array | Specific education requirements (e.g., "STEM degree") |

---

## 4. ATS Scoring (23 columns)

### Overall ATS Score
| Column | Type | Description |
|--------|------|-------------|
| **ats_total_score** | Number | Total ATS score (0-30) from ATS Scorer agent |
| **ats_category** | String | ATS score category (✅ Pass, ⚠️ Borderline, ❌ Reject) |

### Technical Capabilities (6 points)
| Column | Type | Description |
|--------|------|-------------|
| **technical_capabilities_score** | Number | Score for technical capabilities match (0-6) |
| **technical_capabilities_rationale** | String | Rationale for technical capabilities score |

### Technology Stack (4 points)
| Column | Type | Description |
|--------|------|-------------|
| **technology_stack_score** | Number | Score for technology stack match (0-4) |
| **technology_stack_rationale** | String | Rationale for technology stack score |

### Applied Experience (3 points)
| Column | Type | Description |
|--------|------|-------------|
| **applied_experience_score** | Number | Score for applied experience match (0-3) |
| **applied_experience_rationale** | String | Rationale for applied experience score |

### Years of Experience (4 points)
| Column | Type | Description |
|--------|------|-------------|
| **years_calculation** | String | Calculated years of experience (from resume/JD) |
| **years_experience_score** | Number | Score for years of experience match (0-4) |
| **years_experience_rationale** | String | Rationale for years experience score |

### Seniority Match (4 points)
| Column | Type | Description |
|--------|------|-------------|
| **seniority_calculation** | String | Calculated seniority (from resume/JD) |
| **seniority_match_score** | Number | Score for seniority match (0-4) |
| **seniority_match_rationale** | String | Rationale for seniority match |

### Domain Knowledge (3 points)
| Column | Type | Description |
|--------|------|-------------|
| **domain_score** | Number | Score for domain match (0-3) |
| **domain_rationale** | String | Rationale for domain score |

### Education (3 points)
| Column | Type | Description |
|--------|------|-------------|
| **education_score** | Number | Score for education match (0-3) |
| **education_rationale** | String | Rationale for education score |

### Role Type (3 points)
| Column | Type | Description |
|--------|------|-------------|
| **role_type_score** | Number | Score for role type match (0-3) |
| **role_type_rationale** | String | Rationale for role type score |

### Summary & Gaps
| Column | Type | Description |
|--------|------|-------------|
| **ats_summary** | String | Summary of ATS scoring (overall assessment) |
| **strengths** | Array | Key strengths (resume-to-JD connections) |
| **technical_gaps** | Array | Technical gaps (missing skills/tools) |

---

## 5. Application Status & Notes (2 columns)

| Column | Type | Description |
|--------|------|-------------|
| **application_status** | String | Status of application (Applied, Interview, Rejected) |
| **notes** | String | Notes from eligibility checker (commute distance, location info) and manual updates |

---

## Column Order (matches config.json)

The columns appear in the Job_Tracker sheet in this exact order:

1. job_uid
2. company
3. role
4. role_type
5. industry_domain
6. location
7. compensation
8. job_url
9. job_portal
10. date_saved
11. date_applied
12. skills_for_ats
13. job_descr_summary
14. job_descr_full
15. skills_required
16. skills_preferred
17. soft_skills
18. seniority
19. employment_type
20. work_model
21. clearance_required
22. years_experience
23. domain_knowledge_required
24. domain_knowledge_preferred
25. education_required
26. education_preferred
27. education_specs
28. ats_total_score
29. ats_category
30. technical_capabilities_score
31. technical_capabilities_rationale
32. technology_stack_score
33. technology_stack_rationale
34. applied_experience_score
35. applied_experience_rationale
36. years_calculation
37. years_experience_score
38. years_experience_rationale
39. seniority_calculation
40. seniority_match_score
41. seniority_match_rationale
42. domain_score
43. domain_rationale
44. education_score
45. education_rationale
46. role_type_score
47. role_type_rationale
48. ats_summary
49. strengths
50. technical_gaps
51. application_status
52. notes

---

## Data Types Legend

- **String**: Text value
- **Number**: Numeric value (integer or decimal)
- **Date**: Date value (YYYY-MM-DD format)
- **Array**: List of values (stored as comma-separated string in Google Sheets)

---
