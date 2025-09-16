from pydantic import BaseModel
from typing import List, Optional

class Event(BaseModel):
    type: str
    user: str
    text: str
    ts: str
    channel: str
    event_ts: str

class SlackChallengeRequest(BaseModel):
    type: str
    token: str
    challenge: str

class SlackCommandRequest(BaseModel):
    token: Optional[str] = None
    team_id: str
    team_domain: Optional[str] = None
    enterprise_id: Optional[str] = None
    enterprise_name: Optional[str] = None

    channel_id: str
    channel_name: Optional[str] = None

    user_id: str
    user_name: Optional[str] = None

    command: str
    text: Optional[str] = None

    response_url: str
    trigger_id: Optional[str] = None
    api_app_id: Optional[str] = None
    is_enterprise_install: Optional[bool] = None

class SlackCommandResponse(BaseModel):
    response_type: Optional[str] = "in_channel"
    text: Optional[str] = None

class SlackEventCallback(BaseModel):
    token: str
    team_id: str
    api_app_id: str
    event: Event
    type: str
    event_id: str
    event_time: int
    authed_users: List[str]
