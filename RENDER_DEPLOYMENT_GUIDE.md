# Render Deployment Guide for Sandvik LH410 Failure Predictive Maintenance Web App

## Backend (FastAPI)
1. Push your code to GitHub.
2. On Render, create a new **Web Service**:
   - Connect your GitHub repo.
   - **Build Command:**
     ```sh
     pip install -r backend/requirements.txt
     ```
   - **Start Command:**
     ```sh
     uvicorn backend.main:app --host 0.0.0.0 --port 10000
     ```
   - **Environment Variables:**
     - `MONGODB_URI` (your MongoDB connection string)
     - `MONGODB_DB` (your DB name, e.g. sandvik_lh410)
     - `GROQ_API_KEY` (your Groq LLM key)
     - `FRONTEND_ORIGIN` (your frontend Render URL, e.g. https://your-frontend.onrender.com)
     - `API_KEY` (optional, for protected routes)
   - **Port:** 10000 (or your chosen port)

## Frontend (Vue)
1. On Render, create a new **Static Site**:
   - Connect your GitHub repo.
   - **Build Command:**
     ```sh
     cd frontend && npm install && npm run build
     ```
   - **Publish Directory:**
     ```
     frontend/dist
     ```
   - **Environment Variable:**
     - `VITE_BACKEND_URL` (your backend Render URL, e.g. https://your-backend.onrender.com)

## Docker (Alternative)
- If you want to deploy both together, use `docker-compose.yml` and create a Render Blueprint (YAML) or use another service that supports Docker Compose.

## Testing Your Deployment
- Visit your frontend Render URL. Submit a test alarm log.
- The dashboard should update with predictions, risk, and time before failure.
- Check `/api/docs` on your backend for API health.

## Troubleshooting
- Ensure all environment variables are set in Render dashboard.
- Check Render logs for errors.
- Make sure your frontend `.env` points to the deployed backend URL.

---
For more, see the main `README.md` or ask for help!
