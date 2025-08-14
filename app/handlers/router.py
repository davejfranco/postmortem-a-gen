from .models import SlackChallengeRequest, SlackEventCallback
from app.utils import Settings
from fastapi import APIRouter, status

settings = Settings()
router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}

@router.post("/slack/event_verification", status_code=status.HTTP_200_OK)
async def slack_event_verification(event: SlackChallengeRequest):
    return {"challenge": event.challenge}

@router.post("/slack/mention", status_code=status.HTTP_200_OK)
async def slack_event(payload: SlackEventCallback):
    return {"status": "ok"}
