"""
process_jobs.py - Main job processing pipeline

Processes job postings from Google Sheets through the hybrid AI/rule-based workflow:
1. Queries jobs from JD_Saved sheet based on filters
2. Loads candidate documents from Google Drive
3. Runs each job through the LangGraph workflow:
   - JD Parser (LLM agent): Extracts structured data
   - Eligibility Checker (rule-based): Identifies hard/soft blockers
   - ATS Scorer (LLM agent): Evaluates 30-point resume fit
4. Saves individual job outputs as JSON files
5. Generates a summary CSV for manual review

Usage:
    python scripts/process_jobs.py --unprocessed
    python scripts/process_jobs.py --date-from 2025-10-15 --limit 10
    python scripts/process_jobs.py --uids JD-001 JD-002
"""

import json
import os
import sys
import csv
from datetime import datetime
import argparse
from dotenv import load_dotenv
import time

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.google_drive_tool import GoogleDriveTool
from src.tools.google_sheets_tool import GoogleSheetsTool
from src.graph.workflow import create_workflow
from src.utils.parser_utils import (
    normalize_job_url,
    get_job_portal_name,
    clean_job_description,
)
from src.utils.logging_utils import setup_logging
from src.utils.config_utils import get_config
import logging
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache

# Load environment variables from .env file
load_dotenv()

setup_logging()

# Enable LLM response caching for faster testing and cost savings
set_llm_cache(InMemoryCache())

# Load IDs and URLs from config.json
config = get_config()

CREDENTIALS_PATH = config["CREDENTIALS_PATH"]
RESUME_FILE_ID = config["RESUME_FILE_ID"]
STATEMENT_FILE_ID = config["STATEMENT_FILE_ID"]
PROFILE_FILE_PATH = config["PROFILE_FILE_PATH"]
JD_SAVED_URL = config["JD_SAVED_URL"]
JOB_TRACKER_URL = config["JOB_TRACKER_URL"]

# Fields that can appear in multiple agent outputs without triggering duplicate key warnings.
# These are identity/metadata fields that are expected to be consistent across all outputs.
ALLOWED_DUPLICATE_FIELDS = ["job_uid", "company", "role", "title", "job_url", "date_saved"]


def parse_arguments():
    """
    Parse command line arguments for job processing.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Process jobs from Google Sheets",
        epilog="""
Examples:
  Process all unprocessed jobs:
    python scripts/process_jobs.py --unprocessed
    
  Process all jobs (including already processed):
    python scripts/process_jobs.py --all
    
  Process jobs from a specific date range:
    python scripts/process_jobs.py --date-from 2025-10-15 --limit 10
    
  Process specific jobs by UID:
    python scripts/process_jobs.py --uids JD-001 JD-002 JD-003
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--all", action="store_true", help="Process all jobs (including already processed)"
    )
    parser.add_argument("--unprocessed", action="store_true", help="Process all unprocessed jobs")
    parser.add_argument("--date-from", type=str, help="Process jobs from date onwards (YYYY-MM-DD)")
    parser.add_argument("--date-to", type=str, help="Process jobs up to this date (YYYY-MM-DD)")
    parser.add_argument("--uids", nargs="+", help="Process specific jobs by UID")
    parser.add_argument("--limit", type=int, help="Limit number of jobs to process")

    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Validate mutually exclusive options
    if args.all and args.unprocessed:
        parser.error("--all and --unprocessed are mutually exclusive. Use one or the other.")

    return args


def build_query_kwargs(args):
    """
    Build query parameters dictionary from parsed arguments.

    Args:
        args: Parsed command line arguments

    Returns:
        dict: Query parameters for GoogleSheetsTool.query_jobs()
    """
    query_kwargs = {}

    # --all means no filter on parsed status (gets everything)
    # --unprocessed means only get unparsed jobs (parsed=False)
    # If neither is specified, other filters apply without parsed status filter
    if args.unprocessed:
        query_kwargs["parsed"] = False
    # Note: --all doesn't set parsed filter, so it gets all jobs

    if args.date_from:
        query_kwargs["date_from"] = args.date_from
    if args.date_to:
        query_kwargs["date_to"] = args.date_to
    if args.uids:
        query_kwargs["uids"] = args.uids
    if args.limit:
        query_kwargs["limit"] = args.limit
    return query_kwargs


