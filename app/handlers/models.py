from pydantic import BaseModel
from typing import List

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

class SlackEventCallback(BaseModel):
    token: str
    team_id: str
    api_app_id: str
    event: Event
    type: str
    event_id: str
    event_time: int
    authed_users: List[str]
