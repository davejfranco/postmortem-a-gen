import boto3 
from botocore.exceptions import ClientError


DEFAULT_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

POSTMORTEM_SUMMARY_PROMPT = """You are a Site Reliability Engineer tasked with creating postmortem report summaries. 

Given a conversation with timestamps about an incident, please create a concise postmortem summary that includes:

1. **Incident Overview**: Brief description of what happened
2. **Timeline**: Key events with timestamps
3. **Impact**: What systems/users were affected
4. **Root Cause**: Primary cause of the incident
5. **Resolution**: How the incident was resolved
6. **Action Items**: Key follow-up tasks to prevent recurrence

Please analyze the conversation and provide a structured summary suitable for a postmortem report."""


class BedrockClient:
    def __init__(self, aws_profile, region_name='us-east-1', model_id=DEFAULT_MODEL_ID):
        self.session = boto3.Session(profile_name=aws_profile, region_name=region_name)
        self.client = self.session.client('bedrock-runtime')
        self.model_id = model_id
    
    def chat(self, conversation):
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=conversation,
                system=[{"text":POSTMORTEM_SUMMARY_PROMPT}],
            )
            return response['output']['message']
        except ClientError as e:
            raise Exception(f"An error occurred: {e.response['Error']['Message']}")
    
    def create_postmortem_summary(self, incident_conversation):
        conversation = [
            {"role": "user", "content": [{"text": f"Here is the incident conversation with timestamps:\n\n{incident_conversation}"}]}
        ]
        return self.chat(conversation)

    #if __name__ == "__main__":
    #    client = BedrockClient(aws_profile='personal')
    #    thread_conversation = """
    #        - 03:45 PM: Incident started - Service X is down
    #        - 04:00 PM: Alert triggered - High error rates detected
    #        - 04:15 PM: Team notified - Engineers start investigation
    #        - 04:30 PM: Root cause identified - Database connection issue
    #        - 04:45 PM: Fix applied - Database connection restored"""
    #    print(client.create_postmortem_summary(thread_conversation))
