# ATS Scoring Rubric - ML/DS/AI Roles (30 Points)

**Last Updated**: October 16, 2025  
**Version**: 2.0 (Post-validation with 19 real job scorings)  
**Target Roles**: Machine Learning Engineer, Data Scientist, AI Engineer, ML Platform Engineer

---

## 📊 Overview

**Total Score**: 0-30 points (Resume-only, objective assessment)

**Structure**:
- **Technical Assessment** (13 points): What you know, use, and build
- **Experience Assessment** (8 points): Years and level alignment
- **Background Assessment** (9 points): Domain, education, role type

**ATS Categories**:
- ✅ **Pass (24-30)**: 80%+ match → Forward to human review
- ⚠️ **Borderline (20-23)**: 67-77% match → Conditional review
- ⚠️ **Borderline (17-19)**: 57-67% match → Weak conditional
- ❌ **Reject (0-16)**: <57% match → Likely filtered out

**Note**: The 80% threshold (24/30) is based on validation showing that:
- **Scores 24-30**: Strong technical and background fit, minor gaps acceptable
- **Scores 20-23**: Good technical fit but notable gaps (experience, domain, or seniority)
- **Scores 17-19**: Moderate fit with significant gaps across multiple dimensions
- **Scores 0-16**: Poor fit, likely auto-rejected

**Context on Thresholds**: In validation with 19 jobs, the highest scores were 22-23/30 (73-77%), all in Borderline range due to consistent seniority overqualification (-4 points across 18/19 jobs). A candidate perfectly matched in all other dimensions would score 26-27/30 (87-90%) and clearly pass. The 80% threshold balances strictness with realistic ATS behavior.

---

## TECHNICAL ASSESSMENT (13 points)

### 1. Technical Capabilities (0-6 points)
**Measures**: ML/statistical methods, algorithms, theoretical foundation, problem-solving approaches

#### Scoring:

**6 points - Exceptional alignment**
- All or nearly all required methods explicitly mentioned on resume
- Strong theoretical foundation evident
- May include advanced techniques beyond requirements
- Example: JD needs "regression, classification, clustering" + resume shows all PLUS "Bayesian methods, causal inference, time series forecasting"

**5 points - Strong alignment**
- Most required methods present (80%+)
- Solid theoretical foundation visible
- Minor gaps in advanced techniques
- Example: JD needs 5 specific methods, resume clearly demonstrates 4-5

**4 points - Solid alignment**
- Key methods covered (60-80%)
- Some gaps in theory or advanced methods
- Core capabilities are present
- Example: JD needs "hypothesis testing, regression, experimental design" + resume shows 2 of 3 clearly

**3 points - Moderate alignment**
- About half of required methods covered (40-60%)
- Gaps are trainable with mentorship
- Foundation is present but incomplete
- Example: JD needs 6 specific methods, resume demonstrates 3

**2 points - Weak alignment**
- Significant gaps in core methods (<40%)
- Theoretical foundation unclear or weak
- Would require substantial ramp-up time
- Example: JD needs advanced ML methods, resume shows only basic statistics

**1 point - Minimal alignment**
- Surface-level mention only
- No depth or practical application evident
- Buzzword usage without substance
- Example: Resume says "familiar with ML" but lists no specific methods

**0 points - No alignment**
- No relevant technical capabilities mentioned
- Completely different skill set

#### Rationale Requirements:
- ✅ List methods found on resume with evidence
- ⚠️ Note partial coverage or related methods
- ❌ List required methods NOT found

---

### 2. Technology Stack (0-4 points)
**Measures**: Programming languages, frameworks, libraries, cloud platforms, databases, orchestration tools

#### Scoring:

**4 points - Near-complete match**
- All or nearly all required tools explicitly listed on resume
- Example: JD needs "Python, SQL, AWS, Docker" → resume lists all four

**3 points - Strong match**
- Core tools present (75%+)
- Minor gaps or acceptable alternatives used
- Example: JD needs "Python, PyTorch, AWS, Airflow" → resume has "Python, PyTorch, GCP, Airflow"
- (GCP is close substitute for AWS)

**2 points - Partial match**
- About half of required tools matched (40-60%)
- Some key tools are missing
- Example: JD needs "Python, Spark, Kubernetes, Snowflake" → resume has only "Python, Pandas"

**1 point - Minimal match**
- Very few tools aligned (<40%)
- Most required tools are absent
- Example: JD needs modern ML stack → resume shows only Excel and basic R

**0 points - No match**
- No relevant tools listed on resume
- Completely different technology ecosystem

#### Tool Equivalence Guidelines:
**Close matches** (give credit):
- PyTorch ≈ TensorFlow (deep learning frameworks)
- AWS ≈ GCP ≈ Azure (cloud platforms - core services)
- PostgreSQL ≈ MySQL ≈ SQL Server (relational databases)
- scikit-learn ≈ similar ML library

