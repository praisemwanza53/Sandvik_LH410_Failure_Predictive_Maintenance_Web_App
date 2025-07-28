from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config import config
import db.mongodb as mongodb

app = FastAPI(title="Sandvik LH410 Failure Predictor API")

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

@app.get("/api/health")
def health_check():
    return {"status": "ok"} 