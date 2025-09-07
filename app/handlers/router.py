import os
from fastapi import Depends
from fastapi import APIRouter, status
from app.services import slack
from app.utils import Settings, create_google_credentials_file
from app.services.slack import Slack
from app.services.google import Docs
from app.services.bedrock import Bedrock
from app.services.orchestrator import Orchestrator
from .models import SlackChallengeRequest, SlackEventCallback

settings = Settings()
router = APIRouter()
credentials_path = create_google_credentials_file(settings, os.getcwd())


def get_slack_service():
    return Slack(settings.slack_channel_id, settings.slack_bot_token)


def get_google_service():
    return Docs(settings, credentials_path)


def get_bedrock_service():
    return Bedrock(
        settings.aws_profile, settings.aws_region, settings.aws_bedrock_model_id
    )


def get_orchestrator(
    slack: Slack = Depends(get_slack_service),
    google: Docs = Depends(get_google_service),
    ai: Bedrock = Depends(get_bedrock_service),
):
    return Orchestrator(slack, google, ai)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}


@router.post("/slack/event_verification", status_code=status.HTTP_200_OK)
async def slack_event_verification(event: SlackChallengeRequest):
    return {"challenge": event.challenge}


@router.post("/slack/mention", status_code=status.HTTP_200_OK)
async def slack_event(
    payload: SlackEventCallback, orchestrator: Orchestrator = Depends(get_orchestrator)
):
    try:
        thread_ts = payload.event.ts
        result = orchestrator.generate_report(thread_ts)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
