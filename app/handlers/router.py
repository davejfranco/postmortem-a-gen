import os
from fastapi import APIRouter, Request, BackgroundTasks, Depends, status
from app.services import slack
from app.utils import Settings, create_google_credentials_file
from app.services.slack import Slack
from app.services.google import Docs
from app.services.bedrock import Bedrock
from app.services.orchestrator import Orchestrator
from .models import SlackCommandRequest, SlackCommandResponse, SlackChallengeRequest

settings = Settings()
router = APIRouter()
credentials_path = create_google_credentials_file(settings, os.getcwd())


def get_slack_service():
    return Slack(settings.slack_channel_id, settings.slack_bot_token)


def get_google_service():
    return Docs(settings, credentials_path)


def get_bedrock_service():
    return Bedrock(
        settings.aws_bedrock_model_id,
        settings.aws_profile,
        settings.aws_region,
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
    #payload: SlackCommandRequest, 
    request: Request,
    background: BackgroundTasks,
    orchestrator: Orchestrator = Depends(get_orchestrator)
):
    form = await request.form()
    payload = SlackCommandRequest.model_validate(dict(form))
    try:
        url = (payload.text or "").strip()
        #result = orchestrator.generate_report(thread_ts)
        background.add_task(orchestrator.generate_report, url)
        return SlackCommandResponse(
            text="Postmortem report generation initiated. The report will be available in the specified Google Drive folder shortly."
        )
    except Exception as e:
        return SlackCommandResponse(
            text=f"Error generating report, error: {str(e)}"
        )
