from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from db.models import AlarmLogIn, PredictionOut, ExplanationOut
from core.llm import get_llm_explanation
import db.mongodb as mongodb
from main import api_key_auth, limiter
from datetime import datetime
import logging

router = APIRouter(prefix="/api", tags=["explain"])

class ExplainIn(AlarmLogIn, PredictionOut):
    pass

@router.post("/explain", response_model=ExplanationOut)
@limiter.limit("5/minute")
async def explain_prediction(
    explain_in: ExplainIn,
    request: Request,
    _=Depends(api_key_auth)
):
    # Compose dicts for LLM
    alarm = explain_in.dict()
    prediction = {
        "probability": explain_in.overall_risk.probability,
        "hours_to_failure": explain_in.overall_risk.hours_to_failure,
        "component": explain_in.component
    }
    explanation = await get_llm_explanation(prediction, alarm)
    await mongodb.safe_insert_one(mongodb.explanations_collection, {
        **explanation, 
        "alarm_log": alarm, 
        "prediction": prediction
    })
    return explanation

@router.get("/test_groq")
async def test_groq_api(_=Depends(api_key_auth)):
    # Simple test prompt
    #test_prompt = "What is the capital of France?"
    
    # Dummy data for prediction and alarm
    prediction = {"component": "Test", "probability": 0.5, "hours_to_failure": 100}
    alarm = {"alarm_type": "Test Alarm", "spn": 123, "fmi": 4}

    try:
        explanation = await get_llm_explanation(prediction, alarm)
        return JSONResponse(content=explanation, status_code=200)
    except Exception as e:
        logging.exception(f"Error in /api/test_groq endpoint: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)