# Sandvik LH410 Failure Predictor Backend

## Setup

1. Create a `.env` file (see `.env` template).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables
- `MONGODB_URI`: MongoDB connection string
- `GROQ_API_KEY`: Groq LLM API key
- `FRONTEND_ORIGIN`: Allowed CORS origin
- `API_KEY`: Backend API key for protected routes

## Endpoints
- `GET /api/health`: Health check
- `POST /api/predict`: Predict failure
- `POST /api/explain`: LLM explanation
- `GET /api/logs`: Historical logs 