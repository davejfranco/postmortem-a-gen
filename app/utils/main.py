import os
from datetime import datetime
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_region: str = os.environ.get("AWS_REGION", "us-west-2")
    aws_profile: str = os.environ.get("AWS_PROFILE", "personal")
    aws_bedrock_model_id: str = os.environ.get(
        "AWS_BEDROCK_MODEL_ID", "us.anthropic.claude-opus-4-20250514-v1:0"
    )

    slack_bot_token: str = os.environ["SLACK_BOT_TOKEN"]
    slack_signing_secret: str = os.environ["SLACK_SIGNING_SECRET"]
    slack_channel_id: str = os.environ["SLACK_CHANNEL_ID"]

    google_folder_id: str = os.environ["GOOGLE_FOLDER_ID"]
    google_service_account_subject: str = os.environ.get(
        "GOOGLE_SERVICE_ACCOUNT_SUBJECT", ""
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
