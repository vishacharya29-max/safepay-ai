import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(base_dir, "src"))
sys.path.insert(0, os.path.join(base_dir, "data"))

from generate_data import save_default_dataset
from train import train_all_models
from predict import FraudDetector

def main():
    print(">>> 1. Creating Dataset...")
    save_default_dataset()
    print(">>> 2. Training Models...")
    train_all_models()
    print(">>> 3. Testing Predictor...")
    detector = FraudDetector()
    sample = {
        'type': 'TRANSFER', 'amount': 65000.0, 'oldbalanceOrg': 65000.0, 'newbalanceOrig': 0.0,
        'oldbalanceDest': 0.0, 'newbalanceDest': 65000.0, 'hour_of_day': 3, 'distance_from_home': 400.0, 'is_abroad': 1
    }
    print(detector.predict_transaction(sample))
    print("\n>>> Run 'streamlit run app.py' to launch the web dashboard!")

if __name__ == "__main__":
    main()