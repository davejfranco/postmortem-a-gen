# Postmortem Reports Generator

A Python tool that uses AWS Bedrock and Claude to automatically generate postmortem report summaries from incident conversations.

## Features

- **AWS Bedrock Integration**: Uses Claude 3.5 Sonnet via AWS Bedrock for AI-powered analysis
- **Postmortem Generation**: Converts incident conversations with timestamps into structured postmortem reports
- **Flexible Configuration**: Supports custom AWS profiles, regions, and model selection
- **Structured Output**: Generates reports with timeline, impact analysis, root cause, and action items

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from bedrock import BedrockClient

# Initialize client with AWS profile
client = BedrockClient(aws_profile='your-profile')

# Generate postmortem from incident conversation
incident_conversation = """
[2024-01-15 14:30] Alert: Database connection timeout
[2024-01-15 14:32] Engineer: Investigating connection issues
[2024-01-15 14:45] Engineer: Found high CPU usage on DB server
[2024-01-15 15:00] Engineer: Restarted database service, issue resolved
"""

summary = client.create_postmortem_summary(incident_conversation)
print(summary)
```

### Advanced Configuration

```python
# Custom region and model
client = BedrockClient(
    aws_profile='production',
    region_name='us-west-2',
    model_id='anthropic.claude-3-haiku-20240307-v1:0'
)

# Direct chat interface
conversation = [
    {"role": "user", "content": [{"text": "Analyze this incident..."}]}
]
response = client.chat(conversation)
```

## Configuration

### AWS Setup

1. Configure AWS credentials with Bedrock access
2. Ensure your AWS profile has permissions for `bedrock-runtime:InvokeModel`

### Environment

- Python 3.8+
- AWS CLI configured
- Valid AWS profile with Bedrock permissions

## Output Format

The postmortem summary includes:

- **Incident Overview**: Brief description of what happened
- **Timeline**: Key events with timestamps
- **Impact**: Affected systems and users
- **Root Cause**: Primary cause identification
- **Resolution**: How the incident was resolved
- **Action Items**: Follow-up tasks to prevent recurrence

## Files

- `bedrock.py`: Main BedrockClient class and postmortem generation logic
- `main.py`: Application entry point
- `slack.py`: Slack integration utilities