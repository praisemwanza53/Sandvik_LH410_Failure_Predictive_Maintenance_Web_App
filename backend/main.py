# Ensure this file is run from the backend directory
import os
if not os.path.exists('main.py') or not os.path.exists('config.py'):
    raise RuntimeError("Run 'uvicorn main:app --reload' from the backend directory, not the project root.")



from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

app = FastAPI(title="Sandvik LH410 Failure Predictor API")

# Universal import block for local and deployment
try:
    from backend.config import Config
    from backend.db import mongodb
except ImportError:
    from config import Config
    import db.mongodb as mongodb


config = Config()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Log Groq API key presence
if config.GROQ_API_KEY:
    logging.info("GROQ_API_KEY is present in backend/config.py")
else:
    logging.warning("GROQ_API_KEY is NOT present in backend/config.py")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key for authentication
API_KEY = config.API_KEY

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# TEMPORARY: Optional API Key Auth Dependency (disabled for testing)
def api_key_auth(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    # Skip authentication for testing
    return True
    # Uncomment below to re-enable authentication
    # if not credentials or credentials != API_KEY:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")


# Include routes
from routes import predict, explain, logs
app.include_router(predict.router)
app.include_router(explain.router)
app.include_router(logs.router)

# --- PATCH: Override /api/alarm to generate and store AI Insights automatically ---
from fastapi import Request
from routes.predict import router as predict_router
try:
    from backend.core import llm
except ImportError:
    import core.llm as llm
from fastapi import APIRouter

alarm_router = APIRouter()

@alarm_router.post("/api/alarm")
async def alarm_predict(request: Request):
    """Predict failure and generate/store AI Insights automatically."""
    try:
        payload = await request.json()
        # Call the original prediction logic
        response = await predict_router.routes[0].endpoint(payload)
        prediction = response
        # Generate AI Insights from prediction
        insights = generate_insights(prediction)
        # Store insights in MongoDB
        db = getattr(mongodb, "get_database", None)
        if callable(db):
            database = db()
        else:
            database = mongodb.client[config.MONGODB_DB]
        insights_collection = database["insights"]
        if hasattr(insights_collection, "insert_one") and callable(insights_collection.insert_one):
            result = insights_collection.insert_one({"insights": insights})
            if hasattr(result, "__await__"):
                result = await result
        # Return both prediction and insights
        return {"prediction": prediction, "insights": insights}
    except Exception as e:
        print("Error in alarm_predict:", e)
        return {"status": "error", "detail": str(e)}

app.include_router(alarm_router)

@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection on startup"""
    await mongodb.connect_to_mongodb()

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    await mongodb.close_mongodb_connection()


# Add /api/insights endpoint to accept POST requests from frontend

from fastapi import Body
@app.post("/api/insights")
async def receive_insights(insights: dict = Body(...)):
    """Store received AI insights in MongoDB"""
    try:
        db = getattr(mongodb, "get_database", None)
        if callable(db):
            database = db()
        else:
            database = mongodb.client[config.MONGODB_DB]
        insights_collection = database["insights"]
        # Await the insert operation if using Motor (async MongoDB driver)
        if hasattr(insights_collection, "insert_one") and callable(insights_collection.insert_one):
            result = insights_collection.insert_one(insights)
            if hasattr(result, "__await__"):
                result = await result
            inserted_id = getattr(result, "inserted_id", None)
        else:
            inserted_id = None
        print("Received and stored AI insights:", insights)
        return {"status": "received", "inserted_id": str(inserted_id) if inserted_id else None}
    except Exception as e:
        print("Error storing AI insights:", e)
        return {"status": "error", "detail": str(e)}
@app.get("/v1/models")
async def dummy_models():
    """Dummy endpoint to silence frontend 404 errors."""
    return {"models": []}

@app.get("/api/insights")
async def get_insights():
    """Fetch all AI insights from MongoDB"""
    try:
        db = getattr(mongodb, "get_database", None)
        if callable(db):
            database = db()
        else:
            database = mongodb.client[config.MONGODB_DB]
        insights_collection = database["insights"]
        # Use async find if using Motor
        if hasattr(insights_collection, "find") and callable(insights_collection.find):
            cursor = insights_collection.find({}, {"_id": 0})
            if hasattr(cursor, "to_list") and callable(cursor.to_list):
                insights = await cursor.to_list(length=100)
            else:
                insights = list(cursor)
        else:
            insights = []
        return insights
    except Exception as e:
        print("Error fetching AI insights:", e)
        return {"status": "error", "detail": str(e)}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}