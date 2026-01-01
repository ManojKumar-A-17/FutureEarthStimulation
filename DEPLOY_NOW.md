# 🚀 Deployment Manual: Render (Backend) + Vercel (Frontend)

This guide is tailored specifically for your project structure. Follow these steps exactly.

## Part 1: Deploy Backend to Render.com

1.  **Push to GitHub**: Make sure your latest code is pushed to your GitHub repository.
2.  **Create Service**:
    *   Log in to **[dashboard.render.com](https://dashboard.render.com)**.
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub repository.
3.  **Configuration**:
    *   **Name**: `future-earth-backend` (or similar)
    *   **Root Directory**: `backend` (⚠️ IMPORTANT)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4.  **Environment Variables** (Scroll down to "Environment Variables"):
    *   `PYTHON_VERSION`: `3.10.12`
    *   `EARTH_ENGINE_PROJECT`: `valiant-well-482105-n5`
    *   `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Paste the **entire content** of your Google Service Account JSON file here. (The one you download from Google Cloud Console).
5.  **Click "Create Web Service"**.
6.  **Wait**: It will take a few minutes. Once it's live, copy the URL (e.g., `https://future-earth-backend.onrender.com`).

---

## Part 2: Deploy Frontend to Vercel

1.  **Create Project**:
    *   Log in to **[vercel.com](https://vercel.com)**.
    *   Click **"Add New..."** -> **"Project"**.
    *   Import the same GitHub repository.
2.  **Configure Project**:
    *   **Framework Preset**: It should auto-detect `Vite`.
    *   **Root Directory**: Click "Edit" and select `frontend`. (⚠️ IMPORTANT)
3.  **Environment Variables**:
    *   Expand the "Environment Variables" section.
    *   Key: `VITE_BACKEND_URL`
    *   Value: The URL you copied from Render (e.g., `https://future-earth-backend.onrender.com`). **Do not add a trailing slash `/`.**
4.  **Click "Deploy"**.

## Part 3: Verify

1.  Open your new Vercel website URL.
2.  The map should load.
3.  Try selecting "India" or "Greenland" to run a simulation.
4.  If it works, congratulations! Your AI Earth Simulator is live for the world. 🌍

### ⚠️ Troubleshooting
*   **"Backend Disconnected"**: Check if your Render service is actually "Live". Free tier Render spins down after inactivity; it might take 50 seconds to wake up on the first request.
*   **"Earth Engine Error"**: Check your `GOOGLE_APPLICATION_CREDENTIALS_JSON` in Render. It must be the *exact* JSON string, including curly braces `{}`.
