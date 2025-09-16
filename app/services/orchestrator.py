from datetime import date
from typing import Optional
from app.services.bedrock import Bedrock
from app.services.google import Docs
from app.services.slack import Slack


class PostmortemError(Exception):
    """"Custom exception for postmortem generation failures"""
    pass

class Orchestrator:
    def __init__(self, slack: Slack, google: Docs, ai: Bedrock):
        self.slack = slack
        self.google = google
        self.ai = ai

    def _get_conversation(self, thread_ts: str) -> Optional[str]:
        try:
            slack_thread =  self.slack.get_thread_conversation(thread_ts)
            return self.slack.human_readable_conversation(slack_thread)
        except Exception as e:
            raise PostmortemError(f"Could not retrieve Slack conversation: {e}")

    def generate_report(self, thread_ts: str):
        """
        Generate postmortem report from Slack thread 
        """
        try:
            slack_chat = self._get_conversation(thread_ts)
            try:
                report = self.ai.create_postmortem_summary(slack_chat)
                summary = report.get("content")[0].get("text")
            except (KeyError, IndexError, TypeError) as e:
                raise PostmortemError(f"AI service returned invalid response: {e}")
            except Exception as e:
                print(self.ai.model_id)
                raise PostmortemError(f"Failed to generate AI summary: {e}, {self.ai.model_id}")

            try:
                today = date.today().isoformat()
                doc_title = f"{today} - Postmortem(preview)"
                self.google.generate_report(summary, doc_title)
                return
            except Exception as e:
                PostmortemError(f"failed to generate report document: {e}")
        except PostmortemError:
            raise
        except Exception as e:
            raise PostmortemError(f"Unexpected error during postmortem generation: {e}")
        return
