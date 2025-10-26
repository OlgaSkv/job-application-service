"""
Job Tracker Streamlit Dashboard
Simple table view with clickable JSON details
"""

import streamlit as st
import pandas as pd
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="Job Application Service - AI Resume Screening",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🎯 Job Application Service - Processed Jobs Summary</p>', unsafe_allow_html=True)

# Helper functions
@st.cache_data(ttl=10)
def load_latest_summary():
    """Load the most recent summary CSV file and batch statistics."""
    reports_dir = Path("reports")
    if not reports_dir.exists():
        return None
    
    summary_files = list(reports_dir.glob("*/summary_*.csv"))
    if not summary_files:
        return None
    
    latest_file = max(summary_files, key=lambda p: p.stat().st_mtime)
    
    try:
        df = pd.read_csv(latest_file, parse_dates=['date_saved'])
        report_dir = latest_file.parent
        
        # Try to load batch statistics
        batch_stats = None
        # Find matching batch_stats file (same timestamp as summary)
        timestamp = latest_file.stem.replace("summary_", "")
        batch_stats_file = report_dir / f"batch_stats_{timestamp}.json"
        if batch_stats_file.exists():
            try:
                with open(batch_stats_file, 'r', encoding='utf-8') as f:
                    batch_stats = json.load(f)
            except Exception as e:
                st.warning(f"Could not load batch statistics: {e}")
        
        return df, latest_file, report_dir, batch_stats
    except Exception as e:
        st.error(f"Error loading summary: {e}")
        return None

def find_json_file(job_uid, report_dir):
    """Find the flat_report JSON file for a given job_uid."""
    jobs_dir = report_dir / "jobs"
    if not jobs_dir.exists():
        return None
    
    job_dir = jobs_dir / job_uid
    if job_dir.exists():
        # Prefer flat_report.json as it has all the data
        flat_report = job_dir / f"{job_uid}_flat_report.json"
        if flat_report.exists():
            return flat_report
        
        # Fallback to any JSON file
        json_files = list(job_dir.glob("*.json"))
        if json_files:
            return json_files[0]
    
    return None

