import os
import json
from datetime import datetime
from pydantic_settings import BaseSettings

from app.services import google


class Settings(BaseSettings):
    aws_region: str = os.environ.get("AWS_REGION", "us-west-2")
    aws_profile: str = os.environ.get("AWS_PROFILE", "")
    aws_bedrock_model_id: str = os.environ.get(
        "AWS_BEDROCK_MODEL_ID",
        f"{aws_region.split('-')[0]}.anthropic.claude-opus-4-20250514-v1:0",
    )
    slack_bot_token: str = os.environ["SLACK_BOT_TOKEN"]
    slack_signing_secret: str = os.environ["SLACK_SIGNING_SECRET"]
    slack_channel_id: str = os.environ["SLACK_CHANNEL_ID"]

    google_folder_id: str = os.environ["GOOGLE_FOLDER_ID"]
    google_service_account_subject: str = os.environ.get(
        "GOOGLE_SERVICE_ACCOUNT_SUBJECT", ""
    )
    google_access_type: str = os.environ.get("GOOGLE_ACCESS_TYPE", "service_account")
    google_project_id: str = os.environ.get("GOOGLE_PROJECT_ID", "slack-app-postmortem")
    google_private_key_id: str = os.environ["GOOGLE_PRIVATE_KEY_ID"]
    google_private_key: str = os.environ["GOOGLE_PRIVATE_KEY"]
    google_client_email: str = os.environ["GOOGLE_CLIENT_EMAIL"]
    google_client_id: str = os.environ["GOOGLE_CLIENT_ID"]
    google_auth_uri: str = os.environ["GOOGLE_AUTH_URI"]
    google_token_uri: str = os.environ["GOOGLE_TOKEN_URI"]
    google_auth_provider_cert_url: str = os.environ["GOOGLE_AUTH_PROVIDER_CERT_URL"]
    google_client_cert_url: str = os.environ["GOOGLE_CLIENT_CERT_URL"]
    google_universe_domain: str = os.environ.get(
        "GOOGLE_UNIVERSE_DOMAIN", "googleapis.com"
    )
    google_credentials: str = os.environ.get(
        "GOOGLE_CREDENTIALS_FILE", "/app/credentials.json"
    )



def convert_timestamp_to_readable(
    timestamp: str, format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    ts_float = float(timestamp)
    dt = datetime.fromtimestamp(ts_float)
    return dt.strftime(format)
