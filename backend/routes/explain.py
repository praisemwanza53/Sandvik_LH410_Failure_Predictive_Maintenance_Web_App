from fastapi import APIRouter, Depends, Request
from db.models import AlarmLogIn, PredictionOut, ExplanationOut
from core.llm import get_llm_explanation
import db.mongodb as mongodb
from main import api_key_auth, limiter
from datetime import datetime

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