**NOT close matches** (don't give credit):
- Python ≠ Java (different languages)
- AWS S3 ≠ local file system
- Spark ≠ Pandas (different scale/paradigm)

#### Rationale Requirements:
- ✅ Tools explicitly on resume
- ⚠️ Similar/related tools with explanation
- ❌ Required tools NOT listed

---

### 3. Applied Experience (0-3 points)
**Measures**: Project types and execution - end-to-end ML, production systems, MLOps, research, analytics pipelines

#### Scoring:

**3 points - Directly relevant project experience**
- Resume shows projects of the same type as JD requires
- Clear end-to-end ownership demonstrated
- Production/deployment experience if JD requires it
- Appropriate scale and complexity
- Example: JD = "build production ML systems serving millions" → resume = "deployed recommendation system to 1M+ users with 99.9% uptime"

**2 points - Transferable experience**
- Different domain but similar problem types and scale
- Similar technical challenges and complexity
- Relevant execution skills demonstrated
- Example: JD = "healthcare ML prediction models" → resume = "fintech fraud detection models in production"
- (Both are supervised learning in production, different domains)

**1 point - Tangential experience**
- Related work but not core responsibilities
- Different scale or scope than required
- Relevant but incomplete experience
- Example: JD = "production ML systems" → resume = "ML prototypes and POCs only" (research phase, not production)

**0 points - No relevant project experience**
- No projects matching job requirements
- Completely different type of work
- Example: JD = "MLOps engineer building deployment pipelines" → resume = "data analyst writing SQL queries"

#### Project Type Examples:
- **End-to-end ML**: Data collection → model training → deployment → monitoring
- **Production systems**: Scalable inference, model serving, A/B testing
- **MLOps**: CI/CD for ML, model versioning, monitoring, retraining pipelines
- **Research**: Novel algorithm development, experimentation, publications
- **Analytics**: Exploratory analysis, dashboards, metric definition

#### Rationale Requirements:
State clearly which project types match and how

---

## EXPERIENCE ASSESSMENT (8 points)

### 4. Years of Experience (0-4 points)
**Measures**: Years in **TARGET FIELD ONLY** (not total career) vs JD requirement

**⚠️ CRITICAL**: This dimension counts ONLY years in the specific target field (e.g., Data Science/ML/AI for DS roles). Total career years are used ONLY in Seniority Match (Dimension 5).

**🐛 CRITICAL BUG FIX (Oct 2025)**: For requirements like "10+ years of Machine Learning experience", count ONLY years working in ML/DS/AI roles, NOT total career years. A candidate with "15 years software engineering + 2 years ML" has only **2 years ML experience** for ML requirements.

#### Mandatory Calculation:
1. **Extract required years from JD** (e.g., "2 years in data science" → 2)
   - **Special case**: For "10+" requirements, use the number as stated (e.g., "10+ years ML" → 10)
2. **Count candidate's years IN TARGET FIELD ONLY**
   - For DS role: Count only Data Science / ML / AI experience years
   - For SWE role: Count only Software Engineering years
   - Career transitioner with 13yr SWE + 2yr DS → For DS role, count ONLY 2yr
   - **NEVER count total career years here** - that's for Seniority Match only
3. **Calculate ratio**: `target_field_years ÷ required_years`
4. **If ratio ≥ 3x → Score 0** (extreme overqualification = flight risk)

#### Scoring:

**4 points - Significantly exceeds (1.5x-2x)**
- 50%-100% more years than required, but within reasonable range
- Strong experience without flight risk concerns
- Example: Has 8 years DS, JD needs 5 years → 8÷5 = 1.6x → Score 4
- Example: Has 6 years DS, JD needs 3-5 years → 6÷4 = 1.5x → Score 4

**3 points - Meets or exceeds (1x-2x)**
- Within stated range or moderately above
- Appropriate experience level
- Example: Has 5 years DS, JD needs 3-5 years → 5÷4 = 1.25x → Score 3
- Example: Has 7 years DS, JD needs 5 years → 7÷5 = 1.4x → Score 3

**2 points - Slightly below**
- Within 1 year of minimum requirement
- Close enough to be trainable quickly
- Example: Has 2.5 years DS, JD needs 3-5 years → 2.5÷3 = 0.83x → Score 2

**1 point - Significantly below**
- 2+ years short of minimum
- Notable experience gap requiring substantial ramp-up
- Example: Has 1 year DS, JD needs 3-5 years → 1÷3 = 0.33x → Score 1

**0 points - Major mismatch (both directions!)**
- **No experience** in target field: 0 years DS for DS role → Score 0
- **Extreme overqualification (≥3x)**: Flight risk, salary mismatch concerns
  - Example: Has 15 years DS, JD needs 2 years DS → 15÷2 = **7.5x** → Score 0
  - Example: Has 12 years DS, JD needs 3 years DS → 12÷3 = **4x** → Score 0
  - Example: Has 18 years DS, JD needs 5 years DS → 18÷5 = **3.6x** → Score 0

#### Career Transitioner Examples (TARGET FIELD ONLY):

**Example 1**: 2yr Data Science + 13yr Software Engineering = **15yr total**
- JD requires: 2 years Data Science experience
- **Years calculation**: 2yr DS ÷ 2yr required = **1x** → Score 3 ✅
- Note: The 13yr SWE is NOT counted here (used only in Seniority Match)

**Example 2**: 1yr Data Science + 9yr Business Analytics = **10yr total**
- JD requires: 3-5 years Data Science experience
- **Years calculation**: 1yr DS ÷ 4yr required = **0.25x** → Score 1 ⚠️
- Note: The 9yr BA is NOT counted here

**Example 3**: 15yr Data Science (entire career in DS) = **15yr total**
- JD requires: 2 years Data Science experience
- **Years calculation**: 15yr DS ÷ 2yr required = **7.5x** → Score 0 ❌
- Note: Extreme overqualification = flight risk

**Example 4 (10+ year requirement)**: 2yr ML + 13yr SWE = **15yr total**
- JD requires: "10+ years of Machine Learning experience"
- **Years calculation**: 2yr ML ÷ 10yr required = **0.2x** → Score 1 ⚠️
- **Critical**: Do NOT count the 13yr SWE as "ML experience" even though the person is experienced
- The requirement explicitly says "10+ years **of Machine Learning**", not "10+ years total"

#### Rationale Requirements:
**Mandatory format**: "Candidate has X years of [target field] experience, [slightly below/meets/exceeds/significantly below] the JD requirement of Y years."

Example: "Candidate has 2 years of ML experience, while JD requires 10 years. This is significantly below the requirement, resulting in a score of 1."

---

### 5. Seniority Match (0-4 points)
**Measures**: Resume level vs JD level expectations (based on **TOTAL career years** and responsibilities)

**⚠️ CRITICAL**: Use **TOTAL CAREER YEARS** (all fields combined) to determine professional level, NOT just target field years.

#### Mandatory Calculation:
1. **Determine JD seniority level from years required:**
   - 0-3 years required = Level 0 (Junior)
   - 3-7 years required = Level 1 (Mid)
   - 7-12 years required = Level 2 (Senior)
   - 12+ years required = Level 3 (Lead)

2. **Determine candidate's seniority level from TOTAL career experience:**
   - 0-3 total years (any field) = Level 0 (Junior)
   - 3-7 total years (any field) = Level 1 (Mid)
   - 7-12 total years (any field) = Level 2 (Senior)
   - 12+ total years (any field) = Level 3 (Lead)
   - **Use TOTAL career to determine level, NOT just target field**
   - A 15-year software engineer who recently transitioned to DS is still Level 3 (Lead)

3. **Count the level gap and score:**
   - 0 levels = Score 3 or 4
   - 1 level = Score 2
   - 2 levels = Score 1
   - 3 levels = Score 0 (maximum gap) **unless career transitioner** (see below)

4. **Check career transitioner status (MANDATORY FOR ALL CANDIDATES):**
   - **Definition**: ≤3 years in target field AND ≥10 years total career
   - Use the target_field_years from Dimension 4 (Years of Experience)
   - **Step a**: Is target_field_years ≤ 3? → [YES/NO]
   - **Step b**: Is total_career_years ≥ 10? → [YES/NO]
   - **Step c**: If BOTH are YES → Candidate IS a career transitioner
   - **Step d**: If ANY is NO → Candidate is NOT a career transitioner
   
5. **Apply career transitioner floor (if applicable):**
   - **If 3-level gap AND IS transitioner → Score 1** (floor protects career switchers)
   - **If 3-level gap AND NOT transitioner → Score 0** (true overqualification, flight risk)
   - **If gap < 3 → Use standard scoring** (transitioner status doesn't change score)

#### Scoring:

**4 points - Perfect match + exceptional track record**
- Seniority level matches exactly (same level as JD)
- Outstanding achievements and proven impact visible
- Quantified results at appropriate level
- Example: Mid-level (4yr total) with "Led 3 ML projects, improved accuracy 25%" for mid role

**3 points - Perfect level match**
- Seniority level aligns well (same level)
- Responsibilities clearly match required level
- Appropriate experience without exceptional achievements
- Example: Mid-level (4yr total) for mid-level role

**2 points - Adjacent level (one step)**
- One seniority level up OR down from requirement
- **Applies to BOTH overqualified and underqualified**
- Example: Level 1 Mid (5yr total) for Level 0 Junior role → Score 2 (1 level overqualified)
- Example: Level 1 Mid (5yr total) for Level 2 Senior role → Score 2 (1 level underqualified)
- Example: Level 2 Senior (10yr total) for Level 1 Mid role → Score 2 (1 level overqualified)

**1 point - Two or three levels off**
- **TWO levels off**: In either direction, notable gap
- **THREE levels off AND career transitioner**: Floor protects career switchers (≤3yr in target field + ≥10yr total)
- Notable gap requiring significant adjustment
- **Examples (2-level gap)**:
  - Level 0 Junior (2yr total) for Level 2 Senior role → Score 1 (2 levels underqualified)
  - Level 2 Senior (10yr total) for Level 0 Junior role → Score 1 (2 levels overqualified)
  - Level 3 Lead (15yr total) for Level 1 Mid role → Score 1 (2 levels overqualified)
- **Examples (3-level gap + transitioner)**:
  - Level 3 Lead (15yr total: 2yr DS + 13yr SWE) for Level 0 Junior DS role → Score 1 (3-level gap BUT career transitioner, floor applies)

**0 points - Major mismatch**
- **3 levels off AND NOT a career transitioner** (true overqualification in same field)
- **OR wrong career track** (Manager → IC or IC → Manager)
- Fundamental incompatibility (won't work out)
- **Flight risk for overqualified, can't handle for underqualified**
- **Examples**:
  - Level 3 Lead (15yr DS) for Level 0 Junior DS role → Score 0 (3 levels overqualified, NOT transitioner = flight risk)
  - Level 0 Junior (2yr total) for Level 3 Lead role → Score 0 (3 levels underqualified, can't handle)
  - Manager → IC or IC → Manager → Score 0 (wrong track)

#### Career Transitioner Example (TOTAL CAREER):

**Example**: 2yr Data Science + 13yr Software Engineering = **15yr total career**
- JD requires: 2 years Data Science experience (= Level 0 Junior role)
- **Seniority calculation**:
  - Step 1: JD level: Level 0 Junior (2yr requirement)
  - Step 2: Candidate level: Level 3 Lead (15yr total career)
  - Step 3: Level gap: 3 levels (Lead vs Junior)
  - Step 4: Transitioner check:
    - Target field years = 2yr DS ≤ 3? **YES**
    - Total career = 15yr ≥ 10? **YES**
    - **IS a career transitioner** ✅
  - Step 5: Gap = 3 AND IS transitioner → **Score: 1** ✅ (floor protects career switcher)

**Why Score 1 (not 0)?** Career transitioner floor protects career switchers:
- **Without floor**: Would score 0 for "overqualification" despite only 2yr in target field
- **With floor**: Score 1 recognizes 3-level gap but acknowledges transferable experience
- **Rationale**: A 15yr software engineer with 2yr DS experience is genuinely interested in DS career growth, not flight risk

**Key Distinction**:
- **Career Transitioner** (2yr DS + 13yr SWE → 15yr total): Score 1 (floor applies)
- **True Overqualification** (15yr DS → 15yr total): Score 0 (flight risk, no floor)

**Contrast with Years Experience (Dimension 4):**
- **Years Score: 3** ✅ (2yr DS ÷ 2yr required = 1x, appropriate field experience)
- **Seniority Score: 1** ✅ (15yr total = Level 3 Lead, 3 levels above Level 0 Junior, BUT career transitioner floor applies)

#### Seniority Level Reference:

| Level | Total Years | Typical Responsibilities |
|-------|-------------|--------------------------|
| **Level 0 (Junior)** | 0-3 | Executing defined tasks, close supervision, learning |
| **Level 1 (Mid)** | 3-7 | Independent projects, mentoring juniors, moderate scope |
| **Level 2 (Senior)** | 7-12 | Leading projects, technical decisions, broad impact |
| **Level 3 (Lead)** | 12+ | Multi-project leadership, architecture, strategic direction |

#### Focus on Responsibilities, Not Just Title:

Look for:
- **Scope of work**: Individual tasks vs full projects vs multiple projects
- **Autonomy**: Closely supervised vs independent vs leading others
- **Impact**: Team-level vs org-level vs company-level
- **Technical depth**: Executing vs designing vs architecting

#### Rationale Requirements:
**Mandatory format**: "JD level: Level N [Junior/Mid/Senior/Lead] (X years). Candidate level: Level N [Junior/Mid/Senior/Lead] (Y total years). Level gap: Z. Transitioner check: [target_field_years] ≤ 3? [YES/NO], [total_years] ≥ 10? [YES/NO] → [IS/NOT] a career transitioner. Score: [0-4]."

**Examples:**
- Career transitioner: "JD level: Level 0 Junior (2yr). Candidate level: Level 3 Lead (15yr total). Level gap: 3. Transitioner check: 2yr DS ≤ 3? YES, 15yr total ≥ 10? YES → IS a career transitioner. Score: 1 (floor applies)."
- True overqualification: "JD level: Level 0 Junior (2yr). Candidate level: Level 3 Lead (15yr DS). Level gap: 3. Transitioner check: 15yr DS ≤ 3? NO → NOT a career transitioner. Score: 0 (flight risk)."
- Standard match: "JD level: Level 1 Mid (5yr). Candidate level: Level 1 Mid (6yr total). Level gap: 0. Transitioner check: 6yr DS ≤ 3? NO → NOT a career transitioner. Score: 4 (perfect match)."

---

## BACKGROUND ASSESSMENT (9 points)

### 6. Domain/Industry (0-3 points)
**Measures**: Industry-specific knowledge shown on resume

#### Scoring:

**3 points - Direct experience in same industry**
- Clear work history in the target industry
- Industry-specific knowledge and terminology evident
- Understands domain problems and constraints
- Example: 2+ years in healthcare tech for healthcare ML role
- Example: Resume shows "HIPAA compliance, clinical workflows, EHR integration" for healthcare role

**2 points - Adjacent/transferable industry experience**
- Related industry with transferable concepts
- Similar business problems or user needs
- Domain knowledge partially applicable
- Example: E-commerce experience for retail analytics role (both are transactional, inventory, customer behavior)
- Example: Fintech for general financial services (both involve transactions, risk, compliance)

**1 point - Minimal domain relevance**
- Tangentially related at best
- Some conceptual overlap but different context
- Different customer needs and constraints
- Example: Manufacturing analytics for logistics ML role (supply chain overlap but different focus)

**0 points - No relevant domain experience**
- No industry connection visible on resume
- Completely different domain with no transferable knowledge
- Example: Education sector background for defense contractor ML role

#### Industry Categories (examples):

**High overlap**:
- E-commerce ↔ Retail
- Fintech ↔ Financial Services
- Digital Health ↔ Healthcare Tech
- AdTech ↔ Media/Entertainment

**Moderate overlap**:
- SaaS ↔ Enterprise Software
- Logistics ↔ Supply Chain
- EdTech ↔ Education

**Low/No overlap**:
- Pharma ↔ Defense
- Gaming ↔ Finance
- Agriculture ↔ Aerospace

#### Rationale Requirements:
- State resume industries/domains worked
- State JD industry/domain
- Assess overlap with specific examples

---

### 7. Education (0-3 points)
**Measures**: Degree level and field alignment with JD requirements

**✅ CLARIFICATION (Oct 2025)**: Exceeding education requirements is **positive**, not negative. A Master's for a Bachelor's requirement = 3/3, not 2/3. Only penalize if explicitly stated "Bachelor's required, no advanced degrees."

#### Scoring:

**3 points - Meets or exceeds requirement + field matches**
- Degree level meets **OR EXCEEDS** requirement, and field is relevant
- Exceeding is good unless JD explicitly says otherwise
- Example: Master's in Computer Science for role requiring "Bachelor's in quantitative field" → 3/3 ✅
- Example: Master's in Computer Science for role requiring "Master's in quantitative field" → 3/3 ✅
- Example: PhD in Statistics for role requiring "advanced degree in statistics or related field" → 3/3 ✅
- Example: Master's in CS + MicroMasters in Data Science for role requiring "Bachelor's in CS" → 3/3 ✅ (exceeds)

**2 points - Meets requirement OR field matches (but not both)**

**Option A**: Degree level matches/exceeds, field is adjacent
- Example: Master's in Physics for CS/ML role requiring "Bachelor's in CS" (quantitative but not direct)
- Example: Master's in Engineering for Data Science role (technical but different focus)

**Option B**: Field matches, degree level is one step below
- Example: Bachelor's in Computer Science for Master's-preferred role
- Example: Master's for PhD-preferred role (but PhD not required)

**1 point - Some relevance**
- Degree or field is somewhat relevant
- Quantitative background but not directly applicable
- Example: Bachelor's in Engineering for data science role (technical/quantitative but not statistics/CS)
- Example: MBA with analytics focus for data science role (some exposure but not technical depth)

**0 points - Missing or irrelevant**
- No degree when required (and requirement is strict)
- Completely unrelated field
- Example: High school diploma only for role requiring Bachelor's
- Example: BA in History for ML Engineer role (no quantitative background)

#### Special Cases:

**"Degree preferred, not required"**
- 0 points for no degree is NOT disqualifying
- Can still pass ATS if other dimensions are strong
- Note in rationale that preference is unmet

**Self-taught with portfolio**
- Score as 0-1 for education
- Should be captured in "Applied Experience" (0-3) instead
- Strong projects can compensate for lack of formal degree

**Bootcamp/Certificate programs**
- Score as 1-2 depending on depth and relevance
- Data Science bootcamp (3-6 months intensive) = 1 point
- ML certificate from university = 1-2 points
- Not equivalent to degree but shows initiative

**PhD for non-research roles**
- PhD for ML Engineer role (not research) = 3 points (exceeds requirement)
- Don't penalize for being "overqualified" unless role explicitly says "no PhD"

#### Degree Field Categories:

**Direct match** (3 points if level matches):
- Computer Science, Data Science, Statistics, Mathematics, Machine Learning, Applied Math

**Adjacent** (2 points if level matches):
- Physics, Engineering (all types), Economics, Quantitative Finance, Operations Research, Computational Biology

**Some relevance** (1 point):
- General Science degrees, Business Analytics, Information Systems, Applied Statistics

**Not relevant** (0 points):
- Humanities, Arts, Social Sciences (without quantitative focus)

#### Rationale Requirements:
- State resume education (degree + field)
- State JD requirement
- Assess match with reasoning

---

### 8. Role Type Alignment (0-3 points)
**Measures**: Job function match based on actual responsibilities and daily work (not just job title)

#### Scoring:

**3 points - Clear history in same role type**
- Resume shows 1-2+ years in this exact job function
- Responsibilities align very well with JD
- Has done this type of work before
- Example: 2+ years as ML Engineer for ML Engineer role
- Example: 3 years as Data Scientist for Data Scientist role

**2 points - Adjacent role type with transferable experience**
- Different title but similar core responsibilities
- Same general function, different emphasis or stage
- Clear transferability of skills and experience
- Example: Software Engineer (ML team) for ML Engineer role (both build production systems, SWE does more general eng)
- Example: Data Analyst (advanced analytics) for junior Data Scientist role (both analyze data, DS adds modeling)

**1 point - Some overlap in responsibilities**
- Different function but some shared activities
- Would require adjustment period and training
- Partial skill transferability
- Example: Research Scientist for ML Engineer role (both use ML, but research = novel methods/papers, engineer = production systems)
- Example: Data Engineer for Data Scientist role (both work with data, but DE = pipelines, DS = modeling/insights)

**0 points - Different job function**
- Completely different type of work
- No meaningful overlap in day-to-day responsibilities
- Example: Business Analyst for ML Engineer role
- Example: Web Developer for Data Scientist role
- Example: Project Manager for IC Data Scientist role

#### Role Type Definitions:

**Data Scientist**:
- Core work: Statistical modeling, exploratory analysis, hypothesis testing, generating insights
- Deliverables: Models, analysis reports, visualizations, recommendations
- Focus: Understanding data and answering business questions
- Tools: Python/R, SQL, Jupyter, pandas, scikit-learn, matplotlib

**ML Engineer**:
- Core work: Production ML systems, model deployment, scalable inference, MLOps
- Deliverables: Production-grade ML services, APIs, pipelines, monitoring systems
- Focus: Building and maintaining ML systems at scale
- Tools: Python, ML frameworks, Docker, Kubernetes, cloud platforms, CI/CD

**Data Engineer**:
- Core work: Data pipelines, ETL, data infrastructure, data architecture
- Deliverables: Reliable data pipelines, data warehouses, data quality systems
- Focus: Making data available and reliable for analysts/scientists
- Tools: SQL, Spark, Airflow, dbt, Kafka, cloud data platforms

**Research Scientist**:
- Core work: Novel algorithm development, experimental methods, publications, theory
- Deliverables: Research papers, new algorithms, prototypes, patents
- Focus: Advancing state-of-the-art, scientific contribution
- Tools: Python/R, ML frameworks, math/statistics tools, LaTeX

**Analytics Engineer**:
- Core work: Analytics pipelines, metric definition, BI development, data modeling
- Deliverables: Dashboards, metrics, data models, reporting systems
- Focus: Making data accessible for business decision-making
- Tools: SQL, dbt, BI tools (Tableau/Looker), data warehouses

**ML Platform Engineer**:
- Core work: ML infrastructure, tooling, platforms for other ML practitioners
- Deliverables: ML platforms, feature stores, model registries, training infrastructure
- Focus: Enabling other ML teams to be productive
- Tools: Kubernetes, cloud platforms, distributed systems, ML frameworks

#### How to Assess:

1. **Read JD responsibilities** carefully - what will they do daily?
2. **Read resume responsibilities** - what have they been doing?
3. **Compare functions**, not titles
4. **Consider transferability** - can skills transfer with minimal training?

#### Example Assessments:

| Resume Role | JD Role | Score | Reasoning |
|------------|---------|-------|-----------|
| ML Engineer | ML Engineer | 3 | Same function |
| Data Scientist | ML Engineer | 2 | Adjacent - DS does modeling, needs to learn production/deployment |
| Software Engineer (backend) | ML Engineer | 2 | Adjacent - has production systems experience, needs to learn ML specifics |
| Research Scientist | ML Engineer | 1 | Some overlap - both use ML, but research≠production |
| Data Engineer | Data Scientist | 1 | Some overlap - both work with data, very different focus |
| Data Analyst | Data Scientist | 2 | Adjacent - analyst does SQL/BI, can grow into modeling |
| Web Developer | ML Engineer | 0 | Different - no ML or data experience |

#### Rationale Requirements:
- Describe resume role type and responsibilities
- Describe JD role type and responsibilities
- Assess alignment with specific reasoning

---

## 🎯 ATS CATEGORY THRESHOLDS

### Scoring Ranges:

**✅ ATS Pass (24-30 points)** - 80%+ match
- **Meaning**: Strong resume-to-JD match
- **Likelihood**: High probability of passing automated screening
- **Interpretation**: Resume demonstrates clear qualifications
- **Action**: Forward to human review
- **Example**: 25/30 = Strong technical fit, minor gaps acceptable

**⚠️ ATS Borderline (17-23 points)** - 57-80% match
- **Meaning**: Moderate match with some notable gaps
- **Likelihood**: May pass ATS depending on candidate pool
- **Interpretation**: Some qualifications missing but not completely disqualifying
- **Action**: Conditional - worth applying if other factors are strong (Phase 2)
- **Example**: 20/30 = Half the technical skills, but good projects and education

**❌ ATS Reject (0-16 points)** - <57% match
- **Meaning**: Poor match with significant gaps
- **Likelihood**: Likely to be filtered out by ATS
- **Interpretation**: Missing too many key requirements
- **Action**: Low probability of human review, likely automatic rejection
- **Example**: 12/30 = Weak across multiple dimensions

---

## 📋 SCORING PRINCIPLES

### 1. Be Objective
- Only count what's **explicitly** on the resume
- No assumptions about candidate's potential
- No credit for "might know" or "probably can learn"
- If it's not written, it doesn't exist for ATS purposes

### 2. No Inference Beyond Resume
- Don't assume related skills
- Don't give credit for "obvious" extensions
- Don't assume tool proficiency from job titles
- Example: "Data Scientist" title ≠ automatic Python skills unless Python is listed

### 3. Context Matters

**Career Transitioners**:
- Count years in **target field only**, not total career
- Note the transition in rationale
- Don't penalize for diverse background if target field experience is clear

**Tool Equivalence**:
- Give credit for close substitutes (PyTorch ≈ TensorFlow)
- Don't give credit for distant alternatives (Excel ≠ Spark)
- When in doubt, score conservatively

**Role Type vs Title**:
- Focus on **responsibilities and deliverables**, not job titles
- "Senior" title with junior responsibilities = score as junior
- IC title with team leadership = score based on actual level

### 4. Conservative Scoring
- When in doubt, score **lower**
- ATS systems are strict - replicate that strictness
- Borderline cases: round down, not up
- Better to underestimate than overestimate

### 5. Document Everything
- List specific gaps to inform Phase 2
- Note strengths to help with application strategy
- Provide evidence for scores
- Help candidate understand what's missing

---

## ✅ RATIONALE BEST PRACTICES

### What Makes a Good Rationale:

**For Technical Capabilities**:
- ✅ "Resume lists: regression, classification, clustering, time series. JD needs: regression, classification, NLP, reinforcement learning. Match: 2/4 core methods + extras. Missing: NLP, RL. Score: 4/6"
- ❌ "Has some ML skills but not all" (too vague)

**For Technology Stack**:
- ✅ "Resume: Python, scikit-learn, AWS. JD: Python, PyTorch, GCP, Docker. Match: Python ✓, AWS≈GCP ✓. Missing: PyTorch (has scikit-learn but not same), Docker. Score: 2/4"
- ❌ "Mostly matches tech stack" (not specific)

**For Years of Experience**:
- ✅ "Resume shows 3 years in ML (note: 8 years total as SWE prior). JD needs 3-5 years ML. Match: meets minimum. Score: 3/4"
- ❌ "Has enough experience" (doesn't explain transitioner context)

**For Seniority Match**:
- ✅ "Resume shows mid-level responsibilities: 'Led 2-person team, deployed 3 models independently, made technical decisions.' JD expects mid-level. Score: 3/4"
- ❌ "Title says Senior but seems more mid" (needs evidence)

---

## 📝 Example Scoring

### Example 1: Strong Pass

**Job**: Mid-Level ML Engineer, 3-5yr experience, Python/PyTorch/AWS, production ML systems

**Resume**: 
- 4yr ML experience
- Python, TensorFlow, GCP
- Deployed 3 ML models to production
- Master's CS
- Healthcare ML projects

**Scores**:
- Technical Capabilities: 5/6 (strong methods, all present)
- Technology Stack: 3/4 (Python ✓, TensorFlow≈PyTorch, GCP≈AWS, but missing some MLOps tools)
- Applied Experience: 3/3 (production ML systems ✓)
- Years Experience: 3/4 (4yr meets 3-5yr requirement)
- Seniority Match: 3/4 (mid-level for mid-level)
- Domain: 2/3 (healthcare vs general - adjacent)
- Education: 3/3 (Master's CS matches)
- Role Type: 3/3 (ML Engineer for ML Engineer)

**Total**: 25/30 → ✅ **ATS Pass**

**Rationale**: Strong technical fit despite domain mismatch. Would likely pass ATS based on keywords and experience match.

---

### Example 2: Borderline

**Job**: Senior Data Scientist, 5+ years, Python/R/SQL, healthcare experience required

**Resume**:
- 3yr Data Science
- Python, SQL (no R)
- Fintech experience
- Bachelor's Statistics

**Scores**:
- Technical Capabilities: 4/6 (key methods covered, some gaps)
- Technology Stack: 2/4 (Python ✓, SQL ✓, missing R)
- Applied Experience: 2/3 (DS work but different domain)
- Years Experience: 1/4 (3yr vs 5+ requirement - significantly below)
- Seniority Match: 2/4 (mid-level resume for senior role - one level off)
- Domain: 1/3 (fintech vs healthcare - minimal overlap)
- Education: 2/3 (Bachelor's for Senior role that may prefer Master's)
- Role Type: 3/3 (DS for DS)

**Total**: 17/30 → ⚠️ **ATS Borderline**

**Rationale**: Moderate fit with notable gaps in experience, seniority, and domain. Might pass ATS depending on competition, but not ideal match.

---

### Example 3: Reject

**Job**: ML Engineer, 3yr+ experience, production ML systems, Python/TensorFlow/Kubernetes

**Resume**:
- 1yr Data Analyst
- SQL, Excel, Tableau
- BI dashboards
- Bachelor's Business

**Scores**:
- Technical Capabilities: 1/6 (minimal ML methods)
- Technology Stack: 0/4 (SQL only, none of the ML tools)
- Applied Experience: 0/3 (BI dashboards, not ML systems)
- Years Experience: 1/4 (1yr vs 3yr+ - significantly below)
- Seniority Match: 1/4 (junior analyst for mid-level engineer - two levels off)
- Domain: 0/3 (no relevant domain shown)
- Education: 1/3 (non-technical degree)
- Role Type: 0/3 (Analyst for Engineer - different function)

**Total**: 4/30 → ❌ **ATS Reject**

**Rationale**: Poor match across all dimensions. Resume shows BI/analytics work, not ML engineering. Would be filtered out by ATS.

---

## 🔄 Using This Rubric

### For Scoring AI/LLM:
1. Read JD carefully for requirements
2. Read resume objectively
3. Score each dimension using criteria above
4. Document gaps and strengths
5. Calculate total and assign category
6. Write 2-3 sentence summary

### For Candidates:
1. Use this to **gap analysis** your resume
2. Identify which dimensions you're weak in
3. Update resume to highlight relevant experience
4. Add missing keywords/tools where truthful
5. Reframe experience to match target role type

### For Phase 2 (Human Review):
- Use ATS score as **baseline**
- Adjust for personal preferences and fit
- Consider factors ATS can't see
- Make final application decision

---

## 📈 Validation Results (October 2025)

This rubric was validated against **19 real ML/DS/AI job postings** with the following results:

### Score Distribution:
- ✅ **Pass (25-30)**: 0 jobs (0%)
- ⚠️ **Borderline (20-24)**: 13 jobs (68%)
- ⚠️ **Borderline (17-19)**: 5 jobs (26%)
- ❌ **Reject (0-16)**: 1 job (5%)

### Key Findings:

**Common Patterns**:
1. **Seniority Mismatch**: 18/19 jobs (95%) scored 0/4 on seniority due to Level 3 Lead candidate (15+ years total) applying to Level 0 Junior/Level 1 Mid roles (2-5 years required)
2. **Strong Technical Fit**: Most jobs scored 12-13/13 on Technical Assessment (92-100%)
3. **Domain Gaps**: Varied by industry - specialized fields (meteorology, defense) scored lower

**Rejected Job**:
- **AccuWeather Data Scientist II** (Score: 16/30)
- Reason: Highly specialized meteorology domain + missing domain-specific tools (Spark, Hadoop, meteorological algorithms)

**Critical Bug Fixed**:
- **10+ year requirement bug**: LLM was incorrectly counting total career years (15) as ML years for "10+ years ML experience" requirements
- **Fix**: Added "CRITICAL FOR ALL REQUIREMENTS (INCLUDING 10+)" section to prompt
- **Result**: Now correctly counts only target field years (e.g., 2 years ML ÷ 10 years required = 0.2x → Score 1)
- **Validated**: Comcast job (10+ years ML required) now correctly scores 22/30 (Borderline) instead of false positive ~27/30 (Pass)

**Rationale Quality Improvements**:
1. All rationales now use explicit "MUST cite" formats with evidence
2. Technical Capabilities uses `✅ Methods: [list]. ⚠️ Partial: [list]. ❌ Missing: [list]`
3. Technology Stack uses `"Resume has X, Y, Z; JD needs A, B, C → Score N/4"`
4. Years and Seniority have completely separate rationales (no merging)
5. Education correctly scores exceeding requirements as positive (Master's for Bachelor's = 3/3)
6. ATS Summary includes dimensional breakdown pattern

### Scoring Accuracy:
- ✅ Technical assessment: Highly accurate
- ✅ Years calculation: Fixed and accurate (including 10+ edge case)
- ✅ Seniority separation: Working as designed
- ✅ Education consistency: Fixed (exceeding = positive)
- ✅ Domain assessment: Accurate with clear gaps noted

---

**End of Rubric**
