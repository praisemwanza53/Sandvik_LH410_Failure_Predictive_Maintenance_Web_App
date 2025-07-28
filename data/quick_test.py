#!/usr/bin/env python3
"""
Quick test script for optimized models
Simple validation that models work correctly
"""

import sys
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

try:
    from core.model import OptimizedPredictor
    
    print("🧪 QUICK MODEL TEST")
    print("=" * 30)
    
    # Initialize predictor
    print("Loading models...")
    predictor = OptimizedPredictor()
    
    if len(predictor.models) == 0:
        print("❌ No models loaded!")
        sys.exit(1)
    
    print(f"✅ Loaded {len(predictor.models)} models")
    
    # Test with sample data
    sample_alarm = {
        "alarm_type": "engine_temperature_high",
        "component": "engine",
        "severity": "high",
        "location": "front",
        "spn": 110,
        "fmi": 3,
        "count": 5,
        "hours": 1250.5,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    print("\nTesting prediction...")
    result = predictor.predict_failure(sample_alarm)
    
    print("✅ Prediction successful!")
    print(f"Component: {result['component']}")
    print(f"Overall risk: {result['overall_risk']['risk_level']} ({result['overall_risk']['probability']:.3f})")
    print(f"Hours to failure: {result['overall_risk']['hours_to_failure']:.1f}")
    
    print("\nIndividual failure predictions:")
    for failure_type, pred in result['predictions'].items():
        print(f"  {failure_type}: {pred['risk_level']} ({pred['probability']:.3f})")
    
    print("\n🎉 Quick test passed! Models are working correctly.")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1) 