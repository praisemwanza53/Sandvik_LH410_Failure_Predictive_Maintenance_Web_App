import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import warnings

class OptimizedPredictor:
    def __init__(self):
        self.models = {}
        self.feature_names = {}
        self.scaler = None
        self.load_models()
    
    def load_models(self):
        """Load all optimized models and their associated files"""
        data_dir = Path(__file__).parent.parent.parent / "data"
        
        # Load robust scaler
        scaler_path = data_dir / "robust_scaler.pkl"
        if scaler_path.exists():
            self.scaler = joblib.load(scaler_path)
        
        # Load models for each failure type
        failure_types = ['failure_occurred', 'engine_failure', 'brake_failure', 'transmission_failure']
        
        for failure_type in failure_types:
            model_path = data_dir / f"best_model_{failure_type}.pkl"
            feature_names_path = data_dir / f"feature_names_{failure_type}.pkl"
            
            if model_path.exists() and feature_names_path.exists():
                self.models[failure_type] = joblib.load(model_path)
                self.feature_names[failure_type] = joblib.load(feature_names_path)
                print(f"✓ Loaded model for {failure_type}")
            else:
                print(f"⚠ Model files not found for {failure_type}")
    
    def preprocess_new_data(self, alarm_data: Dict[str, Any]) -> pd.DataFrame:
        """Preprocess new alarm data using the same pipeline as training"""
        # Convert to DataFrame
        df = pd.DataFrame([alarm_data])
        
        # Always ensure a valid timestamp
        timestamp_str = df['timestamp'].iloc[0] if 'timestamp' in df.columns and pd.notnull(df['timestamp'].iloc[0]) else datetime.utcnow().isoformat()
        timestamp = pd.to_datetime(timestamp_str)
        df['hour_of_day'] = timestamp.hour
        df['day_of_week'] = timestamp.weekday()
        df['month'] = timestamp.month
        df['is_weekend'] = 1 if timestamp.weekday() >= 5 else 0
        df['is_night_shift'] = 1 if 22 <= timestamp.hour or timestamp.hour <= 6 else 0
        
        # Create binary features for alarm types
        alarm_type = str(alarm_data.get('alarm_type', '')).lower()
        df['is_temperature_alarm'] = 1 if 'temp' in alarm_type else 0
        df['is_pressure_alarm'] = 1 if 'pressure' in alarm_type else 0
        df['is_filter_alarm'] = 1 if 'filter' in alarm_type else 0
        df['is_sensor_alarm'] = 1 if 'sensor' in alarm_type else 0
        df['is_electrical_alarm'] = 1 if 'electrical' in alarm_type else 0
        df['is_safety_alarm'] = 1 if 'safety' in alarm_type else 0
        df['is_maintenance_alarm'] = 1 if 'maintenance' in alarm_type else 0
        df['is_critical_alarm'] = 1 if 'critical' in alarm_type else 0
        
        # Component encoding (simplified)
        component = str(alarm_data.get('component', '')).lower()
        component_mapping = {
            'engine': 0, 'brake': 1, 'transmission': 2, 'electrical': 3
        }
        df['component_category_encoded'] = component_mapping.get(component, 0)
        
        # Severity encoding
        severity = str(alarm_data.get('severity', '')).lower()
        severity_mapping = {'low': 0, 'medium': 1, 'high': 2, 'critical': 3}
        df['severity_level_encoded'] = severity_mapping.get(severity, 1)
        
        # Location encoding
        location = str(alarm_data.get('location', '')).lower()
        location_mapping = {'front': 0, 'rear': 1, 'left': 2, 'right': 3}
        df['Location_encoded'] = location_mapping.get(location, 0)
        
        # Time since last alarm (simplified - would need historical data)
        df['time_since_last_alarm'] = 60  # Default 1 hour
        
        # Alarm frequency features (simplified - would need historical data)
        df['alarms_last_1h'] = 1
        df['alarms_last_6h'] = alarm_data.get('count', 1)
        df['alarms_last_24h'] = alarm_data.get('count', 1)
        
        # Component-specific alarm counts
        df['engine_alarms_24h'] = 1 if component == 'engine' else 0
        df['brake_alarms_24h'] = 1 if component == 'brake' else 0
        df['transmission_alarms_24h'] = 1 if component == 'transmission' else 0
        df['sensor_alarms_24h'] = 1 if component == 'sensor' else 0
        df['electrical_alarms_24h'] = 1 if component == 'electrical' else 0
        
        # Create interaction features
        df['engine_brake_interaction'] = df['engine_alarms_24h'] * df['brake_alarms_24h']
        df['engine_transmission_interaction'] = df['engine_alarms_24h'] * df['transmission_alarms_24h']
        df['engine_electrical_interaction'] = df['engine_alarms_24h'] * df['electrical_alarms_24h']
        df['brake_transmission_interaction'] = df['brake_alarms_24h'] * df['transmission_alarms_24h']
        df['brake_electrical_interaction'] = df['brake_alarms_24h'] * df['electrical_alarms_24h']
        df['transmission_electrical_interaction'] = df['transmission_alarms_24h'] * df['electrical_alarms_24h']
        
        # Add rolling statistics (simplified)
        for col in ['alarms_last_1h', 'alarms_last_6h', 'alarms_last_24h', 
                   'engine_alarms_24h', 'brake_alarms_24h', 'transmission_alarms_24h', 
                   'sensor_alarms_24h', 'electrical_alarms_24h']:
            df[f'{col}_rolling_mean'] = df[col]
            df[f'{col}_rolling_std'] = 0
        
        # One-hot encode categorical features
        df = pd.get_dummies(df, drop_first=True)
        
        return df
    
    def predict_failure(self, alarm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict failure probabilities for all failure types"""
        warnings.filterwarnings("ignore")
        try:
            # Preprocess the data
            features_df = self.preprocess_new_data(alarm_data)
            
            # Ensure we have the right features for each model
            predictions = {}
            
            for failure_type, model in self.models.items():
                if failure_type in self.feature_names:
                    # Get the expected feature names for this model
                    expected_features = self.feature_names[failure_type]
                    
                    # Create a DataFrame with the expected features
                    model_features = pd.DataFrame(0, index=[0], columns=expected_features)
                    
                    # Fill in the features we have
                    for feature in expected_features:
                        if feature in features_df.columns:
                            model_features[feature] = features_df[feature].iloc[0]
                    
                    # Make prediction
                    if hasattr(model, 'predict_proba'):
                        prob = model.predict_proba(model_features)[0, 1]
                    else:
                        prob = model.predict(model_features)[0]
                    
                    predictions[failure_type] = {
                        'probability': float(prob),
                        'risk_level': self._get_risk_level(prob)
                    }
            
            # Calculate overall risk
            overall_prob = predictions.get('failure_occurred', {}).get('probability', 0)
            
            return {
                'predictions': predictions,
                'overall_risk': {
                    'probability': float(overall_prob),
                    'risk_level': self._get_risk_level(overall_prob),
                    'hours_to_failure': self._estimate_hours_to_failure(overall_prob)
                },
                'component': alarm_data.get('component', 'unknown'),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'error': f'Prediction failed: {str(e)}',
                'predictions': {},
                'overall_risk': {'probability': 0, 'risk_level': 'unknown'},
                'component': alarm_data.get('component', 'unknown'),
                'timestamp': datetime.utcnow().isoformat()
            }

    def _get_risk_level(self, probability: float) -> str:
        """Convert probability to risk level"""
        if probability >= 0.8:
            return 'critical'
        elif probability >= 0.6:
            return 'high'
        elif probability >= 0.4:
            return 'medium'
        elif probability >= 0.2:
            return 'low'
        else:
            return 'very_low'
    
    def _estimate_hours_to_failure(self, probability: float) -> float:
        """Estimate hours to failure based on probability"""
        if probability >= 0.8:
            return max(0, 24 - probability * 24)  # Critical: 0-5 hours
        elif probability >= 0.6:
            return max(0, 72 - probability * 72)  # High: 0-29 hours
        elif probability >= 0.4:
            return max(0, 168 - probability * 168)  # Medium: 0-101 hours
        else:
            return max(0, 720 - probability * 720)  # Low: 0-576 hours

# Initialize the predictor
predictor = OptimizedPredictor()