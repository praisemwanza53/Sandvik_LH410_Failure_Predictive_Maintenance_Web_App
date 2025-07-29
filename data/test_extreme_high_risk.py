#!/usr/bin/env python3
"""
Test script for extreme high-risk, imminent failure predictions
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from core.model import OptimizedPredictor

def create_extreme_alarm_data():
    """Create alarm data likely to trigger very high risk and low hours to failure"""
    now = datetime.utcnow()
    return [
        {
            "alarm_type": "engine_temperature_critical",
            "component": "engine",
            "severity": "critical",
            "location": "front",
            "spn": 110,
            "fmi": 1,
            "count": 50,  # very high count
            "hours": 5000.0,  # high operational hours
            "timestamp": now.isoformat()
        },
        {
            "alarm_type": "brake_pressure_zero",
            "component": "brake",
            "severity": "critical",
            "location": "rear",
            "spn": 121,
            "fmi": 1,
            "count": 40,
            "hours": 4800.0,
            "timestamp": (now - timedelta(minutes=5)).isoformat()
        },
        {
            "alarm_type": "transmission_oil_temp_extreme",
            "component": "transmission",
            "severity": "critical",
            "location": "front",
            "spn": 95,
            "fmi": 2,
            "count": 35,
            "hours": 4700.0,
            "timestamp": (now - timedelta(minutes=10)).isoformat()
        },
        {
            "alarm_type": "electrical_voltage_zero",
            "component": "electrical",
            "severity": "critical",
            "location": "front",
            "spn": 168,
            "fmi": 4,
            "count": 30,
            "hours": 4600.0,
            "timestamp": (now - timedelta(minutes=15)).isoformat()
        }
    ]

def main():
    print("\n=== TESTING EXTREME HIGH-RISK PREDICTIONS ===")
    predictor = OptimizedPredictor()
    extreme_data = create_extreme_alarm_data()
    for i, alarm_data in enumerate(extreme_data):
        print(f"\n--- Extreme Test Case {i+1}: {alarm_data['alarm_type']} ---")
        prediction = predictor.predict_failure(alarm_data)
        if 'overall_risk' in prediction:
            print(f"   Component: {prediction['component']}")
            print(f"   Overall risk: {prediction['overall_risk']['risk_level']} ({prediction['overall_risk']['probability']:.3f})")
            print(f"   Hours to failure: {prediction['overall_risk']['hours_to_failure']:.1f}")
            for failure_type, result in prediction['predictions'].items():
                print(f"   {failure_type}: {result['risk_level']} ({result['probability']:.3f})")
        else:
            print(f"❌ Prediction failed or missing 'overall_risk': {prediction}")

if __name__ == "__main__":
    main()
