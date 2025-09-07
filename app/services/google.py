import os
import json
from typing import List, Optional
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

SUBJECT = os.environ.get("GOOGLE_SERVICE_ACCOUNT_SUBJECT", "")


def create_google_credentials_file(settings, file_path: str = "/app") -> str:
    """Create Google credentials JSON file from Settings object."""
    credentials = {
        "type": settings.google_access_type,
        "project_id": settings.google_project_id,
        "private_key_id": settings.google_private_key_id,
        "private_key": settings.google_private_key.replace("\\n", "\n"),
        "client_email": settings.google_client_email,
        "client_id": settings.google_client_id,
        "auth_uri": settings.google_auth_uri,
        "token_uri": settings.google_token_uri,
        "auth_provider_x509_cert_url": settings.google_auth_provider_cert_url,
        "client_x509_cert_url": settings.google_client_cert_url,
        "universe_domain": settings.google_universe_domain,
    }

    file_full_path = os.path.join(file_path, "credentials.json")
    with open(file_full_path, "w") as f:
        json.dump(credentials, f, indent=2)

    return file_full_path


class Docs:
    def __init__(self, settings, credentials_path: str):
        self.folder_id = settings.google_folder_id
        self.credentials_path = credentials_path

        # print(f"Creating creadentials file at {os.path.join(file_path, "credentials.json")}")
        # credentials_path = create_google_credentials_file(settings, file_path)

        # print(f"credentials file created at {credentials_path}")

        self.credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path,
            scopes=SCOPES,
            subject=settings.google_service_account_subject,
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
                {"insertText": {"endOfSegmentLocation": {}, "text": f"{line}"}}
                for line in content
            ]
            self.docs_service.documents().batchUpdate(
                documentId=file_id, body={"requests": request}
            ).execute()
            return f"https://docs.google.com/document/d/{file_id}/"
        except HttpError as error:
            print(f"An error occurred: {error}")
            return
