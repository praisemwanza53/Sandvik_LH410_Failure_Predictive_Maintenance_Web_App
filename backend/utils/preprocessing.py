import pandas as pd
from typing import Dict, Any
from datetime import datetime

def clean_and_prepare_features(alarm_log: dict) -> dict:
    """Clean and prepare alarm log data for prediction"""
    # Basic sanitization and feature extraction
    features = {
        "alarm_type": str(alarm_log.get("alarm_type", "")).strip(),
        "spn": int(alarm_log.get("spn", 0)),
        "fmi": int(alarm_log.get("fmi", 0)),
        "count": int(alarm_log.get("count", 1)),
        "hours": float(alarm_log.get("hours", 0.0)),
        "component": str(alarm_log.get("component", "")).strip(),
        "severity": str(alarm_log.get("severity", "medium")).strip(),
        "location": str(alarm_log.get("location", "front")).strip(),
        "timestamp": alarm_log.get("timestamp", datetime.utcnow().isoformat())
    }
    
    # Validate and clean data
    if features["count"] < 1:
        features["count"] = 1
    if features["hours"] < 0:
        features["hours"] = 0.0
    
    return features

def validate_alarm_data(alarm_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize incoming alarm data"""
    required_fields = ["alarm_type", "component"]
    optional_fields = {
        "spn": 0,
        "fmi": 0,
        "count": 1,
        "hours": 0.0,
        "severity": "medium",
        "location": "front",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Check required fields
    for field in required_fields:
        if field not in alarm_data or not alarm_data[field]:
            raise ValueError(f"Required field '{field}' is missing or empty")
    
    # Set default values for optional fields
    for field, default_value in optional_fields.items():
        if field not in alarm_data:
            alarm_data[field] = default_value
    
    # Clean and validate data types
    cleaned_data = clean_and_prepare_features(alarm_data)
    
    return cleaned_data

def extract_temporal_features(timestamp_str: str) -> Dict[str, Any]:
    """Extract temporal features from timestamp"""
    try:
        timestamp = pd.to_datetime(timestamp_str)
        return {
            "hour_of_day": timestamp.hour,
            "day_of_week": timestamp.weekday(),
            "month": timestamp.month,
            "is_weekend": 1 if timestamp.weekday() >= 5 else 0,
            "is_night_shift": 1 if 22 <= timestamp.hour or timestamp.hour <= 6 else 0
        }
    except Exception:
        # Return default values if timestamp parsing fails
        return {
            "hour_of_day": 12,
            "day_of_week": 0,
            "month": 1,
            "is_weekend": 0,
            "is_night_shift": 0
        } 