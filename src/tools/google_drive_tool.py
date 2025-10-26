from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from typing import Optional
import json
import logging


class GoogleDriveTool:
    """
    Tool for loading documents (resume, personal statement, profile) from Google Drive.

    Uses Google Drive API v3 to export documents as plain text.
    """

    def __init__(self, credentials_path: str):
        """
        Initialize Google Drive tool with service account credentials.

        Args:
            credentials_path: Path to Google service account credentials JSON
        """
        self.credentials_path = credentials_path
        self.service = self._get_service()

    def _get_service(self):
        """
        Create and authorize Google Drive API service.

        Returns:
            Authorized Google Drive API v3 service object
        """
        scope = ["https://www.googleapis.com/auth/drive.readonly"]
        creds = Credentials.from_service_account_file(self.credentials_path, scopes=scope)
        return build("drive", "v3", credentials=creds)

    def load_doc(self, file_id: str, mime_type: str = "text/plain") -> Optional[str]:
        """
        Load and export a file from Google Drive as text.

        For Google Docs/Sheets, exports as specified mime_type.
        For other files (JSON, TXT), downloads directly.

        Args:
            file_id: Google Drive file ID
            mime_type: MIME type for export (default: text/plain)

        Returns:
            File content as string, or None if loading fails
        """
        try:
            # Try export first (for Google Docs)
            request = self.service.files().export_media(fileId=file_id, mimeType=mime_type)
            file_content = request.execute()
            return file_content.decode("utf-8")
        except Exception as download_error:
            logging.error(
                f"Failed to load file {file_id} from Google Drive: Download error: {download_error}"
            )
            return None

    def load_json(
        self,
        file_id: str,
    ) -> Optional[str]:
        """
        Load and export a file from Google Drive as text.

        For Google Docs/Sheets, exports as specified mime_type.
        For other files (JSON, TXT), downloads directly.

        Args:
            file_id: Google Drive file ID

        Returns:
            File content as json, or None if loading fails
        """
        try:
            # Try export first (for Google Docs)
            request = self.service.files().get(fileId=file_id, alt="media")
            file_content = request.execute()
            return json.dumps(file_content)
        except Exception as download_error:
            logging.error(
                f"Failed to load file {file_id} from Google Drive: Download error: {download_error}"
            )
            return None
