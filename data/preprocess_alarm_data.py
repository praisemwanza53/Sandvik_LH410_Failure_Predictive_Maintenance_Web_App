import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import warnings
warnings.filterwarnings('ignore')

class AlarmDataPreprocessor:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
    def load_data(self):
        """Load and clean the CSV data"""
        print("Loading alarm logs data...")
        
        # Read CSV with proper handling of commas in Description field
        try:
            # Try with python engine which is more flexible
            self.df = pd.read_csv(self.csv_path, engine='python')
        except:
            try:
                # If that fails, try with QUOTE_NONE
                self.df = pd.read_csv(self.csv_path, quoting=3)
            except:
                # If that fails, try with custom parsing
                self.df = pd.read_csv(self.csv_path, engine='python', on_bad_lines='skip')
        
        # Clean column names
        self.df.columns = [col.strip() for col in self.df.columns]
        
        # Convert Date and Time to datetime
        self.df['datetime'] = pd.to_datetime(self.df['Date'] + ' ' + self.df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S', errors='coerce')
        
        # Drop rows with invalid datetime
        self.df = self.df.dropna(subset=['datetime'])
        
        # Sort by datetime
        self.df = self.df.sort_values('datetime').reset_index(drop=True)
        
        print(f"Loaded {len(self.df)} alarm records")
        return self.df
    
    def extract_component_categories(self, description):
        """Extract component category from alarm description"""
        description = str(description).lower()
        
        if any(word in description for word in ['engine', 'fuel', 'coolant', 'air filter', 'spn']):
            return 'engine'
        elif any(word in description for word in ['brake', 'pedal']):
            return 'brake'
        elif any(word in description for word in ['transmission', 'solenoid']):
            return 'transmission'
        elif any(word in description for word in ['speed sensor', 'sensor']):
            return 'sensor'
        elif any(word in description for word in ['lubrication', 'lube']):
            return 'lubrication'
        elif any(word in description for word in ['fire', 'e-stop', 'emergency']):
            return 'safety'
        elif any(word in description for word in ['warning', 'lamp', 'fuse', 'circuit']):
            return 'electrical'
        elif any(word in description for word in ['display', 'service', 'calibrat']):
            return 'control'
        else:
            return 'other'
    
    def extract_severity_level(self, description):
        """Extract severity level from alarm description"""
        description = str(description).lower()
        
        if any(word in description for word in ['fire', 'e-stop', 'emergency', 'critical']):
            return 'critical'
        elif any(word in description for word in ['warning', 'high', 'low', 'pressure', 'temperature']):
            return 'warning'
        elif any(word in description for word in ['service', 'calibrat', 'info']):
            return 'info'
        elif any(word in description for word in ['filter', 'lubrication', 'maintenance']):
            return 'maintenance'
        else:
            return 'info'
    
    def extract_alarm_type_features(self, description):
        """Extract specific alarm type features"""
        description = str(description).lower()
        
        return {
            'is_temperature_alarm': any(word in description for word in ['temperature', 'coolant', 'hot']),
            'is_pressure_alarm': any(word in description for word in ['pressure', 'spn']),
            'is_filter_alarm': any(word in description for word in ['filter', 'blocked']),
            'is_sensor_alarm': any(word in description for word in ['sensor', 'signal']),
            'is_electrical_alarm': any(word in description for word in ['circuit', 'voltage', 'fuse', 'lamp']),
            'is_safety_alarm': any(word in description for word in ['fire', 'e-stop', 'emergency']),
            'is_maintenance_alarm': any(word in description for word in ['lubrication', 'service', 'maintenance'])
        }
    
    def create_temporal_features(self):
        """Create temporal features from datetime"""
        self.df['hour_of_day'] = self.df['datetime'].dt.hour
        self.df['day_of_week'] = self.df['datetime'].dt.dayofweek
        self.df['month'] = self.df['datetime'].dt.month
        self.df['day_of_month'] = self.df['datetime'].dt.day
        self.df['is_weekend'] = self.df['day_of_week'].isin([5, 6]).astype(int)
        self.df['is_night_shift'] = ((self.df['hour_of_day'] >= 22) | (self.df['hour_of_day'] <= 6)).astype(int)
        
        # Time since last alarm (in minutes)
        self.df['time_since_last_alarm'] = self.df['datetime'].diff().dt.total_seconds() / 60
        self.df['time_since_last_alarm'] = self.df['time_since_last_alarm'].fillna(0)
    
    def create_rolling_features(self):
        """Create rolling window features"""
        # For time-based rolling, we need to use a different approach
        # Since we have limited data, let's use simple rolling windows
        
        # Alarms in last N records (approximating time windows)
        for window in [1, 6, 24]:
            self.df[f'alarms_last_{window}h'] = self.df['datetime'].rolling(
                window=window, min_periods=1
            ).count()
        
        # Component-specific rolling features
        for component in ['engine', 'brake', 'transmission', 'sensor', 'electrical']:
            mask = self.df['component_category'] == component
            if mask.sum() > 0:  # Only if component exists in data
                # Count component alarms in last 24 records
                self.df[f'{component}_alarms_24h'] = self.df[mask]['datetime'].rolling(
                    window=24, min_periods=1
                ).count().fillna(0)
            else:
                self.df[f'{component}_alarms_24h'] = 0
    
    def create_failure_labels(self):
        """Create failure labels based on critical alarms and patterns"""
        # Define failure indicators
        critical_alarms = [
            'fire detected', 'e-stop activated', 'emergency stop',
            'engine failure', 'transmission failure', 'brake failure'
        ]
        
        # Mark critical alarms as potential failure indicators
        self.df['is_critical_alarm'] = self.df['Description'].str.lower().str.contains(
            '|'.join(critical_alarms), na=False
        ).astype(int)
        
        # Create failure window (24 hours after critical alarm)
        self.df['failure_window'] = 0
        
        for idx, row in self.df[self.df['is_critical_alarm'] == 1].iterrows():
            failure_start = row['datetime']
            failure_end = failure_start + timedelta(hours=24)
            
            # Mark all alarms in the failure window
            mask = (self.df['datetime'] >= failure_start) & (self.df['datetime'] <= failure_end)
            self.df.loc[mask, 'failure_window'] = 1
        
        # Create binary failure target
        self.df['failure_occurred'] = self.df['failure_window'].astype(int)
        
        # Create component-specific failure targets
        for component in ['engine', 'brake', 'transmission', 'electrical']:
            component_mask = self.df['component_category'] == component
            self.df[f'{component}_failure'] = (
                (self.df['failure_window'] == 1) & component_mask
            ).astype(int)
    
    def engineer_features(self):
        """Main feature engineering pipeline"""
        print("Engineering features...")
        
        try:
            # Extract component categories
            print("  - Extracting component categories...")
            self.df['component_category'] = self.df['Description'].apply(self.extract_component_categories)
            
            # Extract severity levels
            print("  - Extracting severity levels...")
            self.df['severity_level'] = self.df['Description'].apply(self.extract_severity_level)
            
            # Extract alarm type features
            print("  - Extracting alarm type features...")
            alarm_features = self.df['Description'].apply(self.extract_alarm_type_features)
            # Convert the series of dictionaries to separate columns
            for feature in ['is_temperature_alarm', 'is_pressure_alarm', 'is_filter_alarm',
                           'is_sensor_alarm', 'is_electrical_alarm', 'is_safety_alarm',
                           'is_maintenance_alarm']:
                self.df[feature] = alarm_features.apply(lambda x: x[feature]).astype(int)
            
            # Create temporal features
            print("  - Creating temporal features...")
            self.create_temporal_features()
            
            # Create rolling features
            print("  - Creating rolling features...")
            self.create_rolling_features()
            
            # Create failure labels
            print("  - Creating failure labels...")
            self.create_failure_labels()
            
            # Fill missing values
            print("  - Filling missing values...")
            self.df['Count'] = self.df['Count'].fillna(1)
            self.df['Code'] = self.df['Code'].fillna(0)
            self.df['Location'] = self.df['Location'].fillna('unknown')
            
            print("Feature engineering completed!")
            
        except Exception as e:
            print(f"Error during feature engineering: {str(e)}")
            print(f"DataFrame shape: {self.df.shape}")
            print(f"DataFrame columns: {list(self.df.columns)}")
            raise
    
    def encode_categorical_features(self):
        """Encode categorical features"""
        print("Encoding categorical features...")
        
        categorical_features = [
            'component_category', 'severity_level', 'Location'
        ]
        
        for feature in categorical_features:
            if feature in self.df.columns:
                le = LabelEncoder()
                self.df[f'{feature}_encoded'] = le.fit_transform(self.df[feature].astype(str))
                self.label_encoders[feature] = le
    
    def select_features(self):
        """Select final features for model training"""
        feature_columns = [
            # Basic alarm features
            'alarm_code', 'count', 'hour_of_day', 'day_of_week', 'month',
            'is_weekend', 'is_night_shift', 'time_since_last_alarm',
            
            # Rolling features
            'alarms_last_1h', 'alarms_last_6h', 'alarms_last_24h',
            'engine_alarms_24h', 'brake_alarms_24h', 'transmission_alarms_24h',
            'sensor_alarms_24h', 'electrical_alarms_24h',
            
            # Alarm type features
            'is_temperature_alarm', 'is_pressure_alarm', 'is_filter_alarm',
            'is_sensor_alarm', 'is_electrical_alarm', 'is_safety_alarm',
            'is_maintenance_alarm', 'is_critical_alarm',
            
            # Encoded categorical features
            'component_category_encoded', 'severity_level_encoded', 'Location_encoded'
        ]
        
        # Filter to only existing columns
        available_features = [col for col in feature_columns if col in self.df.columns]
        
        return self.df[available_features]
    
    def prepare_training_data(self):
        """Prepare final training dataset"""
        print("Preparing training data...")
        
        # Select features
        X = self.select_features()
        
        # Select targets
        targets = ['failure_occurred', 'engine_failure', 'brake_failure', 
                  'transmission_failure', 'electrical_failure']
        available_targets = [target for target in targets if target in self.df.columns]
        
        y = self.df[available_targets]
        
        # Debug: Check for missing values
        print(f"Original X shape: {X.shape}")
        print(f"Missing values in X: {X.isnull().sum().sum()}")
        print(f"Missing values in y: {y.isnull().sum().sum()}")
        
        # Check which columns have missing values
        missing_cols = X.columns[X.isnull().any()].tolist()
        if missing_cols:
            print(f"Columns with missing values: {missing_cols}")
            for col in missing_cols:
                print(f"  {col}: {X[col].isnull().sum()} missing values")
        
        # Fill missing values instead of removing rows
        X = X.fillna(0)  # Fill numeric features with 0
        y = y.fillna(0)  # Fill target variables with 0
        
        print(f"Final dataset shape: {X.shape}")
        print(f"Target variables: {list(y.columns)}")
        
        return X, y
    
    def save_preprocessed_data(self, X, y, output_dir='./'):
        """Save preprocessed data and encoders"""
        print("Saving preprocessed data...")
        
        # Save features and targets
        X.to_csv(f'{output_dir}features.csv', index=False)
        y.to_csv(f'{output_dir}targets.csv', index=False)
        
        # Save encoders
        joblib.dump(self.label_encoders, f'{output_dir}label_encoders.pkl')
        
        # Save feature names
        feature_names = list(X.columns)
        joblib.dump(feature_names, f'{output_dir}feature_names.pkl')
        
        print(f"Data saved to {output_dir}")
    
    def run_preprocessing(self):
        """Run complete preprocessing pipeline"""
        self.load_data()
        self.engineer_features()
        self.encode_categorical_features()
        X, y = self.prepare_training_data()
        self.save_preprocessed_data(X, y)
        
        return X, y

def main():
    """Main execution function"""
    # Initialize preprocessor
    preprocessor = AlarmDataPreprocessor('alarm_logs.csv')
    
    # Run preprocessing
    X, y = preprocessor.run_preprocessing()
    
    # Print summary statistics
    print("\n=== PREPROCESSING SUMMARY ===")
    print(f"Total features: {X.shape[1]}")
    print(f"Total samples: {X.shape[0]}")
    print(f"Failure rate: {y['failure_occurred'].mean():.2%}")
    
    print("\n=== FEATURE IMPORTANCE PREVIEW ===")
    feature_importance = {}
    for feature in X.columns:
        if y['failure_occurred'].corr(X[feature]) > 0.1:
            feature_importance[feature] = abs(y['failure_occurred'].corr(X[feature]))
    
    # Sort by importance
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    for feature, importance in sorted_features[:10]:
        print(f"{feature}: {importance:.3f}")
    
    print("\nPreprocessing completed successfully!")
    print("Files created:")
    print("- features.csv: Feature matrix")
    print("- targets.csv: Target variables")
    print("- label_encoders.pkl: Categorical encoders")
    print("- feature_names.pkl: Feature names")

if __name__ == "__main__":
    main() 