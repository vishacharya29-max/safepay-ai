import os
import sys
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from preprocessing import prepare_data, save_preprocessing_artifacts
from evaluate import evaluate_model, print_evaluation_report

def train_all_models(data_path: str = None, models_dir: str = None):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if data_path is None:
        data_path = os.path.join(base_dir, "data", "transactions.csv")
    if models_dir is None:
        models_dir = os.path.join(base_dir, "models")
        
    (X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_columns, _, _) = prepare_data(data_path)
    save_preprocessing_artifacts(scaler, feature_columns, models_dir)
    
    models = {
        "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(class_weight='balanced', max_depth=6, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, class_weight='balanced', max_depth=8, n_jobs=-1, random_state=42)
    }
    
    evaluation_results = []
    best_model_name = None
    best_f1_score = -1.0
    trained_models = {}
    
    for name, clf in models.items():
        print(f"\n[>>] Training {name}...")
        clf.fit(X_train_scaled, y_train)
        trained_models[name] = clf
        metrics = evaluate_model(clf, X_test_scaled, y_test, model_name=name)
        print_evaluation_report(metrics)
        evaluation_results.append(metrics)
        
        if metrics["f1_score"] > best_f1_score:
            best_f1_score = metrics["f1_score"]
            best_model_name = name
            
    print(f"\n[BEST MODEL SELECTED]: {best_model_name} (F1: {best_f1_score:.4f})")
    best_model_path = os.path.join(models_dir, "best_model.joblib")
    joblib.dump(trained_models[best_model_name], best_model_path)
    print(f"[SAVED] Best model saved to: {best_model_path}")
    
    return evaluation_results, trained_models[best_model_name], scaler, feature_columns

if __name__ == "__main__":
    train_all_models()