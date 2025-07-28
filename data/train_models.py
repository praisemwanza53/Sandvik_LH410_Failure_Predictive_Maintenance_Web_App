import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class FailurePredictorTrainer:
    def __init__(self, features_path='data/features_optimized.csv', targets_path='data/targets.csv', feature_names_path='data/feature_names_optimized.pkl'):
        self.features_path = features_path
        self.targets_path = targets_path
        self.feature_names_path = feature_names_path
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.best_model = None
        self.feature_names = None
        # No scaler needed, features are already scaled
        # self.scaler = StandardScaler()
        
    def load_data(self):
        """Load optimized features and targets"""
        print("Loading optimized preprocessed data...")
        self.X = pd.read_csv(self.features_path)
        self.y = pd.read_csv(self.targets_path)
        try:
            self.feature_names = joblib.load(self.feature_names_path)
        except Exception:
            self.feature_names = list(self.X.columns)
        print(f"Features shape: {self.X.shape}")
        print(f"Targets shape: {self.y.shape}")
        print(f"Missing values in features: {self.X.isnull().sum().sum()}")
        print(f"Missing values in targets: {self.y.isnull().sum().sum()}")
        return self.X, self.y
    
    def prepare_data(self, target_column='failure_occurred'):
        """Prepare data for training"""
        print(f"Preparing data for target: {target_column}")
        # Select target
        if target_column in self.y.columns:
            y_target = self.y[target_column]
        else:
            print(f"Target column {target_column} not found. Available: {list(self.y.columns)}")
            return None, None, None, None
        # Remove rows with missing values
        valid_mask = ~(self.X.isnull().any(axis=1) | y_target.isnull())
        X_clean = self.X[valid_mask]
        y_clean = y_target[valid_mask]
        print(f"Clean data shape: {X_clean.shape}")
        print(f"Target distribution: {y_clean.value_counts().to_dict()}")
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_clean, y_clean, test_size=0.2, random_state=42, stratify=y_clean
        )
        # No scaling needed, already scaled in preprocessing
        self.X_train_scaled = self.X_train.values
        self.X_test_scaled = self.X_test.values
        return self.X_train_scaled, self.X_test_scaled, self.y_train, self.y_test
    
    def train_random_forest(self):
        print("Training Random Forest...")
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        rf = RandomForestClassifier(random_state=42, class_weight='balanced')
        grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='f1', n_jobs=-1)
        grid_search.fit(self.X_train_scaled, self.y_train)
        self.models['random_forest'] = grid_search.best_estimator_
        print(f"Best RF params: {grid_search.best_params_}")
        return grid_search.best_estimator_
    
    def train_xgboost(self):
        print("Training XGBoost...")
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [3, 6, 9],
            'learning_rate': [0.01, 0.1, 0.2],
            'subsample': [0.8, 0.9, 1.0]
        }
        xgb_model = xgb.XGBClassifier(random_state=42, scale_pos_weight=1)
        grid_search = GridSearchCV(xgb_model, param_grid, cv=5, scoring='f1', n_jobs=-1)
        grid_search.fit(self.X_train_scaled, self.y_train)
        self.models['xgboost'] = grid_search.best_estimator_
        print(f"Best XGBoost params: {grid_search.best_params_}")
        return grid_search.best_estimator_
    
    def train_svm(self):
        print("Training SVM...")
        param_grid = {
            'C': [0.1, 1, 10],
            'gamma': ['scale', 'auto', 0.001, 0.01],
            'kernel': ['rbf', 'linear']
        }
        svm = SVC(random_state=42, class_weight='balanced', probability=True)
        grid_search = GridSearchCV(svm, param_grid, cv=5, scoring='f1', n_jobs=-1)
        grid_search.fit(self.X_train_scaled, self.y_train)
        self.models['svm'] = grid_search.best_estimator_
        print(f"Best SVM params: {grid_search.best_params_}")
        return grid_search.best_estimator_
    
    def evaluate_model(self, model, model_name):
        print(f"\n=== {model_name.upper()} EVALUATION ===")
        y_pred = model.predict(self.X_test_scaled)
        y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
        print("Classification Report:")
        print(classification_report(self.y_test, y_pred))
        roc_auc = roc_auc_score(self.y_test, y_pred_proba)
        print(f"ROC AUC: {roc_auc:.3f}")
        cm = confusion_matrix(self.y_test, y_pred)
        print("Confusion Matrix:")
        print(cm)
        return {
            'model': model,
            'predictions': y_pred,
            'probabilities': y_pred_proba,
            'roc_auc': roc_auc,
            'confusion_matrix': cm
        }
    
    def compare_models(self):
        print("\n=== MODEL COMPARISON ===")
        results = {}
        for name, model in self.models.items():
            results[name] = self.evaluate_model(model, name)
        print("\nROC AUC Comparison:")
        for name, result in results.items():
            print(f"{name}: {result['roc_auc']:.3f}")
        best_model_name = max(results.keys(), key=lambda x: results[x]['roc_auc'])
        self.best_model = results[best_model_name]['model']
        print(f"\nBest model: {best_model_name} (ROC AUC: {results[best_model_name]['roc_auc']:.3f})")
        return results
    
    def get_feature_importance(self, model, feature_names):
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importance = np.abs(model.coef_[0])
        else:
            return None
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        return feature_importance
    
    def plot_feature_importance(self, model, feature_names, model_name):
        importance_df = self.get_feature_importance(model, feature_names)
        if importance_df is not None:
            plt.figure(figsize=(10, 8))
            top_features = importance_df.head(15)
            sns.barplot(data=top_features, x='importance', y='feature')
            plt.title(f'{model_name} - Top 15 Feature Importance')
            plt.tight_layout()
            plt.savefig(f'data/{model_name}_feature_importance.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"\nTop 10 features for {model_name}:")
            print(importance_df.head(10))
    
    def save_models(self, output_dir='./', target_column='failure_occurred'):
        print("Saving models...")
        # Save best model
        joblib.dump(self.best_model, f'{output_dir}best_model_{target_column}.pkl')
        # Save all models
        joblib.dump(self.models, f'{output_dir}all_models_{target_column}.pkl')
        # Save feature names
        joblib.dump(self.feature_names, f'{output_dir}feature_names_{target_column}.pkl')
        print(f"Models saved to {output_dir}")
    
    def train_all_models(self, target_column='failure_occurred'):
        self.load_data()
        self.prepare_data(target_column)
        self.train_random_forest()
        self.train_xgboost()
        self.train_svm()
        results = self.compare_models()
        feature_names = self.feature_names if self.feature_names is not None else list(self.X.columns)
        self.plot_feature_importance(self.best_model, feature_names, 'Best_Model')
        self.save_models(output_dir='data/', target_column=target_column)
        return results

def main():
    print("=== SANDVIK LH410 FAILURE PREDICTOR MODEL TRAINING ===")
    trainer = FailurePredictorTrainer()
    targets = ['failure_occurred', 'engine_failure', 'brake_failure', 'transmission_failure']
    for target in targets:
        print(f"\n{'='*50}")
        print(f"TRAINING FOR TARGET: {target}")
        print(f"{'='*50}")
        try:
            results = trainer.train_all_models(target)
            print(f"\nTraining completed for {target}")
            print("Files created:")
            print(f"- data/best_model_{target}.pkl: Best model for {target}")
            print(f"- data/all_models_{target}.pkl: All models for {target}")
            print(f"- data/feature_names_{target}.pkl: Feature names for {target}")
        except Exception as e:
            print(f"Error training for {target}: {str(e)}")
            continue
    print("\n=== TRAINING COMPLETED ===")
    print("Next steps:")
    print("1. Copy the best model to backend/core/predictor.pkl")
    print("2. Update the backend model loading code if needed")
    print("3. Test the API endpoints with the trained model")

if __name__ == "__main__":
    main() 