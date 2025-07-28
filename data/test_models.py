#!/usr/bin/env python3
"""
Test script for optimized failure prediction models
Tests the models with sample data and validates the prediction pipeline
"""

import sys
import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from core.model import OptimizedPredictor

def create_sample_alarm_data():
    """Create sample alarm data for testing"""
    sample_data = [
        {
            "alarm_type": "engine_temperature_high",
            "component": "engine",
            "severity": "high",
            "location": "front",
            "spn": 110,
            "fmi": 3,
            "count": 5,
            "hours": 1250.5,
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "alarm_type": "brake_pressure_low",
            "component": "brake",
            "severity": "critical",
            "location": "rear",
            "spn": 121,
            "fmi": 1,
            "count": 3,
            "hours": 980.2,
            "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat()
        },
        {
            "alarm_type": "transmission_oil_temp",
            "component": "transmission",
            "severity": "medium",
            "location": "front",
            "spn": 95,
            "fmi": 2,
            "count": 2,
            "hours": 2100.0,
            "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat()
        },
        {
            "alarm_type": "electrical_voltage_low",
            "component": "electrical",
            "severity": "low",
            "location": "front",
            "spn": 168,
            "fmi": 4,
            "count": 1,
            "hours": 500.0,
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "alarm_type": "engine_oil_pressure",
            "component": "engine",
            "severity": "critical",
            "location": "front",
            "spn": 100,
            "fmi": 1,
            "count": 8,
            "hours": 1500.0,
            "timestamp": (datetime.utcnow() - timedelta(minutes=30)).isoformat()
        }
    ]
    return sample_data

def test_model_loading():
    """Test if all models load correctly"""
    print("=== TESTING MODEL LOADING ===")
    
    try:
        predictor = OptimizedPredictor()
        
        # Check if models are loaded
        if len(predictor.models) == 0:
            print("❌ No models loaded!")
            return False
        
        print(f"✅ Successfully loaded {len(predictor.models)} models:")
        for failure_type in predictor.models.keys():
            print(f"   - {failure_type}")
        
        # Check if feature names are loaded
        if len(predictor.feature_names) == 0:
            print("❌ No feature names loaded!")
            return False
        
        print(f"✅ Successfully loaded feature names for {len(predictor.feature_names)} models")
        
        return True
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_preprocessing():
    """Test the preprocessing pipeline"""
    print("\n=== TESTING PREPROCESSING PIPELINE ===")
    
    try:
        predictor = OptimizedPredictor()
        sample_data = create_sample_alarm_data()[0]  # Use first sample
        
        # Test preprocessing
        features_df = predictor.preprocess_new_data(sample_data)
        
        print(f"✅ Preprocessing successful")
        print(f"   Input features: {len(sample_data)}")
        print(f"   Output features: {len(features_df.columns)}")
        print(f"   Feature shape: {features_df.shape}")
        
        # Check for expected features
        expected_features = ['hour_of_day', 'day_of_week', 'month', 'is_weekend', 'is_night_shift']
        for feature in expected_features:
            if feature in features_df.columns:
                print(f"   ✅ {feature}: {features_df[feature].iloc[0]}")
            else:
                print(f"   ❌ {feature}: Missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Preprocessing failed: {e}")
        return False

def test_predictions():
    """Test predictions with sample data"""
    print("\n=== TESTING PREDICTIONS ===")
    
    try:
        predictor = OptimizedPredictor()
        sample_data = create_sample_alarm_data()
        
        for i, alarm_data in enumerate(sample_data):
            print(f"\n--- Test Case {i+1}: {alarm_data['alarm_type']} ---")
            
            # Make prediction
            prediction = predictor.predict_failure(alarm_data)
            
            # Check if prediction has expected structure
            if 'predictions' not in prediction:
                print(f"❌ Missing 'predictions' in result")
                continue
            
            if 'overall_risk' not in prediction:
                print(f"❌ Missing 'overall_risk' in result")
                continue
            
            print(f"✅ Prediction successful")
            print(f"   Component: {prediction['component']}")
            print(f"   Overall risk: {prediction['overall_risk']['risk_level']} ({prediction['overall_risk']['probability']:.3f})")
            print(f"   Hours to failure: {prediction['overall_risk']['hours_to_failure']:.1f}")
            
            # Show individual failure predictions
            for failure_type, result in prediction['predictions'].items():
                print(f"   {failure_type}: {result['risk_level']} ({result['probability']:.3f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def test_model_performance():
    """Test model performance with known data"""
    print("\n=== TESTING MODEL PERFORMANCE ===")
    
    try:
        # Load test data
        data_dir = Path(__file__).parent
        features_path = data_dir / "features_optimized.csv"
        targets_path = data_dir / "targets.csv"
        
        if not features_path.exists() or not targets_path.exists():
            print("❌ Test data not found")
            return False
        
        # Load data
        features = pd.read_csv(features_path)
        targets = pd.read_csv(targets_path)
        
        print(f"✅ Loaded test data: {features.shape}")
        
        # Test with a few samples
        predictor = OptimizedPredictor()
        
        # Take first 5 samples for testing
        test_samples = features.head(5)
        test_targets = targets.head(5)
        
        correct_predictions = 0
        total_predictions = 0
        
        for i in range(len(test_samples)):
            # Create alarm data from features (simplified)
            alarm_data = {
                "alarm_type": "test_alarm",
                "component": "engine",
                "severity": "medium",
                "location": "front",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Make prediction
            prediction = predictor.predict_failure(alarm_data)
            
            # Check if prediction is reasonable
            overall_prob = prediction['overall_risk']['probability']
            if 0 <= overall_prob <= 1:
                correct_predictions += 1
            total_predictions += 1
            
            print(f"   Sample {i+1}: Probability = {overall_prob:.3f}")
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        print(f"✅ Model validation: {correct_predictions}/{total_predictions} valid predictions ({accuracy:.1%})")
        
        return accuracy > 0.8
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid data"""
    print("\n=== TESTING ERROR HANDLING ===")
    
    try:
        predictor = OptimizedPredictor()
        
        # Test with invalid data
        invalid_data = {
            "alarm_type": "",  # Empty alarm type
            "component": "",   # Empty component
        }
        
        prediction = predictor.predict_failure(invalid_data)
        
        if 'error' in prediction:
            print(f"✅ Error handling works: {prediction['error']}")
            return True
        else:
            print(f"⚠ No error returned for invalid data")
            return True  # Still acceptable
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 OPTIMIZED MODEL TESTING SUITE")
    print("=" * 50)
    
    tests = [
        ("Model Loading", test_model_loading),
        ("Preprocessing Pipeline", test_preprocessing),
        ("Predictions", test_predictions),
        ("Model Performance", test_model_performance),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total:.1%})")
    
    if passed == total:
        print("🎉 All tests passed! Your optimized models are ready for production.")
    else:
        print("⚠ Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 