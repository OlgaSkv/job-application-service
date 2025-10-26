# Next Steps & Future Roadmap

**Current Status:** Production MVP Complete (2 Agents)  
**Last Updated:** October 25, 2025

---

## Overview

The Job Application Service is fully functional with 2 AI agents (JD Parser, ATS Scorer) and ready for real-world use. This document outlines the next development phase: expanding to a 4-agent system.

---

## Current System (MVP)

- **Agent 1:** JD Parser - Extracts structured data from job descriptions
- **Agent 2:** ATS Scorer - Evaluates resume-to-job fit (30-point rubric)
- **Tool:** Eligibility Checker - Rule-based hard/soft blocker identification
- **Infrastructure:** LangGraph workflow, Google Sheets integration, privacy-by-design

---

## Short-Term Goal: Complete the 4-Agent System

### Agent 3: Company Researcher Agent

**What it does:**
Researches companies to provide culture fit analysis, company insights, and strategic information before you apply.

**Capabilities:**
- Company profile analysis and culture indicators
- Culture fit assessment and red flag identification
- Recent news, funding, and market position research
- Network analysis and referral opportunities
- Competitive intelligence and stability assessment

**Output:**
Provides company overview, culture fit score, pros/cons, recent news, and referral opportunities.

---

### Agent 4: Career Coach Agent

**What it does:**
Synthesizes all analysis to provide strategic recommendations and personalized application guidance.

**Capabilities:**
- Holistic recommendation (APPLY/REJECT/MAYBE) with reasoning
- Application strategy and networking approach
- Skills positioning and project highlighting
- Gap analysis and mitigation strategies
- Cover letter themes and talking points

**Output:**
Provides recommendation with confidence level, application strategy, positioning guidance, gap mitigation, and cover letter themes.

---

## Future Enhancements

Additional planned features include:

### Quality Assurance & Testing Strategy

**Expand Unit Test Coverage (Deterministic Components)**
- **Eligibility Checker**: Comprehensive test suite for rule-based logic
  - Work model filtering (onsite/hybrid/remote)
  - Commute distance calculations and edge cases
  - Clearance requirement validation
  - Travel percentage thresholds
  - Certification matching logic
  - Relocation requirement checks
- **Distance Calculator**: Geographic computation accuracy
  - Address parsing and normalization
  - Distance calculation verification
  - Long commute exception handling
- **Google Sheets/Drive Tools**: Integration reliability
  - Connection handling and error recovery
  - Data formatting and schema validation
  - Batch operation correctness
- **Parser Utils**: Data extraction and transformation
  - Date parsing and normalization
  - Text cleaning and sanitization
  - Field extraction edge cases

**DeepEval Integration (LLM Agent Evaluation)**
- Top candidate framework for evaluating and testing large language models
- **JD Parser Agent Testing**:
  - Structured output validation (JSON schema adherence)
  - Field extraction accuracy across diverse job postings
  - Edge case handling (missing fields, ambiguous requirements)
  - Consistency across similar job descriptions
- **ATS Scorer Agent Testing**:
  - Rubric adherence and scoring consistency
  - Rationale quality and evidence citation
  - Hallucination detection (claims not in resume/JD)
  - Context relevance (using appropriate information)
  - Answer relevance (addressing scoring criteria correctly)
- **Regression Testing**:
  - Prompt change impact assessment
  - Model version upgrade validation
  - Performance benchmarking and A/B testing
- **Continuous Evaluation**:
  - Automated test runs on prompt updates
  - Quality metrics tracking over time
  - Failure case identification and analysis

**Why This Approach:**
- **Unit tests** for deterministic, rule-based components → Fast, reliable, comprehensive coverage
- **DeepEval** for LLM agents → Specialized metrics for quality, consistency, and hallucination detection
- **Separation of concerns** → Right tool for each component type

### Feature Expansion
- Cover letter generation
- Resume version management
- Job board integrations (LinkedIn, Indeed, etc.)
- Application tracking and analytics dashboard

---

**Last Updated:** October 25, 2025
