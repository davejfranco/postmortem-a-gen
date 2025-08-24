# import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Optional, List, Dict, Any
from slack_sdk.web import SlackResponse
from app.utils import convert_timestamp_to_readable


class Slack:
    def __init__(self, channel_id: str, slack_bot_token: str):
        self.channel_id = channel_id
        self.slack_bot_token = slack_bot_token
        self.client = WebClient(token=self.slack_bot_token)

    def publish_message(self, text: str) -> Optional[SlackResponse]:
        """Send a message to the channel"""
        try:
            response = self.client.chat_postMessage(channel=self.channel_id, text=text)
            return response
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
            return None

    def get_conversation(self) -> Optional[List[Dict[str, Any]]]:
        """Get all messages in the channel"""
        try:
            response = self.client.conversations_history(channel=self.channel_id)
            return response["messages"]
        except SlackApiError as e:
            print(f"Error reading chat history: {e.response['error']}")
            return None

    def get_thread_conversation(self, thread_ts: str) -> Optional[List[Dict[str, Any]]]:
        """Get all messages in a specific thread"""
        try:
            all_messages = []
            cursor = None

            while True:
                response = self.client.conversations_replies(
                    channel=self.channel_id, ts=thread_ts, cursor=cursor
                )
                
                messages = response.get("messages")
                if messages:
                    all_messages.extend(messages)

                if not response.get("has_more", False):
                    break

                cursor = response.get("response_metadata", {}).get("next_cursor")
                if not cursor:
                    break

            return all_messages
        except SlackApiError as e:
            print(f"Error reading thread: {e.response['error']}")
            return None

    def get_user_info(self, user_id: str) -> Optional[str]:
        """Get User information by user ID"""
        try:
            response = self.client.users_info(user=user_id)
            user_data = response.get("user")
            if user_data:
                return user_data.get("real_name")
            return None
        except SlackApiError as e:
            print(f"Error getting user info: {e.response['error']}")
            return None

    def human_readable_conversation(self, slack_thread_conversion):
        pretty_conversation = []

        for msg in slack_thread_conversion:
            pretty_msg = {}
            pretty_msg["user"] = self.get_user_info(msg["user"])
            pretty_msg["text"] = msg["text"]
            pretty_msg["ts"] = convert_timestamp_to_readable(msg["ts"])

            pretty_conversation.append(pretty_msg)
        return pretty_conversation
