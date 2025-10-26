"""
finalize_decisions.py - Manual approval workflow for job applications

Reviews processed jobs from summary CSV and uploads approved jobs to Job Tracker.
Supports dry-run mode for safe testing before making actual changes.

Steps:
1. Loads the summary CSV (all_jobs_summary_{date}.csv)
2. Filters for APPLY decisions
3. Constructs tracker rows in exact column order from config
4. Uploads to Job Tracker sheet (if not dry-run)
5. Marks jobs as Parsed in JD_Saved sheet (if not dry-run)

Usage:
    python scripts/finalize_decisions.py --csv reports/all_jobs_summary_2025-10-17.csv --dry-run
    python scripts/finalize_decisions.py --csv reports/all_jobs_summary_2025-10-17.csv
"""

import csv
import argparse
import os
import sys
import json
import time

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.google_sheets_tool import GoogleSheetsTool
from src.utils.logging_utils import setup_logging
from src.utils.config_utils import get_config
import logging


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Finalize job decisions and upload approved jobs to tracker",
        epilog="""
Examples:
  Test what would be uploaded (dry-run):
    python scripts/finalize_decisions.py --csv reports/2025-10-18/summary_20251018_120000.csv --dry-run
    
  Upload approved jobs to Job Tracker:
    python scripts/finalize_decisions.py --csv reports/2025-10-18/summary_20251018_120000.csv
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--csv", type=str, required=True, help="Path to summary CSV file with decisions"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not upload or mark jobs, just print/log what would be done",
    )

    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def process_apply_row(row, sheets_tool, dry_run, job_tracker_columns):
    """
    Process a row with APPLY decision - upload to tracker and mark as parsed.

    Args:
        row: Dictionary representing a CSV row
        sheets_tool: GoogleSheetsTool instance
        dry_run: Whether to run in dry-run mode
        job_tracker_columns: List of column names for Job_Tracker sheet

    Returns:
        int: 1 if successfully processed, 0 otherwise
    """
    job_uid = row.get("job_uid")

    # Load full report JSON for the job to get all fields
    full_report_path = row.get("flat_report_json")
    full_report = {}
    if full_report_path and os.path.exists(full_report_path):
        with open(full_report_path, "r", encoding="utf-8") as f:
            full_report = json.load(f)
    else:
        logging.warning(
            f"Full report not found for job {job_uid}. Proceeding with summary row only."
        )

    # Explicitly construct tracker_row in correct order
    tracker_row = {}
    for col in job_tracker_columns:
        # full_report fields take precedence, then row, else blank
        tracker_row[col] = full_report.get(col, row.get(col, ""))

    # Upload to tracker and mark as processed
    if dry_run:
        logging.info(f"[DRY RUN] Would upload job {job_uid} to tracker.")
        logging.info(f"[DRY RUN] Would mark job {job_uid} as processed in JD_Saved.")
    else:
        sheets_tool.upload_to_tracker(tracker_row)
        logging.info(f"Uploaded job {job_uid} to tracker.")
        time.sleep(5)  # Rate limiting between API calls
        sheets_tool.mark_as_parsed(job_uid)
        logging.info(f"Marked job {job_uid} as processed in JD_Saved.")
        time.sleep(5)  # Wait before processing next job

    return 1


def process_pass_row(row, sheets_tool, dry_run):
    """
    Process a row with PASS decision - just mark as parsed.

    Args:
        row: Dictionary representing a CSV row
        sheets_tool: GoogleSheetsTool instance
        dry_run: Whether to run in dry-run mode

    Returns:
        int: 1 if successfully processed, 0 otherwise
    """
    job_uid = row.get("job_uid")

    if job_uid:
        if dry_run:
            logging.info(f"[DRY RUN] Would mark job {job_uid} (PASS) as processed in JD_Saved.")
        else:
            sheets_tool.mark_as_parsed(job_uid)
            logging.info(f"Marked job {job_uid} (PASS) as processed in JD_Saved.")
        return 1

    return 0


def main():
    """Main function to finalize job decisions."""
    # Initialize logging
    setup_logging()

    # Load configuration
    config = get_config()
    credentials_path = config["CREDENTIALS_PATH"]
    job_tracker_url = config["JOB_TRACKER_URL"]
    jd_saved_url = config["JD_SAVED_URL"]
    job_tracker_columns = config["JOB_TRACKER_COLUMNS"]

    # Parse arguments
    args = parse_arguments()

    # Initialize Google Sheets tool
    sheets_tool = GoogleSheetsTool(credentials_path, jd_saved_url, job_tracker_url)

    # Read CSV and separate into APPLY and PASS records
    apply_rows = []
    pass_rows = []
    empty_rows = []

    with open(args.csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            decision = row.get("decision", "").strip().upper()
            if decision == "APPLY":
                apply_rows.append(row)
            elif decision == "PASS":
                pass_rows.append(row)
            else:
                empty_rows.append(row)

    # Counters
    apply_processed = 0
    pass_processed = 0

    # Process all APPLY records first
    if apply_rows:
        print(f"\n{'='*60}")
        print(f"Processing {len(apply_rows)} APPLY records...")
        print(f"{'='*60}\n")
        for row in apply_rows:
            apply_processed += process_apply_row(
                row, sheets_tool, args.dry_run, job_tracker_columns
            )

    # Then process all PASS records
    if pass_rows:
        print(f"\n{'='*60}")
        print(f"Processing {len(pass_rows)} PASS records...")
        print(f"{'='*60}\n")
        for row in pass_rows:
            pass_processed += process_pass_row(row, sheets_tool, args.dry_run)

    # Print summary
    print(f"\n{'='*60}")
    print(f"[SUCCESS] Finalization complete!")
    print(f"{'='*60}")
    print(f"APPLY jobs uploaded to Job_Tracker: {apply_processed}")
    print(f"PASS jobs marked as parsed: {pass_processed}")
    print(f"Empty decision jobs (skipped): {len(empty_rows)}")
    print(f"Total jobs in CSV: {len(apply_rows) + len(pass_rows) + len(empty_rows)}")
    print(f"{'='*60}\n")

    # Exit codes for Streamlit to handle different outcomes
    # 0 = Success with actions taken (jobs uploaded or marked)
    # 1 = No APPLY or PASS decisions found (nothing to do)
    # 2 = Empty CSV or no jobs found

    total_processed = apply_processed + pass_processed

    if total_processed == 0:
        if len(apply_rows) + len(pass_rows) == 0:
            print("[WARNING] No APPLY or PASS decisions found in CSV.", file=sys.stderr)
            sys.exit(1)
        else:
            print("[ERROR] Jobs were found but none were successfully processed.", file=sys.stderr)
            sys.exit(2)

    # Success - at least some jobs were processed
    sys.exit(0)


if __name__ == "__main__":
    main()
