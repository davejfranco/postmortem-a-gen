import os
from typing import Optional, List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Slack:
    def __init__(self, channel_id: str, slack_bot_token: str) -> None:
        self.channel_id = channel_id
        self.slack_bot_token = slack_bot_token
        self.client = WebClient(token=self.slack_bot_token)

    @staticmethod
    def publish_message(channel_id: str, slack_bot_token: str, text: str) -> Optional[Dict[str, Any]]:
        """Send a message to the channel"""
        try:
            client = WebClient(token=slack_bot_token)
            response = client.chat_postMessage(channel=channel_id, text=text)
            return response
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
            return None

    @staticmethod
    def get_conversation(channel_id: str, slack_bot_token: str) -> Optional[List[Dict[str, Any]]]:
        """Get all messages in the channel"""
        try:
            client = WebClient(token=slack_bot_token)
            response = client.conversations_history(channel=channel_id)
            return response["messages"]
        except SlackApiError as e:
            print(f"Error reading chat history: {e.response['error']}")
            return None

    @staticmethod
    def get_thread_conversation(channel_id: str, slack_bot_token: str, thread_ts: str) -> Optional[List[Dict[str, Any]]]:
        """Get all messages in a specific thread"""
        try:
            client = WebClient(token=slack_bot_token)
            all_messages = []
            cursor = None

            while True:
                response = client.conversations_replies(
                    channel=channel_id, ts=thread_ts, cursor=cursor
                )

                all_messages.extend(response["messages"])

                if not response.get("has_more", False):
                    break

                cursor = response.get("response_metadata", {}).get("next_cursor")
                if not cursor:
                    break

            return all_messages
        except SlackApiError as e:
            print(f"Error reading thread: {e.response['error']}")
            return None


if __name__ == "__main__":
    channel_id = "C098VR4DG9E"
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    print(Slack.get_thread_conversation(channel_id, slack_bot_token, "1753902018.594989"))
