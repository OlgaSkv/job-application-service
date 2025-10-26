# Google Service Account Setup Instructions
## Job Application Service

---

## Overview

The Job Application Service uses a Google Cloud service account to:
- Access Google Sheets (read job descriptions, write tracking data)
- Access Google Drive (download resume, personal statement, candidate profile)

This guide walks through creating the service account and generating credentials.

---

## Prerequisites

- Google Cloud account (free tier is sufficient)
- Project created in Google Cloud Console
- Billing enabled (required for API access, but won't be charged on free tier)

---

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click: **Select a project** → **New Project**
3. Project name: `job-application-service` (or any name you prefer)
4. Click: **Create**
5. Wait for project creation (takes ~30 seconds)
6. Select your new project from the dropdown

---

### 2. Enable Required APIs

1. Go to: **APIs & Services** → **Library**
2. Search and enable the following APIs:
   - **Google Sheets API**
   - **Google Drive API**

For each API:
- Click on the API name
- Click: **Enable**
- Wait for activation

---

### 3. Create Service Account

1. Go to: **IAM & Admin** → **Service Accounts**
2. Click: **Create Service Account**
3. Fill in the details:
   - **Service account name**: `job-tracker` (or your preferred name)
   - **Service account ID**: Auto-generated (e.g., `job-tracker`)
   - **Description**: "Service account for Job Application Service automation"
4. Click: **Create and Continue**
5. **Grant access** (optional): Skip this step, click **Continue**
6. **Grant users access** (optional): Skip this step, click **Done**

**Result:** Service account created with email like:
```
YOUR-SERVICE-ACCOUNT-NAME@YOUR-PROJECT-ID.iam.gserviceaccount.com
```
**Save this email** - you'll need it to share Google Drive files and Sheets.

---

### 4. Generate Private Key (credentials.json)

1. In **Service Accounts** page, find your newly created account
2. Click on the service account name (opens detail page)
3. Go to the **Keys** tab
4. Click: **Add Key** → **Create new key**
5. Choose format: **JSON**
6. Click: **Create**

**Result:** A JSON file automatically downloads to your computer with a name like:
```
job-application-service-abc123def456.json
```

---

### 5. Save Credentials File

1. Rename the downloaded file to: `credentials.json`
2. Move it to your project root directory:
   ```
   job-tracker/
   └── credentials.json  ← Place here
   ```
3. **Verify .gitignore includes it**:
   ```
   # In .gitignore file:
   credentials.json
   ```

**⚠️ SECURITY WARNING:**
- NEVER commit `credentials.json` to version control
- NEVER share this file publicly
- Store securely - it's like a password for your Google account

---

### 6. Credentials File Structure

Your `credentials.json` should look like this:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "abc123def456...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIB...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

**Key Fields:**
- `client_email` - Use this to share Google Drive files and Sheets
- `private_key` - Auto-generated encryption key (never manually edit)
- `project_id` - Your Google Cloud project ID

---

## Grant Access to Google Resources

### For Google Sheets:

1. Open your Google Sheet (e.g., `JD_Saved`, `Job_Tracker`)
2. Click: **Share** button
3. Add email: `your-service-account@your-project-id.iam.gserviceaccount.com`
4. Permission: **Editor** (allows read and write)
5. Click: **Send**

### For Google Drive Files:

1. For each file (resume, personal_statement, candidate_profile):
2. Right-click file → **Share**
3. Add email: `your-service-account@your-project-id.iam.gserviceaccount.com`
4. Permission: **Viewer** (read-only is sufficient)
5. Click: **Done**

---

## Verify Setup

### Test Sheets Connection:

```bash
python tests/test_sheets_connection.py
```

Expected output:
```
Successfully connected to Google Sheets!
Found X rows in jd_saved sheet
```

### Test Drive Connection:

```bash
python tests/test_drive_connection.py
```

Expected output:
```
Successfully connected to Google Drive API!
All configured files accessible
```

### Manual Drive Test (Optional):

```python
from src.tools.google_drive_tool import GoogleDriveTool

drive = GoogleDriveTool("credentials.json")
# Test connection by listing accessible files
try:
    files = drive.service.files().list(pageSize=5).execute()
    print(f"Connected! Found access to Drive API")
except Exception as e:
    print(f"Drive connection failed: {e}")
```

---

## Troubleshooting

### Error: "API has not been used in project before"

**Solution:**
- Go to Google Cloud Console → APIs & Services → Library
- Enable Google Sheets API and Google Drive API

### Error: "The caller does not have permission"

**Solution:**
- Verify service account email is shared with your Sheets/Drive files
- Check permission level (Editor for Sheets, Viewer for Drive)

### Error: "Credentials file not found"

**Solution:**
- Verify `credentials.json` is in project root
- Check file name (must be exactly `credentials.json`)

### Error: "Invalid private key"

**Solution:**
- Delete old credentials.json
- Generate new key from Google Cloud Console
- Download fresh JSON file

---

## Key Rotation (Security Best Practice)

**When to rotate:**
- Every 90 days (recommended)
- If credentials are compromised
- When team member with access leaves

**How to rotate:**
1. Go to: Service Accounts → Keys tab
2. Click: **Add Key** → **Create new key**
3. Download new JSON file
4. Replace old `credentials.json` with new one
5. Delete old key from Google Cloud Console

---

## Cost & Limits

**Free Tier Includes:**
- Google Sheets API: 500 requests/100 seconds (free)
- Google Drive API: 1 billion queries/day (free)

**For this project:**
- Typical usage: ~50-100 API calls per job batch
- Well within free tier limits
- No charges expected for normal use

---

## Summary Checklist

- [ ] Created Google Cloud project
- [ ] Enabled Google Sheets API
- [ ] Enabled Google Drive API
- [ ] Created service account
- [ ] Downloaded credentials JSON file
- [ ] Renamed to `credentials.json`
- [ ] Saved in project root
- [ ] Verified in `.gitignore`
- [ ] Shared Google Sheets with service account (Editor)
- [ ] Shared Google Drive files with service account (Viewer)
- [ ] Tested connection with `python tests/test_sheets_connection.py`
- [ ] Tested file access with `python tests/test_drive_connection.py`
- [ ] Saved service account email for future reference

**Service Account Email:**
```
[Write your service account email here]
```

---

**Document Version:** 1.0  
**Last Updated:** October 17, 2025  
**Project:** Job Application Service  
**Author:** Setup Guide