def load_job_json(json_path):
    """Load and return job JSON data."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
        return None

def process_single_job(job_uid):
    """Process a single job by UID using the process_jobs.py script."""
    with st.spinner(f"🔄 Processing job {job_uid}..."):
        try:
            result = subprocess.run(
                ["python", "scripts/process_jobs.py", "--uids", job_uid],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                st.success(f"✅ Successfully processed job {job_uid}")
                st.balloons()
                st.expander("📋 View Processing Log").code(result.stdout, language="text")
                st.cache_data.clear()
                time.sleep(1)
                st.rerun()
            else:
                error_output = result.stderr or result.stdout
                
                # Interpret exit codes
                if result.returncode == 2:
                    st.error(f"❌ Job with UID '{job_uid}' not found in database")
                elif result.returncode == 1:
                    # Check if it's a parsing/processing error
                    if "failed to process" in error_output.lower() or "[ERROR]" in error_output:
                        st.error(f"⚠️ Job {job_uid} was found but encountered errors during processing")
                    else:
                        st.error(f"❌ Error processing job {job_uid}")
                else:
                    st.error(f"❌ Unexpected error (exit code {result.returncode})")
                
                st.expander("🔍 Error Details").code(error_output, language="text")
                
        except subprocess.TimeoutExpired:
            st.error(f"⏱️ Processing timed out for job {job_uid}")
        except Exception as e:
            st.error(f"❌ Error running process_jobs.py: {e}")

def display_json_details(job_data):
    """Display job JSON data in a structured way."""
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "📊 ATS Scores", "💼 Job Description", "📄 Raw JSON"])
    
    with tab1:
        # Job title as hyperlink
        if job_data.get('job_url'):
            st.markdown(
                f'### <a href="{job_data.get("job_url")}" target="_blank" style="text-decoration:none;">{job_data.get("role", "Job Role")}</a>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"### {job_data.get('role', 'Job Role')}")
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Job Information")
            st.write(f"**Company:** {job_data.get('company', 'N/A')}")
            st.write(f"**Location:** {job_data.get('location', 'Remote' if job_data.get('work_model') == 'Remote' else 'N/A')}")
            st.write(f"**Employment Type:** {job_data.get('employment_type', 'N/A')}")
            st.write(f"**Seniority:** {job_data.get('seniority', 'N/A')}")
            st.write(f"**Compensation:** {job_data.get('compensation', 'N/A')}")
            st.write(f"**Work Model:** {job_data.get('work_model', 'N/A')}")
            st.write(f"**Years Experience:** {job_data.get('years_experience', 'N/A')}")
        
        with col2:
            st.markdown("### Status")
            st.write(f"**Eligible:** {'✅ Yes' if job_data.get('eligible') else '❌ No'}")
            st.write(f"**Decision:** {job_data.get('decision', 'N/A')}")
            st.write(f"**ATS Score:** {job_data.get('ats_total_score', 'N/A')}/30")
            st.write(f"**Category:** {job_data.get('ats_category', 'N/A')}")
            st.write(f"**Date Saved:** {job_data.get('date_saved', 'N/A')}")
        
        # Blockers
        if job_data.get('hard_blockers'):
            st.markdown("### 🚫 Hard Blockers")
            st.error(job_data['hard_blockers'])
        
        if job_data.get('soft_blockers'):
            st.markdown("### ⚠️ Soft Blockers")
            st.warning(job_data['soft_blockers'])
    
    with tab2:
        # ATS Total Score
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total ATS Score", f"{job_data.get('ats_total_score', 'N/A')}/30")
        with col2:
            st.metric("Category", job_data.get('ats_category', 'N/A'))
        with col3:
            st.metric("Eligible", "✅ Yes" if job_data.get('eligible') else "❌ No")
        
        st.divider()
        
        # Detailed Score Breakdown
        st.markdown("### � ATS Score Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Technical Skills (13 points)")
            st.metric("Technical Capabilities", f"{job_data.get('technical_capabilities_score', 'N/A')}/6")
            st.caption(job_data.get('technical_capabilities_rationale', 'N/A'))
            
            st.metric("Technology Stack", f"{job_data.get('technology_stack_score', 'N/A')}/3")
            st.caption(job_data.get('technology_stack_rationale', 'N/A'))
            
            st.metric("Applied Experience", f"{job_data.get('applied_experience_score', 'N/A')}/3")
            st.caption(job_data.get('applied_experience_rationale', 'N/A'))
            
            st.metric("Domain Knowledge", f"{job_data.get('domain_score', 'N/A')}/2")
            st.caption(job_data.get('domain_rationale', 'N/A'))
        
        with col2:
            st.markdown("#### Experience & Background (17 points)")
            st.metric("Years of Experience", f"{job_data.get('years_experience_score', 'N/A')}/3")
            st.caption(job_data.get('years_experience_rationale', 'N/A'))
            
            st.metric("Seniority Match", f"{job_data.get('seniority_match_score', 'N/A')}/5")
            st.caption(job_data.get('seniority_match_rationale', 'N/A'))
            
            st.metric("Role Type Match", f"{job_data.get('role_type_score', 'N/A')}/3")
            st.caption(job_data.get('role_type_rationale', 'N/A'))
            
            st.metric("Education", f"{job_data.get('education_score', 'N/A')}/3")
            st.caption(job_data.get('education_rationale', 'N/A'))
        
        st.divider()
        
        # Summary
        st.markdown("### 📝 ATS Summary")
        st.info(job_data.get('ats_summary', 'N/A'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💪 Strengths")
            strengths = job_data.get('strengths', [])
            if isinstance(strengths, list) and strengths:
                for strength in strengths:
                    st.markdown(f"- {strength}")
            else:
                st.write(strengths or "None identified")
        
        with col2:
            st.markdown("### ⚠️ Technical Gaps")
            gaps = job_data.get('technical_gaps', [])
            if isinstance(gaps, list) and gaps:
                for gap in gaps:
                    st.markdown(f"- {gap}")
            else:
                st.write(gaps or "None identified")
        
        # Skills
        st.divider()
        st.markdown("### 🎯 Skills Match")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Skills Required:**")
            required_skills = job_data.get('skills_required', [])
            if isinstance(required_skills, list) and required_skills:
                st.write(", ".join(required_skills))
            else:
                st.write("None specified")
        
        with col2:
            st.markdown("**Skills for ATS:**")
            ats_skills = job_data.get('skills_for_ats', [])
            if isinstance(ats_skills, list) and ats_skills:
                st.write(", ".join(ats_skills))
            else:
                st.write("None identified")
    
    with tab3:
        st.markdown("### Job Description")
        jd = job_data.get('job_description', '')
        if jd:
            st.text_area("Full Job Description", jd, height=400)
        else:
            st.write("No job description available")
    
    with tab4:
        st.markdown("### Raw JSON Data")
        st.json(job_data)

# Sidebar
with st.sidebar:
    st.header("⚙️ Job Processing")
    
    # Process by Date
    st.subheader("📅 Process by Date")
    col1, col2 = st.columns(2)
    with col1:
        date_from = st.date_input(
            "From Date",
            value=datetime.now() - timedelta(days=30),
            help="Process jobs from this date onwards"
        )
    with col2:
        date_to = st.date_input(
            "To Date",
            value=datetime.now(),
            help="Process jobs up to this date"
        )
    
    limit = st.number_input("Max Jobs", min_value=1, max_value=100, value=10, step=1)
    unprocessed_only = st.checkbox("Unprocessed only", value=True)
    
    if st.button("� Process by Date", type="primary", use_container_width=True):
        with st.spinner("Processing jobs..."):
            cmd = ["python", "scripts/process_jobs.py", "--limit", str(limit)]
            
            if unprocessed_only:
                cmd.append("--unprocessed")
            else:
                cmd.extend(["--date-from", date_from.strftime("%Y-%m-%d")])
                cmd.extend(["--date-to", date_to.strftime("%Y-%m-%d")])
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
                
                if result.returncode == 0:
                    st.success("✅ Processing complete!")
                    st.balloons()
                    st.expander("📋 View Processing Log").code(result.stdout, language="text")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
                elif result.returncode == 2:
                    st.warning("⚠️ No jobs found matching the specified criteria")
                    st.expander("📋 Details").code(result.stderr or result.stdout, language="text")
                elif result.returncode == 1:
                    error_output = result.stderr or result.stdout
                    if "failed to process" in error_output.lower() or "[ERROR]" in error_output:
                        st.error("⚠️ Some jobs encountered errors during processing")
                        st.info("Jobs may have been partially processed. Check the reports directory.")
                    else:
                        st.error("❌ Processing failed")
                    st.expander("🔍 Error Details").code(error_output, language="text")
                else:
                    st.error(f"❌ Unexpected error (exit code {result.returncode})")
                    st.expander("🔍 Error Details").code(result.stderr or result.stdout, language="text")
            except subprocess.TimeoutExpired:
                st.error("⏱️ Processing timed out (>10 minutes)")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # Process by UID
    st.subheader("🎯 Process by UID")
    uid_input = st.text_input(
        "Job UID",
        placeholder="e.g., tAj0c",
        help="Enter the 5-character job UID"
    )
    
    if st.button("🎯 Process by UID", type="secondary", use_container_width=True, disabled=not uid_input):
        if uid_input:
            process_single_job(uid_input.strip())
    
    st.divider()
    
    st.subheader("📊 System Info")
    reports_dir = Path("reports")
    if reports_dir.exists():
        date_dirs = [d for d in reports_dir.iterdir() if d.is_dir()]
        st.metric("Report Dates", len(date_dirs))
        
        total_jobs = 0
        for date_dir in date_dirs:
            jobs_dir = date_dir / "jobs"
            if jobs_dir.exists():
                total_jobs += len([d for d in jobs_dir.iterdir() if d.is_dir()])
        st.metric("Total Jobs Processed", total_jobs)

# Main content
data = load_latest_summary()

if data is None:
    st.info("👋 No data yet! Use the sidebar to process some jobs.")
    st.markdown("""
    ### Getting Started:
    1. Click **Process Jobs** in the sidebar
    2. Select date range or use 'Unprocessed only'
    3. Click 🚀 **Process Jobs** button
    4. Wait for processing to complete
    5. View results here!
    """)
else:
    df, summary_file, report_dir, batch_stats = data
    
    # Show data timestamp and description
    st.info("📊 **Viewing the last successfully processed batch of jobs.** Use the sidebar to process new jobs or specific UIDs.")
    st.caption(f"📅 Data from: {summary_file.name} (Last updated: {datetime.fromtimestamp(summary_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')})")
    
    # Display batch processing statistics if available
    if batch_stats:
        with st.expander("⏱️ Batch Processing Statistics", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Processing Time", f"{batch_stats.get('total_time_seconds', 0):.1f}s")
                st.metric("Jobs Processed", batch_stats.get('total_jobs_processed', 0))
            
            with col2:
                st.metric("Eligible Jobs", batch_stats.get('eligible_jobs', 0))
                st.metric("Ineligible Jobs", batch_stats.get('ineligible_jobs', 0))
            
            with col3:
                st.metric("Avg Time (All)", f"{batch_stats.get('avg_time_all_jobs', 0):.1f}s")
                if batch_stats.get('avg_time_eligible_jobs'):
                    st.metric("Avg Time (Eligible)", f"{batch_stats.get('avg_time_eligible_jobs', 0):.1f}s")
            
            with col4:
                if batch_stats.get('fastest_eligible_job'):
                    st.metric("Fastest Job", f"{batch_stats.get('fastest_eligible_job', 0):.1f}s")
                if batch_stats.get('slowest_eligible_job'):
                    st.metric("Slowest Job", f"{batch_stats.get('slowest_eligible_job', 0):.1f}s")
            
            # Show ineligible jobs details
            ineligible_details = batch_stats.get('ineligible_jobs_details', [])
            if ineligible_details:
                st.divider()
                st.markdown("### 🚫 Ineligible Jobs Details")
                for job in ineligible_details:
                    with st.container():
                        st.markdown(f"**{job.get('job_uid')}** - {job.get('company')} - {job.get('role')}")
                        if job.get('hard_blockers'):
                            st.error(f"❌ Hard Blockers: {', '.join(job['hard_blockers'])}")
                        if job.get('soft_blockers'):
                            st.warning(f"⚠️ Soft Blockers: {', '.join(job['soft_blockers'])}")
                        if job.get('notes'):
                            st.info(f"📝 {job['notes']}")
                        st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Jobs", len(df))
    
    with col2:
        if 'ats_total_score' in df.columns:
            avg_score = df['ats_total_score'].mean()
            st.metric("Avg Score", f"{avg_score:.1f}/30")
    
    with col3:
        if 'ats_total_score' in df.columns:
            high_score = len(df[df['ats_total_score'] >= 24])
            st.metric("High Score (24+)", high_score)
    
    with col4:
        if 'eligible' in df.columns:
            eligible = len(df[df['eligible'] == True])
            st.metric("Eligible", eligible)
    
    with col5:
        if 'decision' in df.columns:
            applied = len(df[df['decision'] == 'APPLY'])
            st.metric("To Apply", applied)
    
    st.divider()
    
    # Bulk Actions
    st.subheader("⚡ Bulk Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Mark High Scores (>23) as APPLY", use_container_width=True):
            if 'ats_total_score' in df.columns:
                # Update decisions in the full dataframe
                mask = df['ats_total_score'] > 23
                df.loc[mask, 'decision'] = 'APPLY'
                count = mask.sum()
                
                # Save to CSV
                try:
                    df.to_csv(summary_file, index=False)
                    st.success(f"✅ Marked {count} jobs with score >23 as APPLY")
                    st.cache_data.clear()
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saving: {e}")
            else:
                st.warning("Score column not available")
    
    with col2:
        if st.button("❌ Mark Low Scores (<17) as PASS", use_container_width=True):
            if 'ats_total_score' in df.columns:
                # Update decisions in the full dataframe
                mask = df['ats_total_score'] < 17
                df.loc[mask, 'decision'] = 'PASS'
                count = mask.sum()
                
                # Save to CSV
                try:
                    df.to_csv(summary_file, index=False)
                    st.success(f"✅ Marked {count} jobs with score <17 as PASS")
                    st.cache_data.clear()
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saving: {e}")
            else:
                st.warning("Score column not available")
    
    with col3:
        if st.button("🔄 Clear All Decisions", use_container_width=True):
            # Clear all decisions in the full dataframe
            df['decision'] = ''
            
            # Save to CSV
            try:
                df.to_csv(summary_file, index=False)
                st.success("✅ All decisions cleared")
                st.cache_data.clear()
                time.sleep(0.5)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error saving: {e}")
    
    st.divider()
    
    # Filters
    st.subheader("🔍 Filter Jobs")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if 'ats_total_score' in df.columns:
            score_min = st.slider("Min ATS Score", 0, 30, 0)
        else:
            score_min = 0
    
    with col2:
        eligible_filter = st.selectbox("Eligibility", ["All", "Eligible Only", "Ineligible Only"])
    
    with col3:
        if 'ats_category' in df.columns:
            categories = ["All"] + sorted(df['ats_category'].dropna().unique().tolist())
            category_filter = st.selectbox("ATS Category", categories)
        else:
            category_filter = "All"
    
    with col4:
        decision_filter = st.selectbox("Decision", ["All", "APPLY", "PASS", "No Decision"])
    
    with col5:
        if 'company' in df.columns:
            companies = ["All"] + sorted(df['company'].dropna().unique().tolist())
            company_filter = st.selectbox("Company", companies)
        else:
            company_filter = "All"
    
    # Apply filters
    filtered_df = df.copy()
    
    # Apply eligibility filter first
    if eligible_filter == "Eligible Only" and 'eligible' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['eligible'] == True]
    elif eligible_filter == "Ineligible Only" and 'eligible' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['eligible'] == False]
    
    # Only apply score filter for eligible jobs (ineligible jobs don't have scores)
    if 'ats_total_score' in filtered_df.columns and eligible_filter != "Ineligible Only":
        filtered_df = filtered_df[filtered_df['ats_total_score'] >= score_min]
    
    if decision_filter != "All" and 'decision' in filtered_df.columns:
        if decision_filter == "No Decision":
            filtered_df = filtered_df[filtered_df['decision'].isna() | (filtered_df['decision'] == '')]
        else:
            filtered_df = filtered_df[filtered_df['decision'] == decision_filter]
    
    if category_filter != "All" and 'ats_category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['ats_category'] == category_filter]
    
    if company_filter != "All":
        filtered_df = filtered_df[filtered_df['company'] == company_filter]
    
    st.divider()
    st.subheader(f"📋 Jobs Table ({len(filtered_df)} of {len(df)} jobs)")
    
    # Sorting options
    col1, col2 = st.columns([1, 3])
    with col1:
        sort_by_score = st.checkbox(
            "Sort by ATS Score (High to Low)",
            value=True,
            help="Show highest scoring jobs first to prioritize applications"
        )
    with col2:
        st.write("")  # Spacer
    
    # Apply sorting by ATS score
    if sort_by_score and 'ats_total_score' in filtered_df.columns:
        filtered_df = filtered_df.sort_values('ats_total_score', ascending=False)
    
    # Column selection
    col1, col2 = st.columns([1, 3])
    with col1:
        show_all_columns = st.checkbox("Show all columns", value=False, help="Display all available columns with horizontal scroll")
    with col2:
        if not show_all_columns:
            st.caption("💡 Enable 'Show all columns' to see every field with horizontal scrolling")
    
    # Columns to always exclude (JSON file paths and linkedin URL)
    exclude_columns = ['linkedin_url', 'parsed_jd_json', 'eligibility_report_json', 'ats_score_json', 'flat_report_json', 'full_state_json']
    
    # Select columns to display
    if show_all_columns:
        # Show ALL columns except excluded ones
        display_columns = [col for col in filtered_df.columns if col not in exclude_columns]
    else:
        # Show first 10 key columns by default
        default_columns = ['job_uid', 'date_saved', 'decision', 'company', 'role', 'job_url', 'job_description', 'ats_total_score', 'ats_category', 'eligible']
        display_columns = [col for col in default_columns if col in filtered_df.columns]
    
    # Display table with selection
    st.markdown("**💡 Edit decisions directly in the table below, then click Save.**")
    st.caption("To view full job details (JSON), use the dropdown selector after the table.")
    
    # Display info about columns
    st.caption(f"📊 Showing {len(display_columns)} columns. Use horizontal scroll below to see all fields. Total columns available: {len(filtered_df.columns)}")
    
    # Prepare editable dataframe - only include selected columns
    edit_df = filtered_df[display_columns].copy()
    
    # CRITICAL: Ensure decision column is string type to prevent float conversion errors
    if 'decision' in edit_df.columns:
        edit_df['decision'] = edit_df['decision'].fillna('').astype(str)
        # Replace 'nan' string with empty string
        edit_df['decision'] = edit_df['decision'].replace('nan', '')
    
    # Build column config dynamically based on displayed columns
    column_config = {}
    
    if "job_uid" in edit_df.columns:
        column_config["job_uid"] = st.column_config.TextColumn("Job UID", width="small", disabled=True)
    if "date_saved" in edit_df.columns:
        column_config["date_saved"] = st.column_config.DateColumn(
            "Date Saved", 
            width="small", 
            disabled=True,
            format="MMM DD, YYYY"  # e.g., "Oct 17, 2025"
        )
    if "decision" in edit_df.columns:
        column_config["decision"] = st.column_config.SelectboxColumn(
            "Decision",
            width="small",
            options=["", "APPLY", "PASS"],
            required=False,
            help="APPLY = will apply | PASS = skip this job | (empty) = not decided yet"
        )
    if "company" in edit_df.columns:
        column_config["company"] = st.column_config.TextColumn("Company", width="medium", disabled=True)
    if "role" in edit_df.columns:
        column_config["role"] = st.column_config.TextColumn("Role", width="medium", disabled=True)
    if "job_url" in edit_df.columns:
        column_config["job_url"] = st.column_config.LinkColumn("Job URL", width="small", disabled=True)
    if "job_description" in edit_df.columns:
        column_config["job_description"] = st.column_config.TextColumn("Job Description", width="large", disabled=True)
    if "ats_total_score" in edit_df.columns:
        column_config["ats_total_score"] = st.column_config.NumberColumn("Score", width="small", disabled=True, format="%.1f")
    if "location" in edit_df.columns:
        column_config["location"] = st.column_config.TextColumn("Location", width="medium", disabled=True)
    if "ats_category" in edit_df.columns:
        column_config["ats_category"] = st.column_config.TextColumn("Category", width="medium", disabled=True)
    if "eligible" in edit_df.columns:
        column_config["eligible"] = st.column_config.CheckboxColumn("Eligible", width="small", disabled=True)
    
    # Use data_editor for inline editing with dropdown for decision
    edited_data = st.data_editor(
        edit_df,
        use_container_width=True,
        height=500,
        hide_index=True,
        column_config=column_config,
        disabled=list(set(edit_df.columns) - {"decision"}),  # Only allow editing decision column
        key="job_table"
    )
    
    # Save buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Changes", type="secondary", use_container_width=True):
            # Update the main dataframe with edited decisions
            # Match edited_data back to df by job_uid and update the decision column
            for idx, row in edited_data.iterrows():
                job_uid = row['job_uid']
                new_decision = row.get('decision', '')
                # Convert new_decision to string to ensure type consistency
                new_decision = str(new_decision) if new_decision is not None else ''
                # Find the row in df with matching job_uid and update its decision
                df.loc[df['job_uid'] == job_uid, 'decision'] = new_decision
            
            try:
                # Ensure decision column is string type before saving
                df['decision'] = df['decision'].astype(str)
                df.to_csv(summary_file, index=False)
                changes_count = len(edited_data[edited_data['decision'].notna() & (edited_data['decision'] != '')])
                st.success(f"✅ All decisions saved! ({changes_count} jobs with decisions)")
                st.info(f"📁 Saved to: `{summary_file}`")
                st.cache_data.clear()
                time.sleep(0.5)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error saving: {e}")
    
    with col2:
        st.empty()  # Spacer
    
    with col3:
        if st.button("🚀 Save & Finalize Decisions", type="primary", use_container_width=True):
            # First, save the changes
            for idx, row in edited_data.iterrows():
                job_uid = row['job_uid']
                new_decision = row.get('decision', '')
                # Convert new_decision to string to ensure type consistency
                new_decision = str(new_decision) if new_decision is not None else ''
                df.loc[df['job_uid'] == job_uid, 'decision'] = new_decision
            
            try:
                # Ensure decision column is string type before saving
                df['decision'] = df['decision'].astype(str)
                df.to_csv(summary_file, index=False)
                st.success(f"✅ Decisions saved to CSV")
                st.cache_data.clear()
                
                # Then run finalize_decisions.py with the CSV file path
                with st.spinner("📤 Uploading to Google Sheets and marking jobs as processed..."):
                    result = subprocess.run(
                        ["python", "scripts/finalize_decisions.py", "--csv", str(summary_file)],
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    # Handle exit codes:
                    # 0 = Success (jobs uploaded/marked)
                    # 1 = No APPLY or PASS decisions found
                    # 2 = Jobs found but failed to process
                    
                    if result.returncode == 0:
                        st.success("✅ Decisions finalized and uploaded to Google Sheets!")
                        st.balloons()
                        st.expander("📋 View Finalization Log").code(result.stdout, language="text")
                        time.sleep(1)
                        st.rerun()
                    elif result.returncode == 1:
                        st.warning("⚠️ No APPLY or PASS decisions found to process")
                        st.info("💡 Mark some jobs as APPLY or PASS, then save and finalize.")
                        st.expander("📋 View Details").code(result.stdout + "\n" + result.stderr, language="text")
                    elif result.returncode == 2:
                        st.error("❌ Jobs were found but failed to process")
                        st.expander("🔍 Error Details").code(result.stderr or result.stdout, language="text")
                    else:
                        st.error(f"❌ Unexpected error (exit code: {result.returncode})")
                        st.expander("🔍 Error Details").code(result.stderr or result.stdout, language="text")
                        
            except subprocess.TimeoutExpired:
                st.error("⏱️ Finalization timed out (>5 minutes)")
            except Exception as e:
                st.error(f"❌ Error during finalization: {e}")
    
    # Handle row selection for viewing JSON
    st.divider()
    st.subheader("📄 View Job Details")
    
    # Create a mapping for display
    def format_job_option(uid):
        if not uid:
            return "Choose a job..."
        # Use the full df to ensure we can always find the job
        job_row = df[df['job_uid'] == uid]
        if len(job_row) > 0:
            company = job_row['company'].values[0]
            role = job_row['role'].values[0]
            return f"{uid} - {company} - {role}"
        return uid
    
    selected_uid = st.selectbox(
        "Select a job to view details:",
        options=[""] + filtered_df['job_uid'].tolist(),
        format_func=format_job_option,
        key="job_selector"
    )
    
    if selected_uid:
        # Find and load JSON
        json_path = find_json_file(selected_uid, report_dir)
        
        if json_path:
            st.caption(f"📂 Loading: {json_path.name}")
            job_data = load_job_json(json_path)
            
            if job_data:
                display_json_details(job_data)
            else:
                st.error("Failed to load JSON data")
        else:
            st.warning(f"JSON file not found for job_uid: {selected_uid}")
            
            # Show process button for jobs without JSON
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🔄 Process This Job", key=f"process_{selected_uid}"):
                    process_single_job(selected_uid)
    else:
        st.info("👆 Select a job from the dropdown above to view full details")
    
    # Export button
    st.divider()
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Results as CSV",
        data=csv_data,
        file_name=f"job_tracker_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🎯 Job Tracker - AI-Powered Resume Screening System</p>
    <p>Built with LangChain, LangGraph, and OpenAI GPT-4o</p>
</div>
""", unsafe_allow_html=True)
