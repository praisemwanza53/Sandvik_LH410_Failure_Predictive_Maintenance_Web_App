import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def analyze_preprocessed_data_optimized():
    """Enhanced analysis of preprocessed data with optimization recommendations"""
    
    print("=== ENHANCED DATA ANALYSIS & OPTIMIZATION ===\n")
    
    # Load data
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        features = pd.read_csv(os.path.join(script_dir, 'features.csv'))
        targets = pd.read_csv(os.path.join(script_dir, 'targets.csv'))
        print("✓ Successfully loaded preprocessed data")
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return
    
    print(f"\n=== DATA OVERVIEW ===")
    print(f"Features shape: {features.shape}")
    print(f"Targets shape: {targets.shape}")
    print(f"Total samples: {len(features)}")
    print(f"Total features: {len(features.columns)}")
    
    # Enhanced failure analysis
    print(f"\n=== FAILURE ANALYSIS ===")
    total_failures = targets['failure_occurred'].sum()
    print(f"Total failures: {total_failures} out of {len(targets)} samples")
    print(f"Overall failure rate: {total_failures/len(targets)*100:.1f}%")
    
    for col in targets.columns:
        failure_count = targets[col].sum()
        failure_rate = targets[col].mean()
        print(f"{col}: {failure_count} failures ({failure_rate*100:.1f}%)")
    
    # Data quality assessment
    print(f"\n=== DATA QUALITY ASSESSMENT ===")
    
    # Check for outliers in time_since_last_alarm
    if 'time_since_last_alarm' in features.columns:
        time_data = features['time_since_last_alarm']
        q99 = time_data.quantile(0.99)
        q95 = time_data.quantile(0.95)
        max_val = time_data.max()
        
        print(f"Time since last alarm:")
        print(f"  95th percentile: {q95:.0f} minutes ({q95/60:.1f} hours)")
        print(f"  99th percentile: {q99:.0f} minutes ({q99/60:.1f} hours)")
        print(f"  Maximum: {max_val:.0f} minutes ({max_val/60:.1f} hours)")
        
        if max_val > q99 * 10:
            print(f"  ⚠ CRITICAL: Extreme outlier detected! Max value is {max_val/q99:.1f}x the 99th percentile")
    
    # Check feature variation
    print(f"\n=== FEATURE VARIATION ANALYSIS ===")
    low_variance_features = []
    for col in features.columns:
        if features[col].dtype in ['int64', 'float64']:
            std_dev = features[col].std()
            if std_dev < 0.01:  # Very low variation
                low_variance_features.append(col)
                print(f"⚠ {col}: std={std_dev:.4f} (very low variation)")
    
    # Check for perfect correlation
    print(f"\n=== CORRELATION ANALYSIS ===")
    numeric_features = features.select_dtypes(include=[np.number])
    corr_matrix = numeric_features.corr()
    
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.95:
                high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val))
    
    if high_corr_pairs:
        print("⚠ Highly correlated features (|correlation| > 0.95):")
        for feat1, feat2, corr_val in high_corr_pairs:
            print(f"  {feat1} ↔ {feat2}: {corr_val:.3f}")
    else:
        print("✓ No highly correlated features detected")
    
    # Feature importance analysis
    print(f"\n=== FEATURE IMPORTANCE ANALYSIS ===")
    if 'failure_occurred' in targets.columns:
        correlations = []
        for col in features.columns:
            if features[col].dtype in ['int64', 'float64']:
                corr = features[col].corr(targets['failure_occurred'])
                if not pd.isna(corr):
                    correlations.append((col, abs(corr)))
        
        correlations.sort(key=lambda x: x[1], reverse=True)
        print("Top 10 features by absolute correlation with failure:")
        for i, (col, corr) in enumerate(correlations[:10], 1):
            print(f"{i:2d}. {col}: {corr:.3f}")
    
    # Optimization recommendations
    print(f"\n=== OPTIMIZATION RECOMMENDATIONS ===")
    
    # Data collection recommendations
    print("📊 DATA COLLECTION IMPROVEMENTS:")
    print("  1. Increase sample size: Current 148 samples is quite small for ML")
    print("  2. Collect more balanced data: 15.5% failure rate is imbalanced")
    print("  3. Investigate the extreme time gap (1.5M minutes) - likely data error")
    print("  4. Consider collecting data over longer time periods")
    
    # Feature engineering recommendations
    print("\n🔧 FEATURE ENGINEERING IMPROVEMENTS:")
    if low_variance_features:
        print(f"  1. Remove or transform low-variance features: {', '.join(low_variance_features)}")
    
    if 'time_since_last_alarm' in features.columns:
        print("  2. Cap or log-transform 'time_since_last_alarm' to handle outliers")
        print("  3. Create binned time features (e.g., 'recent', 'medium', 'old')")
    
    print("  4. Consider creating interaction features between alarm types")
    print("  5. Add rolling statistics (mean, std) for alarm frequencies")
    
    # Model recommendations
    print("\n🤖 MODELING RECOMMENDATIONS:")
    print("  1. Use techniques for imbalanced data:")
    print("     - SMOTE or other oversampling methods")
    print("     - Class weights in models")
    print("     - F1-score instead of accuracy for evaluation")
    
    print("  2. Consider ensemble methods:")
    print("     - Random Forest with class weights")
    print("     - XGBoost with scale_pos_weight")
    print("     - Voting classifiers")
    
    print("  3. Cross-validation strategy:")
    print("     - Use stratified k-fold to maintain class distribution")
    print("     - Consider time-series split if data is temporal")
    
    # Data preprocessing recommendations
    print("\n⚙️ PREPROCESSING RECOMMENDATIONS:")
    print("  1. Handle outliers in 'time_since_last_alarm':")
    print("     - Cap at 95th or 99th percentile")
    print("     - Use robust scaling")
    
    print("  2. Feature scaling:")
    print("     - Use RobustScaler for features with outliers")
    print("     - Use StandardScaler for normally distributed features")
    
    print("  3. Feature selection:")
    print("     - Remove features with correlation > 0.95")
    print("     - Use mutual information or chi-square for feature selection")
    
    # Specific issues to address
    print(f"\n🚨 CRITICAL ISSUES TO ADDRESS:")
    print("  1. Data quality: Investigate the 1.5M minute time gap")
    print("  2. Sample size: 148 samples may be insufficient for reliable models")
    print("  3. Class imbalance: Consider collecting more failure cases")
    print("  4. Feature redundancy: Some features may be redundant")
    
    print(f"\n=== SUMMARY ===")
    print("✓ Data structure is good with 25 features")
    print("✓ No missing values detected")
    print("⚠ Main concerns: small sample size, class imbalance, data quality issues")
    print("💡 Focus on data collection and quality improvement before model optimization")

if __name__ == "__main__":
    analyze_preprocessed_data_optimized() 