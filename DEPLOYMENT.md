# 🌍 Deployment Guide for Alternate Earth Futures

This guide explains how to deploy your application to production. Since your app relies on **Google Earth Engine (GEE)**, the most important step is setting up authentication correctly for a remote server.

## 1. How the Data Works (IMPORTANT)
**You do NOT strictly "download" satellite data to your local disk.**
*   Code like `reduceRegion().getInfo()` sends a computation request to Google's Cloud.
*   Google processes terabytes of data on *their* servers.
*   They send back only the tiny summary (JSON) to your backend.
*   **Result:** You don't need a huge hard drive on your production server. A standard small server is fine.

---

## 2. Google Earth Engine Authentication (Production)
On your local machine, you used `earthengine authenticate` (browser login). This **will not work** on a cloud server (which has no browser).

### Step A: Create a Service Account
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Select your project (`valiant-well-482105-n5`).
3.  Go to **IAM & Admin** > **Service Accounts**.
4.  Click **Create Service Account**.
    *   Name: `earth-engine-bot`
    *   Role: **Earth Engine Resource Writer** (or Editor).
5.  Click **Done**.

### Step B: Generate Key
1.  Click on the newly created service account email.
2.  Go to "Keys" tab -> "Add Key" -> "Create new key" -> **JSON**.
3.  This downloads a `.json` file. **Keep this safe!**

### Step C: Register Service Account in Earth Engine
1.  Copy the service account email (e.g., `earth-engine-bot@valiant-well....iam.gserviceaccount.com`).
2.  Go to the [Earth Engine Console](https://code.earthengine.google.com/).
3.  Click your profile picture -> **Register a new Cloud Project** (if not done) OR ensure your project is registered.
4.  **Crucial:** Users often forget to give the service account permission. Ensure the service account email is added as a "Writer" or "Editor" in your Google Cloud IAM settings for the project.

---

## 3. Prepare Backend for Deployment
You need to modify your code slightly to use the Service Account if a specific environment variable is present.

### Update `.env` on Production Server
Set these environment variables on your cloud provider (Render/Railway/Heroku):
```bash
# Data from the JSON key you downloaded
GOOGLE_APPLICATION_CREDENTIALS_JSON='{ "type": "service_account", ... }' 
EARTH_ENGINE_PROJECT=valiant-well-482105-n5
PORT=8000
```

---

## 4. Deployment Options

### Option A: Render.com (Recommended for simplicity)
1.  **Backend:**
    *   Connect your GitHub repo.
    *   Build Command: `pip install -r requirements.txt`
    *   Start Command: `python run.py`
    *   **Env Vars:** Copy contents of `.env`, plus the `GOOGLE_APPLICATION_CREDENTIALS` logic (see below).

2.  **Frontend:**
    *   Connect repo as "Static Site".
    *   Build Command: `npm run build`
    *   Publish Directory: `dist`
    *   **Env Var:** `VITE_BACKEND_URL` = `https://your-backend-app.onrender.com`

---

## 5. Code Adjustment for Service Account
In `backend/app/main.py` (or `utils`), update the initialization logic to look like this (pseudo-code):

```python
import os
import json
from google.oauth2.service_account import Credentials
import ee

def init_ee():
    # Check if we have the JSON key in env vars (Production)
    service_account_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    
    if service_account_json:
        # Production: Use Service Account
        creds_dict = json.loads(service_account_json)
        creds = Credentials.from_service_account_info(creds_dict)
        ee.Initialize(credentials=creds, project=os.getenv("EARTH_ENGINE_PROJECT"))
    else:
        # Local: Use default browser login
        ee.Initialize(project=os.getenv("EARTH_ENGINE_PROJECT"))
```
