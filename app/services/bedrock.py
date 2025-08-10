import boto3
from botocore.exceptions import ClientError


DEFAULT_MODEL_ID = "us.anthropic.claude-opus-4-20250514-v1:0"

POSTMORTEM_SUMMARY_PROMPT = """You are a Site Reliability Engineer tasked with creating postmortem report summaries. 

Given a conversation with timestamps about an incident, please create a concise postmortem report:

It needs to contain the following sections:
1. **Incident Report**: Brief description of what happened
2. **Impact**: What systems were affected
3. **Summary**: Key events with timestamps
4. **Post-Incident Review**: Including sub sections for root cause, recovery summarym prevention measures.

Example:
Summary
Impacted Components:

Routing Node A

Gateway B

Core Database C

Monitoring Window: 2025-07-19 14:35:00 → 16:00:00


Detailed Timeline
14:42:30: Complete packet loss observed on Routing Node A.

14:42:40: Load begins increasing on Gateway B.

14:43:10: Signaling spike on Protocol A and interconnect interfaces.

14:45:30: Partial recovery (40% packet restoration).

14:46:00: Surge in authentication requests (318/AIR); other types decline.

14:47:30: Tunnel creation rate drops.

14:48:00: Gateway B congestion resolved.

14:49:00: Core router hits 2900 msg/s; traffic stabilizes at this peak.

Decision made to follow emergency escalation protocol due to pattern resemblance to prior major incident.

14:54:00: First monitoring alert received.

15:00:00: Ticket created via external support portal (#40645).

15:01:00: External party acknowledges receipt.

15:10:00: Direct call to ensure prioritization; confirmed ongoing.

15:23:00: Joint meeting scheduled with vendor and partners.

15:27:00: Full block applied to device identifier ranges (Protocol B).

15:30:00: All parties present in coordination call.

15:35:00: Debated whether to block Protocol A; ultimately not done.

15:37:00: Begin lifting identifier blocks.

15:45:00: Full unblock completed.

Post-Incident Review
Root Cause:
Prolonged packet loss on critical transport path.

Secondary Issues:
Transport layer saturation triggered congestion control mechanisms. Although local systems managed load effectively, broader ecosystem responses (e.g., retransmits) necessitated stricter traffic management.

Recovery:
Protocol B traffic blocked/unblocked collaboratively. External partner initiated block prematurely.

Preventative Measures:
New core database throttling logic deployed and under test—intended to prioritize device onboarding across all regional replicas.
Please analyze the conversation and provide a structured summary suitable for a postmortem report."""


class BedrockClient:
    def __init__(self, aws_profile, region_name="us-east-1", model_id=DEFAULT_MODEL_ID):
        self.session = boto3.Session(profile_name=aws_profile, region_name=region_name)
        self.client = self.session.client("bedrock-runtime")
        self.model_id = model_id

    def chat(self, conversation):
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=conversation,
                system=[{"text": POSTMORTEM_SUMMARY_PROMPT}],
            )
            return response["output"]["message"]
        except ClientError as e:
            raise Exception(f"An error occurred: {e.response['Error']['Message']}")

    def create_postmortem_summary(self, incident_conversation):
        conversation = [
            {
                "role": "user",
                "content": [
                    {
                        "text": f"Here is the incident conversation with timestamps:\n\n{incident_conversation}"
                    }
                ],
            }
        ]
        return self.chat(conversation)
