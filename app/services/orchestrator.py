from datetime import date
from app.services.bedrock import BedrockClient
from app.services.google import Docs
from app.services.slack import Slack


class Orchestrator:
    def __init__(self, slack: Slack, google: Docs, ai: BedrockClient):
        self.slack = slack
        self.google = google
        self.ai = ai

    def get_conversation(self, thread_ts: str):
        return self.slack.human_readable_conversation(thread_ts)

    def generate_report(self, thread_ts: str):
        slack_thread = self.slack.human_readable_conversation(thread_ts)
        
        today = date.today().isoformat()
        self.google.generate_report(
            slack_thread,
            f"{today} - Postmortem(preview)"
        )
        return
