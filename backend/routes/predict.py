from fastapi import APIRouter, Depends, Request, HTTPException
from db.models import AlarmLogIn, PredictionOut
from utils.preprocessing import clean_and_prepare_features, validate_alarm_data
from core.model import predictor
import db.mongodb as mongodb
from main import api_key_auth, limiter
from datetime import datetime
from typing import Dict, Any

router = APIRouter(prefix="/api", tags=["predict"])

@router.post("/predict", response_model=PredictionOut)
@limiter.limit("5/minute")
async def predict_failure(
    alarm_log: AlarmLogIn,
    request: Request,
    _=Depends(api_key_auth)
):
    """Predict failure probabilities for all failure types"""
    try:
        # Validate and prepare features
        alarm_data = validate_alarm_data(alarm_log.dict())
        
        # Make prediction using optimized models
        prediction_result = predictor.predict_failure(alarm_data)
        
        # Add metadata
        prediction_result["predicted_at"] = datetime.utcnow().isoformat()
        prediction_result["model_version"] = "optimized_v1"
        
        # Store log and prediction in database
        alarm_log_dict = alarm_log.dict()
        alarm_log_dict["timestamp"] = alarm_log_dict.get("timestamp") or datetime.utcnow().isoformat()
        
        # Store in database using safe operations
        await mongodb.safe_insert_one(mongodb.logs_collection, alarm_log_dict)
        await mongodb.safe_insert_one(mongodb.predictions_collection, {
            **prediction_result, 
            "alarm_log": alarm_log_dict
        })
        
        return prediction_result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/predict/health")
async def health_check():
    """Health check endpoint for the prediction service"""
    try:
        # Check if models are loaded
        model_count = len(predictor.models)
        if model_count == 0:
            return {
                "status": "unhealthy",
                "message": "No models loaded",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        return {
            "status": "healthy",
            "models_loaded": model_count,
            "model_types": list(predictor.models.keys()),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@router.post("/predict/batch")
@limiter.limit("2/minute")
async def predict_failure_batch(
    alarm_logs: list[AlarmLogIn],
    request: Request,
    _=Depends(api_key_auth)
):
    """Predict failure probabilities for multiple alarm logs"""
    try:
        if len(alarm_logs) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 alarm logs per batch")
        
        results = []
        for alarm_log in alarm_logs:
            try:
                alarm_data = validate_alarm_data(alarm_log.dict())
                prediction_result = predictor.predict_failure(alarm_data)
                prediction_result["alarm_id"] = alarm_log.dict().get("id", "unknown")
                results.append(prediction_result)
            except Exception as e:
                results.append({
                    "alarm_id": alarm_log.dict().get("id", "unknown"),
                    "error": str(e),
                    "predictions": {},
                    "overall_risk": {"probability": 0, "risk_level": "error"}
                })
        
        return {
            "batch_results": results,
            "total_processed": len(results),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}") 