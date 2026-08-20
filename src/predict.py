import os
import sys
import joblib
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from preprocessing import engineer_features, encode_categorical_features

class FraudDetector:
    def __init__(self, models_dir: str = None):
        if models_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            models_dir = os.path.join(base_dir, "models")
            
        self.model = joblib.load(os.path.join(models_dir, "best_model.joblib"))
        self.scaler = joblib.load(os.path.join(models_dir, "scaler.joblib"))
        self.feature_columns = joblib.load(os.path.join(models_dir, "feature_columns.joblib"))

    def predict_transaction(self, transaction_data: dict) -> dict:
        df = pd.DataFrame([transaction_data])
        df_feat = engineer_features(df)
        df_encoded = encode_categorical_features(df_feat)
        
        for col in self.feature_columns:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
                
        df_ordered = df_encoded[self.feature_columns]
        scaled_input = self.scaler.transform(df_ordered)
        
        is_fraud = int(self.model.predict(scaled_input)[0])
        if hasattr(self.model, "predict_proba"):
            risk_score = float(self.model.predict_proba(scaled_input)[0][1])
        else:
            risk_score = 1.0 if is_fraud == 1 else 0.0
            
        risk_pct = round(risk_score * 100, 2)
        
        if risk_pct >= 75:
            risk_level, status = "CRITICAL RISK", "[ALERT] FRAUD DETECTED"
        elif risk_pct >= 40:
            risk_level, status = "MODERATE RISK", "[WARNING] SUSPICIOUS TRANSACTION"
        else:
            risk_level, status = "LOW RISK", "[OK] LEGITIMATE TRANSACTION"
            
        reasons = []
        if transaction_data.get('amount', 0) > 10000:
            reasons.append(f"High amount (${transaction_data['amount']:,.2f})")
        if transaction_data.get('type') in ['TRANSFER', 'CASH_OUT']:
            reasons.append(f"High risk type ({transaction_data['type']})")
        if transaction_data.get('hour_of_day', 12) in [23, 0, 1, 2, 3, 4, 5]:
            reasons.append(f"Odd hour ({transaction_data['hour_of_day']}:00)")
        if df_feat['is_drain_attempt'].iloc[0] == 1:
            reasons.append("Account drained to $0.00")
        if transaction_data.get('distance_from_home', 0) > 150:
            reasons.append(f"High distance ({transaction_data['distance_from_home']} km)")
        if transaction_data.get('is_abroad', 0) == 1:
            reasons.append("International transaction")
        if not reasons:
            reasons.append("Normal spending pattern.")
            
        return {
            "status": status,
            "is_fraud": is_fraud,
            "risk_score_percentage": risk_pct,
            "risk_level": risk_level,
            "reasons": reasons
        }

if __name__ == "__main__":
    detector = FraudDetector()
    sample = {
        'type': 'PAYMENT', 'amount': 45.50, 'oldbalanceOrg': 1500.0, 'newbalanceOrig': 1454.50,
        'oldbalanceDest': 300.0, 'newbalanceDest': 345.50, 'hour_of_day': 14, 'distance_from_home': 5.2, 'is_abroad': 0
    }
    print(detector.predict_transaction(sample))