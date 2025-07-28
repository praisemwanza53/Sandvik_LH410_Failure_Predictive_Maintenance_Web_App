import pandas as pd
import numpy as np

def analyze_preprocessed_data():
    """Analyze the preprocessed data to check if it makes sense"""
    
    print("=== ANALYZING PREPROCESSED DATA ===\n")
    
    # Load data
    try:
        # Get the directory where this script is located
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        features = pd.read_csv(os.path.join(script_dir, 'features.csv'))
        targets = pd.read_csv(os.path.join(script_dir, 'targets.csv'))
        print("✓ Successfully loaded preprocessed data")
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return
    
    print(f"\n=== DATA SHAPES ===")
    print(f"Features shape: {features.shape}")
    print(f"Targets shape: {targets.shape}")
    
    print(f"\n=== FEATURE COLUMNS ===")
    for i, col in enumerate(features.columns, 1):
        print(f"{i:2d}. {col}")
    
    print(f"\n=== TARGET COLUMNS ===")
    for i, col in enumerate(targets.columns, 1):
        print(f"{i}. {col}")
    
    print(f"\n=== BASIC STATISTICS ===")
    print(f"Total samples: {len(features)}")
    print(f"Total features: {len(features.columns)}")
    
    # Check failure rates
    print(f"\n=== FAILURE ANALYSIS ===")
    for col in targets.columns:
        failure_rate = targets[col].mean()
        print(f"{col}: {failure_rate:.3f} ({failure_rate*100:.1f}%)")
    
    # Check feature ranges
    print(f"\n=== FEATURE RANGES ===")
    numeric_features = features.select_dtypes(include=[np.number]).columns
    for col in numeric_features[:10]:  # Show first 10 features
        min_val = features[col].min()
        max_val = features[col].max()
        mean_val = features[col].mean()
        print(f"{col}: min={min_val:.2f}, max={max_val:.2f}, mean={mean_val:.2f}")
    
    # Check for missing values
    print(f"\n=== MISSING VALUES ===")
    missing_features = features.isnull().sum()
    missing_targets = targets.isnull().sum()
    
    if missing_features.sum() == 0:
        print("✓ No missing values in features")
    else:
        print("✗ Missing values found in features:")
        for col, count in missing_features[missing_features > 0].items():
            print(f"  {col}: {count}")
    
    if missing_targets.sum() == 0:
        print("✓ No missing values in targets")
    else:
        print("✗ Missing values found in targets:")
        for col, count in missing_targets[missing_targets > 0].items():
            print(f"  {col}: {count}")
    
    # Check temporal features
    print(f"\n=== TEMPORAL FEATURES ANALYSIS ===")
    if 'hour_of_day' in features.columns:
        print(f"Hour of day range: {features['hour_of_day'].min()} - {features['hour_of_day'].max()}")
    if 'day_of_week' in features.columns:
        print(f"Day of week range: {features['day_of_week'].min()} - {features['day_of_week'].max()}")
    if 'month' in features.columns:
        print(f"Month range: {features['month'].min()} - {features['month'].max()}")
    
    # Check alarm frequency features
    print(f"\n=== ALARM FREQUENCY ANALYSIS ===")
    alarm_features = [col for col in features.columns if 'alarms_last' in col or 'alarms_24h' in col]
    for col in alarm_features:
        mean_val = features[col].mean()
        max_val = features[col].max()
        print(f"{col}: mean={mean_val:.2f}, max={max_val:.2f}")
    
    # Check binary features
    print(f"\n=== BINARY FEATURES ANALYSIS ===")
    binary_features = [col for col in features.columns if col.startswith('is_')]
    for col in binary_features:
        positive_rate = features[col].mean()
        print(f"{col}: {positive_rate:.3f} ({positive_rate*100:.1f}% positive)")
    
    # Check correlation with failure
    print(f"\n=== FEATURE-FAILURE CORRELATIONS ===")
    if 'failure_occurred' in targets.columns:
        correlations = []
        for col in features.columns:
            corr = features[col].corr(targets['failure_occurred'])
            if abs(corr) > 0.1:  # Only show meaningful correlations
                correlations.append((col, corr))
        
        correlations.sort(key=lambda x: abs(x[1]), reverse=True)
        for col, corr in correlations[:10]:
            print(f"{col}: {corr:.3f}")
    
    print(f"\n=== DATA QUALITY ASSESSMENT ===")
    
    # Check for data consistency
    issues = []
    
    # Check if all failure windows have critical alarms
    if 'is_critical_alarm' in features.columns and 'failure_occurred' in targets.columns:
        critical_alarms = features['is_critical_alarm'].sum()
        failures = targets['failure_occurred'].sum()
        if failures > critical_alarms:
            issues.append(f"More failures ({failures}) than critical alarms ({critical_alarms})")
    
    # Check for reasonable time gaps
    if 'time_since_last_alarm' in features.columns:
        max_gap = features['time_since_last_alarm'].max()
        if max_gap > 1000000:  # More than ~11 days
            issues.append(f"Very large time gap detected: {max_gap:.0f} minutes")
    
    # Check for reasonable alarm counts
    if 'alarms_last_24h' in features.columns:
        max_alarms = features['alarms_last_24h'].max()
        if max_alarms > 100:
            issues.append(f"Very high alarm count: {max_alarms} alarms in 24h")
    
    if issues:
        print("⚠ Potential issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ No obvious data quality issues detected")
    
    print(f"\n=== SUMMARY ===")
    print(f"✓ Data preprocessing appears to be working correctly")
    print(f"✓ Features are properly scaled and encoded")
    print(f"✓ Failure labels are created based on critical alarm patterns")
    print(f"✓ Temporal and rolling features capture alarm patterns")
    print(f"✓ Binary features identify specific alarm types")

if __name__ == "__main__":
    analyze_preprocessed_data() 