def save_agent_outputs_and_flatten(result, uid, job_out_dir):
    """
    Save individual agent outputs as separate JSON files and create a flattened report.

    For each agent output (parsed_jd, eligibility_report, ats_score, etc.):
    1. Saves the output as a separate JSON file (e.g., JD-001_parsed_jd.json)
    2. Merges all fields into a single flat_report.json for easy access
    3. Warns about key conflicts (except for allowed duplicate fields)

    Args:
        result: Workflow state dictionary containing all agent outputs
        uid: Job UID for filename generation
        job_out_dir: Directory to save all output files

    Returns:
        tuple: (json_links dict with paths to all JSONs, full_report dict with merged data)

    Example:
        >>> result = {
        ...     "job_uid": "JD-001",
        ...     "parsed_jd": {"company": "Acme", "role": "Engineer", ...},
        ...     "eligibility_report": {"eligible": True, ...},
        ...     "ats_score": {"ats_total_score": 24, ...}
        ... }
        >>> links, report = save_agent_outputs_and_flatten(result, "JD-001", "./output/JD-001")
        >>> print(links.keys())
        dict_keys(['parsed_jd_json', 'eligibility_report_json', 'ats_score_json',
                   'flat_report_json', 'full_state_json'])
    """
    json_links = {}
    full_report = {}

    # Add core metadata fields first (from workflow state, not agent outputs)
    # Only save cleaned versions, not raw data
    core_metadata = {
        "job_uid": result.get("job_uid"),
        "date_saved": result.get("date_saved"),
        "job_url": result.get("job_url"),
        "job_portal": result.get("job_portal"),
        "job_description": result.get("job_description"),
    }
    full_report.update({k: v for k, v in core_metadata.items() if v is not None})

    for key in [
        "parsed_jd",
        "eligibility_report",
        "ats_score",
        "company_report",
        "coach_recommendation",
    ]:
        agent_output = result.get(key)
        if agent_output is not None:
            # Add job_uid as first property for consistency and traceability
            if "job_uid" not in agent_output:
                # Create new dict with job_uid first, then merge rest
                agent_output = {"job_uid": uid, **agent_output}
                # Update result dict with new ordered output
                result[key] = agent_output

            json_filename = f"{uid}_{key}.json"
            json_path = os.path.join(job_out_dir, json_filename)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(agent_output, f, ensure_ascii=False, indent=2)
            json_links[f"{key}_json"] = json_path
            for k, v in agent_output.items():
                if k not in full_report:
                    full_report[k] = v
                elif k not in ALLOWED_DUPLICATE_FIELDS:
                    logging.warning(
                        f"Key conflict for '{k}' in job {uid}; skipping duplicate from {key} output."
                    )
    # Save flat full_report
    flat_report_path = os.path.join(job_out_dir, f"{uid}_flat_report.json")
    with open(flat_report_path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, ensure_ascii=False, indent=2)
    json_links["flat_report_json"] = flat_report_path
    # Save full state as well
    full_state_path = os.path.join(job_out_dir, f"{uid}_full_state.json")
    with open(full_state_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    json_links["full_state_json"] = full_state_path
    return json_links, full_report


def main():
    """Main job processing pipeline."""
    # Load shared candidate documents
    drive_tool = GoogleDriveTool(credentials_path=CREDENTIALS_PATH)
    resume = drive_tool.load_doc(file_id=RESUME_FILE_ID)
    personal_statement = drive_tool.load_doc(file_id=STATEMENT_FILE_ID)

    # Load candidate profile from local JSON file
    profile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), PROFILE_FILE_PATH)
    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            candidate_profile = json.load(f)
        logging.info(f"✅ Loaded candidate profile from {profile_path}")
    except FileNotFoundError:
        logging.error(f"❌ Candidate profile not found at {profile_path}. Using empty profile.")
        candidate_profile = {}
    except json.JSONDecodeError as e:
        logging.error(f"❌ Error parsing candidate profile JSON: {e}. Using empty profile.")
        candidate_profile = {}

    # Load jobs to process
    sheets_tool = GoogleSheetsTool(CREDENTIALS_PATH, JD_SAVED_URL, JOB_TRACKER_URL)

    # Parse arguments and build query parameters
    args = parse_arguments()
    query_kwargs = build_query_kwargs(args)

    # Query only needed jobs from Google Sheets
    jobs_to_process = sheets_tool.query_jobs(**query_kwargs)

    # Create workflow
    workflow = create_workflow()

    # Prepare report output paths
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reports_base = os.path.expanduser(config.get("REPORTS_DIR", "reports"))
    report_dir = os.path.join(reports_base, today)
    jobs_dir = os.path.join(report_dir, "jobs")
    os.makedirs(jobs_dir, exist_ok=True)
    summary_path = os.path.join(report_dir, f"summary_{timestamp}.csv")

    # Collect summary rows
    summary_rows = []
    summary_fieldnames = None

    # Error collection
    all_job_errors = []
    
    # Timing tracking
    batch_start_time = time.time()
    job_times = []
    eligible_job_times = []  # Track times only for eligible jobs
    
    # Eligibility tracking
    ineligible_jobs = []
    
    # Debug: collect all parsed JDs with job descriptions
    all_parsed_jds = []
    
    # Debug: collect all ATS scores with job descriptions
    all_ats_scores = []

    for job in jobs_to_process:
        job_uid = job["job_uid"]
        
        # Skip jobs with empty job_uid
        if not job_uid or not job_uid.strip():
            logging.warning(f"Skipping job with empty job_uid")
            continue
            
        job_errors = []
        job_start_time = time.time()

        # Enrich job metadata before workflow
        try:
            job_url = normalize_job_url(job["job_url"])
            job_portal = get_job_portal_name(job_url)
            job_description = clean_job_description(job["job_description"])

            logging.info(f"Processing job {job_uid} from {job_portal}")
        except Exception as e:
            logging.error(f"Error enriching metadata for job {job_uid}: {e}")
            job_url = job["job_url"]
            job_portal = "Unknown"
            job_description = job["job_description"]

        try:
            initial_state = {
                "job_uid": job_uid,
                "job_url": job_url,
                "job_portal": job_portal,
                "job_description": job_description,
                "date_saved": job["date_saved"],
                "resume": resume,
                "personal_statement": personal_statement,
                "candidate_profile": candidate_profile,
                "errors": [],
            }
            result = workflow.invoke(initial_state)  # type: ignore[attr-defined]
            job_elapsed = time.time() - job_start_time
            result["processing_time_seconds"] = round(job_elapsed, 2)
            job_times.append(job_elapsed)
            logging.info(f"⏱️  Job {job_uid} processed in {job_elapsed:.2f} seconds")
        except Exception as e:
            logging.error(f"Exception while processing job {job_uid}: {e}")
            job_errors.append(str(e))
            # Create a minimal result for failed jobs
            result = {"job_uid": job_uid, "errors": [str(e)]}
        try:
            job_out_dir = os.path.abspath(os.path.join(jobs_dir, job_uid))
            os.makedirs(job_out_dir, exist_ok=True)
            json_links, full_report = save_agent_outputs_and_flatten(result, job_uid, job_out_dir)
        except Exception as e:
            logging.error(f"Exception while saving outputs for job {job_uid}: {e}")
            job_errors.append(f"Output save error: {e}")
            json_links, full_report = {"save_error": str(e)}, (
                result if isinstance(result, dict) else {}
            )

        # Prepare summary row
        try:
            summary_row = {
                "job_uid": full_report.get("job_uid"),
                "date_saved": full_report.get("date_saved"),
                "decision": "",
                "company": full_report.get("company"),
                "role": full_report.get("role"),  # Manual decision field, initially empty
                "job_url": full_report.get("job_url"),
                "job_description": full_report.get("job_descr_full"),
                "ats_total_score": full_report.get("ats_total_score"),
                "ats_category": full_report.get("ats_category"),
                "skills_for_ats": full_report.get("skills_for_ats"),
                "eligible": full_report.get("eligible"),
                "hard_blockers": ", ".join(full_report.get("hard_blockers", [])),
                "soft_blockers": ", ".join(full_report.get("soft_blockers", [])),
                "strengths": " | ".join(full_report.get("strengths", [])),
                "technical_gaps": " | ".join(full_report.get("technical_gaps", [])),
                "errors": ", ".join(full_report.get("errors", [])),
            }
            summary_row.update(json_links)
            if job_errors:
                summary_row["errors"] = (
                    summary_row.get("errors", "")
                    + (", " if summary_row.get("errors") else "")
                    + ", ".join(job_errors)
                ).strip(", ")
            summary_rows.append(summary_row)
            if summary_fieldnames is None:
                summary_fieldnames = list(summary_row.keys())
            logging.info(
                f"Processed job {job_uid}: ATS Score = {summary_row.get('ats_total_score')}, ATS Category = {summary_row.get('ats_category')}"
            )
            
            # Track ineligible jobs for summary report
            if full_report.get("eligible") == False:
                ineligible_entry = {
                    "job_uid": job_uid,
                    "company": full_report.get("company"),
                    "role": full_report.get("role"),
                    "hard_blockers": full_report.get("hard_blockers", []),
                    "soft_blockers": full_report.get("soft_blockers", []),
                    "notes": full_report.get("notes", "")
                }
                ineligible_jobs.append(ineligible_entry)
            else:
                # Only track timing for eligible jobs (they go through full workflow)
                if job_times:  # Make sure we captured a time for this job
                    eligible_job_times.append(job_times[-1])
            
            # Collect parsed JD with job description for debugging
            if result.get("parsed_jd"):
                parsed_jd_debug = result["parsed_jd"].copy()
                parsed_jd_debug["job_description"] = result.get("job_description", "")
                all_parsed_jds.append(parsed_jd_debug)
            
            # Collect ATS score with job description for debugging
            if result.get("ats_score"):
                ats_score_debug = result["ats_score"].copy()
                ats_score_debug["job_description"] = result.get("job_description", "")
                all_ats_scores.append(ats_score_debug)
                
        except Exception as e:
            logging.error(f"Exception while preparing summary row for job {job_uid}: {e}")
            all_job_errors.append({"job_uid": job_uid, "error": f"Summary row error: {e}"})
            continue
        if job_errors:
            all_job_errors.append({"job_uid": job_uid, "error": "; ".join(job_errors)})

    # Calculate batch timing
    batch_elapsed = time.time() - batch_start_time
    avg_time_all = sum(job_times) / len(job_times) if job_times else 0
    avg_time_eligible = sum(eligible_job_times) / len(eligible_job_times) if eligible_job_times else 0
    
    # Create batch statistics for logging and Streamlit
    batch_stats = {
        "timestamp": datetime.now().isoformat(),
        "total_time_seconds": round(batch_elapsed, 2),
        "total_jobs_processed": len(job_times),
        "eligible_jobs": len(eligible_job_times),
        "ineligible_jobs": len(ineligible_jobs),
        "avg_time_all_jobs": round(avg_time_all, 2),
        "avg_time_eligible_jobs": round(avg_time_eligible, 2) if eligible_job_times else None,
        "fastest_eligible_job": round(min(eligible_job_times), 2) if eligible_job_times else None,
        "slowest_eligible_job": round(max(eligible_job_times), 2) if eligible_job_times else None,
        "ineligible_jobs_details": ineligible_jobs
    }
    
    # Save batch stats to JSON file alongside summary CSV
    batch_stats_path = os.path.join(report_dir, f"batch_stats_{timestamp}.json")
    try:
        with open(batch_stats_path, "w", encoding="utf-8") as f:
            json.dump(batch_stats, f, ensure_ascii=False, indent=2)
        logging.info(f"Batch statistics saved to {batch_stats_path}")
    except Exception as e:
        logging.error(f"Failed to save batch statistics: {e}")
    
    # Save debug file with all parsed JDs and job descriptions
    if all_parsed_jds:
        debug_parsed_jds_path = os.path.join(report_dir, f"debug_parsed_jds_{timestamp}.json")
        try:
            with open(debug_parsed_jds_path, "w", encoding="utf-8") as f:
                json.dump(all_parsed_jds, f, ensure_ascii=False, indent=2)
            logging.info(f"Debug parsed JDs saved to {debug_parsed_jds_path}")
        except Exception as e:
            logging.error(f"Failed to save debug parsed JDs: {e}")
    
    # Save debug file with all ATS scores and job descriptions
    if all_ats_scores:
        debug_ats_scores_path = os.path.join(report_dir, f"debug_ats_scores_{timestamp}.json")
        try:
            with open(debug_ats_scores_path, "w", encoding="utf-8") as f:
                json.dump(all_ats_scores, f, ensure_ascii=False, indent=2)
            logging.info(f"Debug ATS scores saved to {debug_ats_scores_path}")
        except Exception as e:
            logging.error(f"Failed to save debug ATS scores: {e}")
    
    logging.info(f"\n⏱️  Batch Processing Summary:")
    logging.info(f"   Total time: {batch_elapsed:.2f} seconds")
    logging.info(f"   Total jobs processed: {len(job_times)}")
    logging.info(f"   Eligible jobs (full workflow): {len(eligible_job_times)}")
    logging.info(f"   Ineligible jobs (skipped scoring): {len(ineligible_jobs)}")
    logging.info(f"   Average time (all jobs): {avg_time_all:.2f} seconds")
    if eligible_job_times:
        logging.info(f"   Average time (eligible jobs only): {avg_time_eligible:.2f} seconds")
        logging.info(f"   Fastest eligible job: {min(eligible_job_times):.2f} seconds")
        logging.info(f"   Slowest eligible job: {max(eligible_job_times):.2f} seconds")
    
    # Report ineligible jobs
    if ineligible_jobs:
        logging.info(f"\n🚫 Eligibility Report - {len(ineligible_jobs)} job(s) failed eligibility:")
        for job_info in ineligible_jobs:
            logging.info(f"\n   Job: {job_info['job_uid']} - {job_info['company']} - {job_info['role']}")
            if job_info['hard_blockers']:
                logging.info(f"      ❌ Hard Blockers: {', '.join(job_info['hard_blockers'])}")
            if job_info['soft_blockers']:
                logging.info(f"      ⚠️  Soft Blockers: {', '.join(job_info['soft_blockers'])}")
            if job_info['notes']:
                logging.info(f"      📝 Notes: {job_info['notes']}")
    else:
        logging.info(f"\n✅ All {len(jobs_to_process)} job(s) passed eligibility checks")

    # Write summary CSV
    if summary_rows and summary_fieldnames:
        try:
            with open(summary_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=summary_fieldnames)
                writer.writeheader()
                writer.writerows(summary_rows)
            logging.info(f"Summary written to {summary_path}")
        except Exception as e:
            logging.error(f"Exception while writing summary CSV to {summary_path}: {e}")

    # Report all errors at the end
    if all_job_errors:
        logging.error("\n===== ERRORS ENCOUNTERED DURING JOB PROCESSING =====")
        for err in all_job_errors:
            logging.error(f"Job {err['job_uid']}: {err['error']}")
        print("\n[ERROR] Some jobs failed to process. See log for details.", file=sys.stderr)
        print(f"Failed jobs: {len(all_job_errors)} out of {len(jobs_to_process)}", file=sys.stderr)
        # Exit with error code to indicate failures
        sys.exit(1)

    # If no jobs were found to process
    if not jobs_to_process:
        print("\n[WARNING] No jobs found matching the specified criteria.", file=sys.stderr)
        sys.exit(2)

    # Success - all jobs processed without errors
    print(f"\n[SUCCESS] Successfully processed {len(jobs_to_process)} job(s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
