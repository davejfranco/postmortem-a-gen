import os
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Path to your downloaded JSON credentials
SERVICE_ACCOUNT_FILE = "credentials.json"

# Scopes: Drive is needed for listing files
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents.readonly",
]

SUBJECT=os.environ.get("GOOGLE_SERVICE_ACCOUNT_SUBJECT", "")

class Docs:
    def __init__(self, folder_id: str, credentials: str):
        self.folder_id = folder_id
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials, scopes=SCOPES, subject=SUBJECT
        )

        self.drive_service = build("drive", "v3", credentials=self.credentials)
        self.docs_service = build("docs", "v1", credentials=self.credentials)

    def _create_empty_file(self, file_name: str):
        """This creates an empty file for the report in the specified folder."""
        file_metadata = {
            "name": file_name,
            "mimeType": "application/vnd.google-apps.document",
            "parents": [self.folder_id],
        }

        try:
            file = self.drive_service.files().create(body=file_metadata).execute()
            return file.get("id")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return


    def generate_report(self, content: List[str], file_name: str) -> str | None:
        # Generate blank file 
        try:
             file_id = self._create_empty_file(file_name)
             if file_id is None:  # Add this check
                 print("Failed to create file - cannot proceed with report generation")
                 return
        except Exception as error:
             print(f"An error occurred: {error}")
             return
        try:
            request = [
                {
                    "insertText": {
                    "endOfSegmentLocation": {},
                    "text": f"{line}"
                    }
                }
                for line in content
            ]
            self.docs_service.documents().batchUpdate(
                documentId=file_id,
                body={'requests': request}).execute()
            return f"https://docs.google.com/document/d/{file_id}/"
        except HttpError as error:
            print(f"An error occurred: {error}")
            return
