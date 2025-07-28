# Data Processing and Model Training

This directory contains scripts to preprocess your alarm logs data and train machine learning models for failure prediction.

## 📁 Files

- `alarm_logs.csv` - Your raw alarm logs data
- `preprocess_alarm_data.py` - Data preprocessing script
- `train_models.py` - Model training script
- `requirements.txt` - Python dependencies

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Preprocess Data
```bash
python preprocess_alarm_data.py
```

This will:
- Load and clean your CSV data
- Extract 25+ engineered features
- Create failure labels
- Save preprocessed data to `features.csv` and `targets.csv`

### 3. Train Models
```bash
python train_models.py
```

This will:
- Train Random Forest, XGBoost, and SVM models
- Compare model performance
- Save the best model as `best_model.pkl`
- Generate feature importance plots

## 📊 Extracted Features

### Temporal Features
- Hour of day, day of week, month
- Weekend/night shift indicators
- Time since last alarm

### Alarm-Specific Features
- Alarm code, count, location
- Component category (engine, brake, transmission, etc.)
- Severity level (critical, warning, info, maintenance)

### Rolling Window Features
- Alarms in last 1h, 6h, 24h
- Component-specific alarm counts

### Alarm Type Features
- Temperature, pressure, filter alarms
- Electrical, safety, maintenance alarms
- Critical alarm indicators

## 🎯 Target Variables

- `failure_occurred` - Binary failure prediction
- `engine_failure` - Engine-specific failures
- `brake_failure` - Brake system failures
- `transmission_failure` - Transmission failures
- `electrical_failure` - Electrical system failures

## 📈 Model Performance

The training script will:
- Use 5-fold cross-validation
- Optimize hyperparameters via grid search
- Compare ROC AUC scores
- Generate confusion matrices
- Plot feature importance

## 🔧 Integration with Backend

After training:

1. Copy the best model:
   ```bash
   cp data/best_model.pkl backend/core/predictor.pkl
   ```

2. Update backend model loading if needed

3. Test API endpoints with real predictions

## 📋 Output Files

After preprocessing:
- `features.csv` - Feature matrix
- `targets.csv` - Target variables
- `label_encoders.pkl` - Categorical encoders
- `feature_names.pkl` - Feature names

After training:
- `best_model.pkl` - Best performing model
- `all_models.pkl` - All trained models
- `scaler.pkl` - Feature scaler
- `*_feature_importance.png` - Feature importance plots

## 🔍 Data Analysis

The preprocessing script provides:
- Data quality statistics
- Feature correlation analysis
- Failure rate analysis
- Component distribution analysis

## 🛠️ Customization

You can modify:
- Feature extraction logic in `preprocess_alarm_data.py`
- Model parameters in `train_models.py`
- Target variable definitions
- Feature selection criteria

## 📝 Notes

- The model uses failure windows (24 hours after critical alarms)
- Features are automatically scaled for training
- Class imbalance is handled with balanced class weights
- All categorical features are properly encoded 