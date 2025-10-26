"""
setup.py - Initialize Google Sheets for Job Tracker project
Adds or updates headers in the first row of existing Google Sheets.

Usage:
    python scripts/setup.py --both           # Update both sheets
    python scripts/setup.py --saver          # Update JD_Saved only
    python scripts/setup.py --tracker        # Update Job_Tracker only
"""

import gspread
from google.oauth2.service_account import Credentials
import logging
import argparse
import sys
import os

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.utils.logging_utils import setup_logging
from src.utils.config_utils import get_config

# Load config from config.json
config = get_config()

CREDENTIALS_PATH = config["CREDENTIALS_PATH"]
JD_SAVED_URL = config["JD_SAVED_URL"]
JOB_TRACKER_URL = config["JOB_TRACKER_URL"]
JD_SAVED_COLUMNS = config.get(
    "JD_SAVED_COLUMNS", ["job_uid", "date_saved", "job_url", "job_description", "parsed"]
)
JOB_TRACKER_COLUMNS = config["JOB_TRACKER_COLUMNS"]

# Google Sheets API scopes
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]


def get_gspread_client():
    """Get authenticated gspread client"""
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    return gspread.authorize(creds)


def parse_arguments():
    """
    Parse command line arguments for sheet setup.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Initialize Google Sheets headers for Job Tracker project",
        epilog="""
Examples:
  Update both sheets:
    python scripts/setup.py --both
    
  Update only JD_Saved sheet:
    python scripts/setup.py --saver
    
  Update only Job_Tracker sheet:
    python scripts/setup.py --tracker
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Create mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--both", action="store_true", help="Update headers in both JD_Saved and Job_Tracker sheets"
    )
    group.add_argument("--saver", action="store_true", help="Update headers in JD_Saved sheet only")
    group.add_argument(
        "--tracker", action="store_true", help="Update headers in Job_Tracker sheet only"
    )

    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def add_headers_to_sheet(client, sheet_url, columns, sheet_name):
    """
    Add or update headers in the first row of an existing Google Sheet

    Args:
        client: Authenticated gspread client
        sheet_url: URL of the Google Sheet
        columns: List of column headers
        sheet_name: Name for logging purposes
    """
    try:
        # Open the sheet by URL
        spreadsheet = client.open_by_url(sheet_url)
        worksheet = spreadsheet.sheet1  # Get first worksheet

        # Check if first row already has headers
        try:
            existing_headers = worksheet.row_values(1)
            if existing_headers:
                logging.info(
                    f"📋 {sheet_name}: First row already has {len(existing_headers)} headers"
                )
                logging.info(
                    f"   Existing: {', '.join(existing_headers[:5])}{'...' if len(existing_headers) > 5 else ''}"
                )

                # Ask if we should update
                if existing_headers == columns:
                    logging.info(f"✅ {sheet_name}: Headers match config. No update needed.")
                    return
                else:
                    logging.warning(f"⚠️  {sheet_name}: Headers differ from config!")
                    logging.info(
                        f"   Will update to: {', '.join(columns[:5])}{'...' if len(columns) > 5 else ''}"
                    )
        except Exception:
            logging.info(f"📋 {sheet_name}: Sheet appears empty. Adding headers...")

        # Update the first row with headers
        worksheet.update(values=[columns], range_name="A1")
        logging.info(f"✅ {sheet_name}: Headers added/updated successfully!")
        logging.info(f"   Total columns: {len(columns)}")
        logging.info(f"   URL: {spreadsheet.url}")

    except Exception as e:
        logging.error(f"❌ {sheet_name}: Failed to add headers - {e}")
        raise


def main():
    """Main setup function"""
    # Initialize logging
    setup_logging()

    # Parse arguments
    args = parse_arguments()

    logging.info("=" * 60)
    logging.info("🚀 Starting Google Sheets Setup")
    logging.info("=" * 60)

    client = get_gspread_client()

    # Update sheets based on arguments
    if args.both or args.saver:
        logging.info("\n📊 Processing JD_Saved sheet...")
        add_headers_to_sheet(client, JD_SAVED_URL, JD_SAVED_COLUMNS, "JD_Saved")

    if args.both or args.tracker:
        logging.info("\n📊 Processing Job_Tracker sheet...")
        add_headers_to_sheet(client, JOB_TRACKER_URL, JOB_TRACKER_COLUMNS, "Job_Tracker")

    logging.info("\n" + "=" * 60)
    logging.info("✅ Setup complete!")
    logging.info("=" * 60)


if __name__ == "__main__":
    main()
