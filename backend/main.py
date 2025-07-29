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

app = FastAPI(title="Sandvik LH410 Failure Predictor API")

# Universal import block for local and deployment
try:
    from backend.config import Config
    from backend.db import mongodb
except ImportError:
    from config import Config
    import db.mongodb as mongodb


config = Config()

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
    # if not credentials or credentials.credentials != API_KEY:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")

# Include routes
from routes import predict, explain, logs
app.include_router(predict.router)
app.include_router(explain.router)
app.include_router(logs.router)

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
    # You can log, store, or process insights here
    print("Received AI insights:", insights)
    return {"status": "received"}

@app.get("/api/insights")
async def get_insights():
    """Fetch all AI insights from MongoDB"""
    # Ensure insights_collection is defined (replace 'your_collection_name' with the actual collection name)
    insights_collection = mongodb.database["insights"]  # Use the correct collection name if different
    insights = list(insights_collection.find({}, {"_id": 0}))
    return insights

@app.get("/api/health")
def health_check():
    return {"status": "ok"}