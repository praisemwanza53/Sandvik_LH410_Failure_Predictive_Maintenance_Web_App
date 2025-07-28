from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class AlarmLogIn(BaseModel):
    alarm_type: str = Field(..., max_length=100)
    spn: int
    fmi: int
    count: int
    hours: float
    component: str = Field(..., max_length=100)
    severity: Optional[str] = "medium"
    location: Optional[str] = "front"
    timestamp: Optional[str] = None

class FailurePrediction(BaseModel):
    probability: float
    risk_level: str

class OverallRisk(BaseModel):
    probability: float
    risk_level: str
    hours_to_failure: float

class PredictionOut(BaseModel):
    predictions: Dict[str, FailurePrediction]
    overall_risk: OverallRisk
    component: str
    timestamp: str
    predicted_at: str
    model_version: Optional[str] = None

class ExplanationOut(BaseModel):
    explanation: str
    recommendation: Optional[str] = None
    generated_at: datetime 