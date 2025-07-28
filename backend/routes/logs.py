
from fastapi import APIRouter, Depends, Request, Body, HTTPException
import db.mongodb as mongodb
from db.models import AlarmLogIn, PredictionOut, ExplanationOut
from main import api_key_auth, limiter
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["logs"])

@router.get("/logs", response_model=dict)
@limiter.limit("10/minute")
async def get_logs(request: Request, _=Depends(api_key_auth)):
    logs = await mongodb.safe_find(
        mongodb.logs_collection, 
        sort_list=[("timestamp", -1)], 
        limit_count=100
    )
    predictions = await mongodb.safe_find(
        mongodb.predictions_collection, 
        sort_list=[("predicted_at", -1)], 
        limit_count=100
    )
    explanations = await mongodb.safe_find(
        mongodb.explanations_collection, 
        sort_list=[("generated_at", -1)], 
        limit_count=100
    )
    return {
        "logs": logs,
        "predictions": predictions,
        "explanations": explanations
    }

# Add POST endpoint for alarm log submission
@router.post("/logs")
@limiter.limit("10/minute")
async def post_log(request: Request, log: dict = Body(...), _=Depends(api_key_auth)):
    # Optionally validate with AlarmLogIn, but allow raw dict for flexibility
    try:
        # If you want strict validation, uncomment:
        # log_obj = AlarmLogIn(**log)
        # log = log_obj.dict()
        if "timestamp" not in log:
            from datetime import datetime
            log["timestamp"] = datetime.utcnow().isoformat()
        result = await mongodb.logs_collection.insert_one(log)
        return JSONResponse(status_code=201, content={"inserted_id": str(result.inserted_id)})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to insert log: {e}")