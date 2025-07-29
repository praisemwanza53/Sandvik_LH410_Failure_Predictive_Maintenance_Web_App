
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


# POST /api/alarm: Accepts AlarmLogIn, stores log, triggers prediction, returns log and prediction

from db.models import AlarmLogIn, PredictionOut
from core.model import predictor
from utils.preprocessing import validate_alarm_data
from datetime import datetime
from bson import ObjectId

def fix_mongo_ids(doc):
    if isinstance(doc, list):
        return [fix_mongo_ids(d) for d in doc]
    if isinstance(doc, dict):
        return {k: (str(v) if isinstance(v, ObjectId) else fix_mongo_ids(v)) for k, v in doc.items()}
    return doc

@router.post("/alarm", response_model=dict)
@limiter.limit("10/minute")
async def post_alarm_log(alarm_log: AlarmLogIn, request: Request, _=Depends(api_key_auth)):
    try:
        # Validate and prepare features
        alarm_data = validate_alarm_data(alarm_log.dict())
        # Make prediction
        prediction_result = predictor.predict_failure(alarm_data)
        prediction_result["predicted_at"] = datetime.utcnow().isoformat()
        prediction_result["model_version"] = "optimized_v1"
        # Store log and prediction in database
        alarm_log_dict = alarm_log.dict()
        alarm_log_dict["timestamp"] = alarm_log_dict.get("timestamp") or datetime.utcnow().isoformat()
        await mongodb.safe_insert_one(mongodb.logs_collection, alarm_log_dict)
        await mongodb.safe_insert_one(mongodb.predictions_collection, {
            **prediction_result,
            "alarm_log": alarm_log_dict
        })
        return fix_mongo_ids({"log": alarm_log_dict, "prediction": prediction_result})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process alarm log: {e}")

# GET /api/predictions: Return latest predictions
@router.get("/predictions", response_model=list)
@limiter.limit("10/minute")
async def get_predictions(request: Request, _=Depends(api_key_auth)):
    preds = await mongodb.safe_find(
        mongodb.predictions_collection,
        sort_list=[("predicted_at", -1)],
        limit_count=100
    )
    return fix_mongo_ids(preds)

# GET /api/insights: Return latest explanations
@router.get("/insights", response_model=list)
@limiter.limit("10/minute")
async def get_insights(request: Request, _=Depends(api_key_auth)):
    insights = await mongodb.safe_find(
        mongodb.explanations_collection,
        sort_list=[("generated_at", -1)],
        limit_count=100
    )
    return fix_mongo_ids(insights)