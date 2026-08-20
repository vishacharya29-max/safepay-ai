import sys
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def evaluate_model(model, X_test, y_test, model_name: str = "Model") -> dict:
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
        roc_auc = float(roc_auc_score(y_test, y_prob))
    else:
        y_prob = None
        roc_auc = float(roc_auc_score(y_test, y_pred))
        
    return {
        "model_name": model_name,
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": roc_auc,
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "y_pred": y_pred,
        "y_prob": y_prob
    }

def print_evaluation_report(metrics: dict):
    name = metrics["model_name"]
    cm = metrics["confusion_matrix"]
    tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]
    
    print(f"\n{'='*55}")
    print(f">> PERFORMANCE EVALUATION: {name.upper()}")
    print(f"{'='*55}")
    print(f" * Accuracy:   {metrics['accuracy']*100:.2f}%")
    print(f" * Precision:  {metrics['precision']*100:.2f}% (Low False Alarms)")
    print(f" * Recall:     {metrics['recall']*100:.2f}% (Caught Frauds)")
    print(f" * F1-Score:   {metrics['f1_score']:.4f}")
    print(f" * ROC-AUC:    {metrics['roc_auc']:.4f}")
    print(f"\n--- Confusion Matrix ---")
    print(f" True Legit (TN): {tn:,} | False Alarms (FP): {fp:,}")
    print(f" Missed (FN):     {fn:,} | Caught Frauds (TP): {tp:,}")
    print(f"{'='*55}")