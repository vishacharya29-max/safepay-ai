"""
Synthetic Financial Transaction Dataset Generator
Generates realistic banking/e-commerce transaction data mimicking real-world
datasets (like Kaggle PaySim) with authentic fraud patterns.
"""

import os
import sys
import numpy as np
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def generate_transaction_dataset(n_samples: int = 15000, fraud_ratio: float = 0.03, random_state: int = 42) -> pd.DataFrame:
    np.random.seed(random_state)
    n_fraud = int(n_samples * fraud_ratio)
    n_legit = n_samples - n_fraud
    
    # 1. Legitimate Transactions
    legit_types = np.random.choice(
        ['PAYMENT', 'CASH_OUT', 'TRANSFER', 'CASH_IN', 'DEBIT'],
        size=n_legit,
        p=[0.40, 0.25, 0.15, 0.15, 0.05]
    )
    legit_amounts = np.round(np.random.lognormal(mean=5.0, sigma=1.4, size=n_legit), 2)
    legit_amounts = np.clip(legit_amounts, 5.0, 45000.0)
    
    legit_old_orig = np.round(np.random.uniform(500.0, 100000.0, size=n_legit), 2)
    legit_old_orig = np.maximum(legit_old_orig, legit_amounts + np.random.uniform(50.0, 5000.0, size=n_legit))
    legit_new_orig = np.maximum(0.0, legit_old_orig - legit_amounts)
    
    legit_old_dest = np.round(np.random.uniform(0.0, 100000.0, size=n_legit), 2)
    legit_new_dest = legit_old_dest + legit_amounts
    
    legit_hour_weights = np.array([
        0.01, 0.01, 0.01, 0.01, 0.01, 0.02, 0.03, 0.05, 0.07, 0.08, 0.08, 0.08, 
        0.08, 0.07, 0.06, 0.06, 0.06, 0.07, 0.06, 0.04, 0.02, 0.01, 0.01, 0.01
    ])
    p_legit_hours = legit_hour_weights / legit_hour_weights.sum()
    legit_hours = np.random.choice(range(24), size=n_legit, p=p_legit_hours)
    
    legit_distance = np.round(np.random.exponential(scale=18.0, size=n_legit), 2)
    legit_distance = np.clip(legit_distance, 0.5, 250.0)
    legit_abroad = np.random.choice([0, 1], size=n_legit, p=[0.96, 0.04])
    
    df_legit = pd.DataFrame({
        'type': legit_types,
        'amount': legit_amounts,
        'oldbalanceOrg': legit_old_orig,
        'newbalanceOrig': legit_new_orig,
        'oldbalanceDest': legit_old_dest,
        'newbalanceDest': legit_new_dest,
        'hour_of_day': legit_hours,
        'distance_from_home': legit_distance,
        'is_abroad': legit_abroad,
        'isFraud': 0
    })
    
    # 2. Fraudulent Transactions
    fraud_types = np.random.choice(['TRANSFER', 'CASH_OUT', 'PAYMENT'], size=n_fraud, p=[0.55, 0.40, 0.05])
    large_fraud = np.round(np.random.uniform(8000.0, 98000.0, size=n_fraud), 2)
    micro_fraud = np.round(np.random.uniform(50.0, 800.0, size=n_fraud), 2)
    use_micro = np.random.rand(n_fraud) < 0.12
    fraud_amounts = np.where(use_micro, micro_fraud, large_fraud)
    
    drain_mask = np.random.rand(n_fraud) > 0.35
    fraud_old_orig = np.zeros(n_fraud)
    fraud_old_orig[drain_mask] = fraud_amounts[drain_mask]
    fraud_old_orig[~drain_mask] = np.round(fraud_amounts[~drain_mask] * np.random.uniform(1.02, 1.6, size=np.sum(~drain_mask)), 2)
    fraud_new_orig = np.maximum(0.0, fraud_old_orig - fraud_amounts)
    
    fraud_old_dest = np.random.choice([0.0, 200.0, 2000.0], size=n_fraud, p=[0.65, 0.25, 0.10])
    fraud_new_dest = fraud_old_dest + fraud_amounts
    
    fraud_hour_weights = np.array([
        0.08, 0.09, 0.09, 0.10, 0.08, 0.06, 0.03, 0.02, 0.02, 0.02, 0.02, 0.03,
        0.03, 0.03, 0.03, 0.04, 0.04, 0.04, 0.04, 0.05, 0.06, 0.07, 0.07, 0.06
    ])
    p_fraud_hours = fraud_hour_weights / fraud_hour_weights.sum()
    fraud_hours = np.random.choice(range(24), size=n_fraud, p=p_fraud_hours)
    
    fraud_distance = np.round(np.random.uniform(25.0, 500.0, size=n_fraud), 2)
    fraud_abroad = np.random.choice([0, 1], size=n_fraud, p=[0.55, 0.45])
    
    df_fraud = pd.DataFrame({
        'type': fraud_types,
        'amount': fraud_amounts,
        'oldbalanceOrg': fraud_old_orig,
        'newbalanceOrig': fraud_new_orig,
        'oldbalanceDest': fraud_old_dest,
        'newbalanceDest': fraud_new_dest,
        'hour_of_day': fraud_hours,
        'distance_from_home': fraud_distance,
        'is_abroad': fraud_abroad,
        'isFraud': 1
    })
    
    df = pd.concat([df_legit, df_fraud], ignore_index=True)
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    return df

def save_default_dataset(output_path: str = None) -> str:
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "transactions.csv")
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print("Generating synthetic financial transaction dataset...")
    df = generate_transaction_dataset(n_samples=15000, fraud_ratio=0.03, random_state=42)
    df.to_csv(output_path, index=False)
    print(f"[OK] Dataset saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    save_default_dataset()