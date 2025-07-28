import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
import joblib
import os

def optimize_preprocessing():
    """Optimize the preprocessing pipeline based on analysis findings"""
    
    print("=== OPTIMIZED PREPROCESSING PIPELINE ===\n")
    
    # Load original data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    features = pd.read_csv(os.path.join(script_dir, 'features.csv'))
    targets = pd.read_csv(os.path.join(script_dir, 'targets.csv'))
    
    print(f"Original features shape: {features.shape}")
    
    # 1. Handle outliers in time_since_last_alarm
    if 'time_since_last_alarm' in features.columns:
        print("\n1. Handling outliers in time_since_last_alarm...")
        time_data = features['time_since_last_alarm']
        
        # Calculate percentiles
        q95 = time_data.quantile(0.95)
        q99 = time_data.quantile(0.99)
        
        print(f"   Original max: {time_data.max():.0f} minutes")
        print(f"   95th percentile: {q95:.0f} minutes")
        print(f"   99th percentile: {q99:.0f} minutes")
        
        # Cap outliers at 99th percentile
        features['time_since_last_alarm_capped'] = np.minimum(time_data, q99)
        
        # Create binned time features
        features['time_since_last_alarm_binned'] = pd.cut(
            features['time_since_last_alarm_capped'],
            bins=[0, q95/2, q95, q99],
            labels=['recent', 'medium', 'old'],
            include_lowest=True
        )
        
        # Encode the binned feature
        features['time_since_last_alarm_binned_encoded'] = features['time_since_last_alarm_binned'].cat.codes
        
        # Remove original problematic column
        features = features.drop('time_since_last_alarm', axis=1)
        print(f"   ✓ Created capped and binned versions, removed original")
    
    # 2. Remove low-variance features
    print("\n2. Removing low-variance features...")
    low_variance_features = []
    for col in features.columns:
        if features[col].dtype in ['int64', 'float64']:
            std_dev = features[col].std()
            if std_dev < 0.01:
                low_variance_features.append(col)
    
    if low_variance_features:
        print(f"   Removing features with std < 0.01: {low_variance_features}")
        features = features.drop(low_variance_features, axis=1)
    else:
        print("   ✓ No low-variance features found")
    
    # 3. Handle highly correlated features
    print("\n3. Handling highly correlated features...")
    numeric_features = features.select_dtypes(include=[np.number])
    corr_matrix = numeric_features.corr()
    
    # Find highly correlated features
    high_corr_features = set()
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > 0.95:
                # Keep the feature with higher correlation to target
                feat1, feat2 = corr_matrix.columns[i], corr_matrix.columns[j]
                if 'failure_occurred' in targets.columns:
                    corr1 = abs(features[feat1].corr(targets['failure_occurred']))
                    corr2 = abs(features[feat2].corr(targets['failure_occurred']))
                    if corr1 < corr2:
                        high_corr_features.add(feat1)
                    else:
                        high_corr_features.add(feat2)
                else:
                    # If no target, remove the second feature
                    high_corr_features.add(feat2)
    
    if high_corr_features:
        print(f"   Removing highly correlated features: {list(high_corr_features)}")
        features = features.drop(high_corr_features, axis=1)
    else:
        print("   ✓ No highly correlated features found")
    
    # 4. Create interaction features
    print("\n4. Creating interaction features...")
    
    # Interaction between alarm types
    alarm_features = [col for col in features.columns if 'alarms_24h' in col]
    if len(alarm_features) >= 2:
        for i, feat1 in enumerate(alarm_features):
            for feat2 in alarm_features[i+1:]:
                interaction_name = f"{feat1.split('_')[0]}_{feat2.split('_')[0]}_interaction"
                features[interaction_name] = features[feat1] * features[feat2]
        print(f"   ✓ Created {len(alarm_features) * (len(alarm_features) - 1) // 2} alarm interaction features")
    
    # 5. Add rolling statistics for alarm frequencies
    print("\n5. Adding rolling statistics...")
    alarm_freq_features = [col for col in features.columns if 'alarms_last' in col or 'alarms_24h' in col]
    
    for col in alarm_freq_features:
        features[f'{col}_rolling_mean'] = features[col].rolling(window=3, min_periods=1).mean()
        features[f'{col}_rolling_std'] = features[col].rolling(window=3, min_periods=1).std()
    
    print(f"   ✓ Added rolling mean and std for {len(alarm_freq_features)} alarm features")
    
    # One-hot encode all categorical/object columns before scaling
    features = pd.get_dummies(features, drop_first=True)

    # 6. Feature scaling
    print("\n6. Applying feature scaling...")
    
    # Separate numeric and categorical features
    numeric_features = features.select_dtypes(include=[np.number])
    categorical_features = features.select_dtypes(include=['object', 'category'])
    
    # Apply robust scaling to handle outliers
    scaler = RobustScaler()
    features_scaled = scaler.fit_transform(numeric_features)
    features_scaled_df = pd.DataFrame(features_scaled, columns=numeric_features.columns, index=features.index)
    
    # Combine scaled numeric features with categorical features
    if not categorical_features.empty:
        final_features = pd.concat([features_scaled_df, categorical_features], axis=1)
    else:
        final_features = features_scaled_df
    
    print(f"   ✓ Applied RobustScaler to {len(numeric_features.columns)} numeric features")

    # Fill NaN values in categorical columns with 'unknown'
    for col in final_features.select_dtypes(include=['category', 'object']).columns:
        if not hasattr(final_features[col], 'cat') or 'unknown' not in final_features[col].cat.categories:
            final_features[col] = final_features[col].astype('category')
            final_features[col] = final_features[col].cat.add_categories(['unknown'])
        final_features[col] = final_features[col].fillna('unknown')

    # Fill NaN values in numeric columns with 0
    for col in final_features.select_dtypes(include=[np.number]).columns:
        final_features[col] = final_features[col].fillna(0)
    
    # 7. Feature selection
    print("\n7. Performing feature selection...")
    if 'failure_occurred' in targets.columns:
        # Use mutual information for feature selection
        selector = SelectKBest(score_func=mutual_info_classif, k=min(20, len(final_features.columns)))
        
        # Prepare data for selection (only numeric features)
        numeric_final = final_features.select_dtypes(include=[np.number])
        if len(numeric_final.columns) > 0:
            selector.fit(numeric_final, targets['failure_occurred'])
            
            # Get selected feature names
            selected_features = numeric_final.columns[selector.get_support()].tolist()
            
            # Keep categorical features as well
            categorical_cols = final_features.select_dtypes(include=['object', 'category']).columns.tolist()
            selected_features.extend(categorical_cols)
            
            final_features = final_features[selected_features]
            print(f"   ✓ Selected {len(selected_features)} features using mutual information")
        else:
            print("   ⚠ No numeric features available for selection")
    else:
        print("   ⚠ No target variable available for feature selection")
    
    # 8. Save optimized data
    print("\n8. Saving optimized data...")
    
    # Save optimized features
    final_features.to_csv(os.path.join(script_dir, 'features_optimized.csv'), index=False)
    
    # Save scaler for later use
    joblib.dump(scaler, os.path.join(script_dir, 'robust_scaler.pkl'))
    
    # Save feature names for later use
    feature_names = final_features.columns.tolist()
    joblib.dump(feature_names, os.path.join(script_dir, 'feature_names_optimized.pkl'))
    
    print(f"   ✓ Saved optimized features: {final_features.shape}")
    print(f"   ✓ Saved scaler and feature names")
    
    # 9. Summary
    print(f"\n=== OPTIMIZATION SUMMARY ===")
    print(f"Original features: {len(features.columns)}")
    print(f"Optimized features: {len(final_features.columns)}")
    print(f"Features removed: {len(features.columns) - len(final_features.columns)}")
    
    print(f"\nOptimization steps applied:")
    print("✓ Outlier handling in time features")
    print("✓ Low-variance feature removal")
    print("✓ High-correlation feature removal")
    print("✓ Interaction feature creation")
    print("✓ Rolling statistics addition")
    print("✓ Robust scaling")
    print("✓ Feature selection using mutual information")
    
    print(f"\nFiles created:")
    print("- features_optimized.csv: Optimized feature dataset")
    print("- robust_scaler.pkl: Fitted scaler for new data")
    print("- feature_names_optimized.pkl: Selected feature names")
    
    return final_features, targets

if __name__ == "__main__":
    optimize_preprocessing() 