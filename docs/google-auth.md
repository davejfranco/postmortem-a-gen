## 🛠️ Google API Integration Guide with Service Account Impersonation
### Overview
This guide sets up:

A Service Account with domain-wide delegation

Required Google APIs

OAuth Scopes & Permissions for impersonation

Code snippet to impersonate a user

### ✅ STEP 1: Enable Required APIs
Go to the Google Cloud Console

Select your project (or create a new one)

Navigate to APIs & Services → Library

Enable each API you need:

Google Drive API

Google Docs API


### ✅ STEP 2: Create a Service Account
Go to IAM & Admin → Service Accounts

Click “Create Service Account”

Name: drive-docs-service-account

ID: e.g., drive-docs-sa

Description: Service account for API access via impersonation

Click Create and Continue

Assign Editor role
Click Done

### ✅ STEP 3: Enable Domain-Wide Delegation
In the service account list, click the name of your new service account

Go to the “Details” tab

Click “Advance settings”

Copy the Domain-Wide Delegation Client ID

✅ STEP 4: Authorize the Service Account in Admin Console
Open https://admin.google.com

Navigate to:

Security → Access and Data Control → API Controls → Domain-Wide Delegation

Click “Add new”

Input:

Client ID = (from Step 3)

OAuth Scopes = comma-separated list of API scopes

These are the scopes we need for this app:

"https://www.googleapis.com/auth/drive",
"https://www.googleapis.com/auth/documents.readonly",

Click Authorize
