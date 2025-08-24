import boto3
from botocore.exceptions import ClientError


POSTMORTEM_SUMMARY_PROMPT = """You are a Site Reliability Engineer tasked with creating postmortem report summaries. 

You'll be given a conversation with timestamps about an incident, like this:
```
[{'user': 'Dave Franco', 'text': 'Oh shit we're experiencing an issue, 'ts': '2025-07-30 21:00:18'}, 
{'user': 'Dave Franco', 'text': 'I'm checking servers, it appears there is a lot of request latency', 'ts': '2025-07-30 21:00:47'}, 
{'user': 'Dave Franco', 'text': 'I'm checking DB', 'ts': '2025-07-30 21:01:00'}, 
{'user': 'Dave Franco', 'text': 'it seems we have missing indexes', 'ts': '2025-07-30 21:01:18'}]
```
Generate a summary report. It needs to contain the following sections:

1. Title: Portmortem Summary (Preview)
2. Impacted Components
3. Detailed Timeline
4. Post Incident Review: Root cause
5. Secondary Issue: if any
6. Recovery
7. Preventive Measures

Note: translate to english if input in different language

To format I want you to follow this instructions.
- Start Title with `## `
- Each section with `### `

As Example:
## Postmortem Summary (Preview)
Increase request latency due to missing database indexes
### Impacted Components:

- App servers 
- Database

### Detailed Timeline
2025-07-30 21:00:18 - System experiencing request latency 
2025-07-30 21:00:47 - On-call Engineer checking servers 
2025-07-30 21:01:00 - On-call Engineer checking Database 
2025-07-30 21:01:18 - On-call Engineer has identified missing indexes in the Database

### Post-Incident Review
Root Cause:
Increase request latency due to missing DB indexes

### Secondary Issues:


### Recovery:
Add missing indexes

### Preventative Measures:
Make sure we have index where data is requested frequently"""


class Bedrock:
    def __init__(self, aws_profile, region_name, model_id):
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
