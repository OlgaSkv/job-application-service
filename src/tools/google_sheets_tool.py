import gspread
from google.oauth2.service_account import Credentials
from typing import List, Optional, Dict, Any
import logging

# Constants for Google Sheets operations
PARSED_COLUMN_NAME = "parsed"
PARSED_TRUE_VALUE = "TRUE"
PARSED_FALSE_VALUE = "FALSE"
JOB_UID_FIELD = "job_uid"


class GoogleSheetsTool:
    """
    Tool for reading/writing Google Sheets for job data management.

    Manages two sheets:
    - JD_Saved: Staging area for jobs to be processed
    - Job_Tracker: Permanent tracking sheet for approved jobs
    """

    def __init__(self, credentials_path: str, jd_saved_url: str, job_tracker_url: str):
        """
        Initialize Google Sheets tool with credentials and sheet URLs.

        Args:
            credentials_path: Path to Google service account credentials JSON
            jd_saved_url: URL of the JD_Saved Google Sheet
            job_tracker_url: URL of the Job_Tracker Google Sheet
        """
        self.credentials_path = credentials_path
        self.jd_saved_url = jd_saved_url
        self.job_tracker_url = job_tracker_url
        self.client = self._get_client()

    def _get_client(self):
        """
        Create and authorize gspread client with service account credentials.

        Returns:
            Authorized gspread Client object
        """
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(self.credentials_path, scopes=scope)
        return gspread.authorize(creds)

    def get_jd_saved_sheet(self):
        """
        Get the first sheet of JD_Saved spreadsheet.

        Returns:
            gspread Worksheet object

        Raises:
            Exception if sheet cannot be opened
        """
        try:
            return self.client.open_by_url(self.jd_saved_url).sheet1
        except Exception as e:
            logging.error(f"Failed to open JD_Saved sheet: {e}")
            raise

    def get_job_tracker_sheet(self):
        """
        Get the first sheet of Job_Tracker spreadsheet.

        Returns:
            gspread Worksheet object

        Raises:
            Exception if sheet cannot be opened
        """
        try:
            return self.client.open_by_url(self.job_tracker_url).sheet1
        except Exception as e:
            logging.error(f"Failed to open Job_Tracker sheet: {e}")
            raise

    def query_jobs(
        self,
        parsed: Optional[bool] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        uids: Optional[List[str]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Query jobs from JD_Saved sheet with optional filters.

        Args:
            parsed: Filter by parsed status (True/False/None for all)
            date_from: Include jobs from this date onwards (YYYY-MM-DD)
            date_to: Include jobs up to this date (YYYY-MM-DD)
            uids: List of job UIDs to include
            limit: Maximum number of jobs to return

        Returns:
            List of job dictionaries matching the filters

        Example:
            >>> tool = GoogleSheetsTool(creds_path, jd_url, tracker_url)
            >>> # Get all unprocessed jobs from October 2025
            >>> jobs = tool.query_jobs(parsed=False, date_from="2025-10-01", limit=10)
            >>> # Get specific jobs by UID
            >>> jobs = tool.query_jobs(uids=["JD-001", "JD-002"])
        """
        try:
            sheet = self.get_jd_saved_sheet()
            all_jobs = sheet.get_all_records()

            # Filter by parsed status
            if parsed is not None:
                def is_parsed(job):
                    parsed_value = job.get(PARSED_COLUMN_NAME, "")
                    # Handle string values from Google Sheets
                    if isinstance(parsed_value, str):
                        return parsed_value.upper() == PARSED_TRUE_VALUE
                    # Handle boolean values
                    return bool(parsed_value)
                
                all_jobs = [j for j in all_jobs if is_parsed(j) == bool(parsed)]

            # Filter by date range
            if date_from or date_to:

                def in_range(job):
                    d = job.get("date_saved")
                    if not d:
                        return False
                    if date_from and d < date_from:
                        return False
                    if date_to and d > date_to:
                        return False
                    return True

                all_jobs = [j for j in all_jobs if in_range(j)]

            # Filter by UIDs (FIXED: was using 'uid' instead of 'job_uid')
            if uids:
                all_jobs = [j for j in all_jobs if j.get(JOB_UID_FIELD) in uids]

            # Limit results
            if limit:
                all_jobs = all_jobs[:limit]

            return all_jobs
        except Exception as e:
            logging.error(f"Failed to query jobs: {e}")
            return []

    def mark_as_parsed(self, uid: str):
        """
        Mark a job as parsed in the JD_Saved sheet.

        Finds the job by UID and updates the 'parsed' column to TRUE.

        Args:
            uid: Job UID to mark as parsed

        Raises:
            ValueError: If uid is empty or None
        """
        if not uid or not uid.strip():
            raise ValueError("Job UID cannot be empty")

        try:
            sheet = self.get_jd_saved_sheet()
            cell = sheet.find(uid)
            if cell:
                parsed_col = sheet.find(PARSED_COLUMN_NAME).col
                sheet.update_cell(cell.row, parsed_col, PARSED_TRUE_VALUE)
                logging.info(f"Marked job {uid} as parsed")
            else:
                logging.warning(f"UID {uid} not found in JD_Saved sheet.")
        except Exception as e:
            logging.error(f"Failed to mark UID {uid} as parsed: {e}")

    def upload_to_tracker(self, job_data: Dict[str, Any]):
        """
        Upload a job to the Job_Tracker sheet.

        Appends a new row with job data values.
        Note: Assumes job_data dict is ordered to match Job_Tracker columns.

        Args:
            job_data: Dictionary of job data (must be in column order)

        Raises:
            ValueError: If job_data is empty or missing job_uid
        """
        if not job_data:
            raise ValueError("Job data cannot be empty")
        if JOB_UID_FIELD not in job_data or not job_data.get(JOB_UID_FIELD):
            raise ValueError(f"Job data must contain '{JOB_UID_FIELD}' field")

        try:
            # Convert list values to comma-separated strings
            # Google Sheets API doesn't accept Python lists as cell values
            serialized_data = {}
            for key, value in job_data.items():
                if isinstance(value, list):
                    # Join list items with comma-space separator
                    serialized_data[key] = ", ".join(str(item) for item in value) if value else ""
                elif value is None:
                    # Convert None to empty string
                    serialized_data[key] = ""
                else:
                    serialized_data[key] = value

            sheet = self.get_job_tracker_sheet()
            sheet.append_row(list(serialized_data.values()))
            logging.info(f"Uploaded job {job_data.get(JOB_UID_FIELD, 'unknown')} to Job_Tracker")
        except Exception as e:
            logging.error(f"Failed to upload job to Job_Tracker: {e}")
