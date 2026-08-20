import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

TRANSACTION_TYPES = ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['balance_error_orig'] = df['oldbalanceOrg'] - df['amount'] - df['newbalanceOrig']
    df['balance_error_dest'] = df['oldbalanceDest'] + df['amount'] - df['newbalanceDest']
    df['amount_to_oldbalance_ratio'] = df['amount'] / (df['oldbalanceOrg'] + 1.0)
    df['is_drain_attempt'] = (
        (df['oldbalanceOrg'] > 0) & 
        (np.abs(df['oldbalanceOrg'] - df['amount']) < 1.0) & 
        (df['newbalanceOrig'] == 0)
    ).astype(int)
    return df

def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for t in TRANSACTION_TYPES:
        df[f'type_{t}'] = (df['type'] == t).astype(int)
    if 'type' in df.columns:
        df = df.drop(columns=['type'])
    return df

def prepare_data(data_path: str, test_size: float = 0.2, random_state: int = 42):
    df = pd.read_csv(data_path)
    df = engineer_features(df)
    df = encode_categorical_features(df)
    
    X = df.drop(columns=['isFraud'])
    y = df['isFraud']
    feature_columns = list(X.columns)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_columns, X_train, X_test

def save_preprocessing_artifacts(scaler, feature_columns, models_dir: str = None):
    if models_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(scaler, os.path.join(models_dir, "scaler.joblib"))
    joblib.dump(feature_columns, os.path.join(models_dir, "feature_columns.joblib"))