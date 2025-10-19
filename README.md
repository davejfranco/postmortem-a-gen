# Postmortems Reports

A Slack app that automatically generates postmortem reports from Slack thread conversations using AWS Bedrock AI and saves them to Google Drive.

## Overview

This service listens for Slack slash commands, fetches thread conversations, generates structured postmortem reports using AI, and creates Google Docs in a specified Google Drive folder.

## Features

- **Slack Integration**: Slash command interface to trigger postmortem generation from thread URLs
- **AI-Powered Analysis**: Uses AWS Bedrock to analyze conversation threads and generate structured postmortem reports
- **Google Drive Export**: Automatically creates and saves reports as Google Docs
- **Background Processing**: Asynchronous report generation to avoid blocking Slack responses
- **Health Monitoring**: Built-in health check endpoint for service monitoring

## Architecture

```
┌──────────┐    Slash Command    ┌─────────────┐
│  Slack   │ ───────────────────> │   FastAPI   │
│          │ <─────────────────── │   Service   │
└──────────┘    Confirmation      └─────────────┘
                                         │
                                         │ Background Task
                                         ▼
                            ┌────────────────────────┐
                            │    Orchestrator        │
                            └────────────────────────┘
                                    │      │      │
                        ┌───────────┘      │      └───────────┐
                        ▼                  ▼                  ▼
                  ┌─────────┐      ┌──────────┐      ┌─────────────┐
                  │  Slack  │      │   AWS    │      │   Google    │
                  │   SDK   │      │ Bedrock  │      │    Docs     │
                  └─────────┘      └──────────┘      └─────────────┘
```

## Requirements

- Python 3.13+
- AWS account with Bedrock access
- Slack workspace with app configured
- Google Cloud project with Drive and Docs API enabled

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd postmortems-reports
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The application uses environment variables for configuration. Set the following:

### Slack Configuration
- `SLACK_BOT_TOKEN`: Slack bot OAuth token
- `SLACK_CHANNEL_ID`: Default channel ID for thread retrieval

### AWS Configuration
- `AWS_PROFILE`: AWS profile name (optional)
- `AWS_REGION`: AWS region (e.g., us-east-1)
- `AWS_BEDROCK_MODEL_ID`: Bedrock model ID to use

### Google Configuration
- `GOOGLE_CREDENTIALS`: JSON string of Google service account credentials
- `GOOGLE_DRIVE_FOLDER_ID`: Target folder ID for created documents

See `docs/google-auth.md` for Google authentication setup details.

## Usage

### Running Locally

```bash
fastapi dev app/main.py
```

The service will start on `http://localhost:8000`.

### Running with Docker

```bash
docker build -t postmortems-reports .
docker run -p 8000:8000 --env-file .env postmortems-reports
```

### Slack Command

In your Slack workspace, use the configured slash command:

```
/postmortem <thread_url>
```

The bot will:
1. Acknowledge the command
2. Fetch the thread conversation
3. Generate an AI-powered postmortem report
4. Create a Google Doc with the report
5. Save it to the configured Google Drive folder

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /slack/event_verification`: Slack URL verification
- `POST /slack/mention`: Slash command handler

## Deployment

The project includes Kubernetes manifests in the `k8s/` directory and Terraform configuration in the `infra/` directory for AWS infrastructure provisioning.

## Development

### Running Tests

```bash
pytest
```

### Project Structure

```
app/
├── handlers/       # API routes and request handlers
├── services/       # Business logic (Slack, Bedrock, Google integrations)
└── utils/          # Configuration and utilities
```

## License

MIT License - free to use, modify, and distribute.
