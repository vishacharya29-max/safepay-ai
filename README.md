# safepay-ai
# 🛡️ SafePay AI

## Financial Fraud Detection & Cyber Scam Shield

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-3F4F75.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **SafePay AI is an intelligent Machine Learning platform designed to detect potentially fraudulent financial transactions and help users understand common digital banking scams.**

---

## 🌟 Overview

**SafePay AI** is a financial fraud detection and cyber scam awareness platform built using **Python, Machine Learning, and Streamlit**.

The system analyzes financial transaction information and provides a risk assessment to help identify potentially suspicious activity.

Along with fraud detection, SafePay AI provides a **Cyber Scam Defense Center** that explains common digital banking scams in simple language, with special attention to helping senior citizens and everyday users stay safe online.

### 🎯 Objectives

- Detect potentially fraudulent financial transactions.
- Analyze suspicious transaction patterns.
- Generate an understandable risk score.
- Provide human-readable explanations for predictions.
- Reduce unnecessary false-positive alerts.
- Educate users about common digital banking scams.
- Promote safer digital payment practices.

---

# 🚀 Key Features

### 🔍 AI Fraud Detection

Analyze financial transaction information using machine learning and identify potentially suspicious transactions.

### 📊 Risk Score

Generate a risk score based on transaction characteristics and present the result through an easy-to-understand interface.

### 🧠 Machine Learning

Use machine learning classification algorithms to identify patterns associated with fraudulent transactions.

### 💡 Explainable Results

Provide simple explanations about why a transaction may be considered safe, suspicious, or high risk.

### 👤 Context-Aware Detection

Use transaction context and additional rules to reduce unnecessary fraud alerts.

### 🛡️ Cyber Defense Center

Explain common digital banking scams and provide practical safety recommendations.

### 👴 Senior Citizen Protection

Present cyber safety information in simple language to help senior citizens understand common digital scams.

### 📈 Interactive Analytics

Visualize financial transaction and fraud patterns using interactive Plotly charts.

### 🚨 Cybercrime Assistance

Provide information about reporting cybercrime in India.

---

# 🧠 How SafePay AI Works

                Financial Transaction
                         │
                         ▼
              ┌─────────────────────┐
              │  Data Preprocessing  │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Feature Engineering │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Feature Scaling     │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Machine Learning    │
              │       Model         │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Fraud Prediction    │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Risk Score          │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Contextual Analysis │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ User-Friendly Result│
              └─────────────────────┘

---

# 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Streamlit
- Joblib
- Git & GitHub

---

# 📂 Project Structure

```text
safepay-ai/
│
├── app.py
├── requirements.txt
├── run_demo.py
├── README.md
├── LICENSE
├── .gitignore
│
├── data/
├── src/
└── models/

🚀 Installation & Setup
1. Clone the Repository
git clone https://github.com/vishacharya29-max/safepay-ai.git
cd safepay-ai
2. Create a Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Run SafePay AI
python -m streamlit run app.py

The application will open in your browser at:

http://localhost:8501
📊 Machine Learning

SafePay AI uses Machine Learning to analyze transaction patterns and identify potentially fraudulent activity.

Models Used
🌲 Random Forest Classifier
📈 Gradient Boosting Classifier
📊 Logistic Regression

The best-performing model is saved and used for prediction.

Important Transaction Factors

The system can analyze factors such as:

Transaction amount
Original account balance
New account balance
Balance changes
Transaction type
Transaction time
Transaction location
Account-draining behavior
Domestic or international transactions
🛡️ Cyber Scam Defense Center

SafePay AI also helps users understand common digital banking scams.

📱 Fake Electricity Bill Scam

Scammers may send messages claiming that your electricity connection will be disconnected unless you make an immediate payment.

Safety Tip: Always verify the message using the official electricity provider.

🎁 Fake Lottery Scam

A scammer may claim that you have won a large amount of money and ask you to pay a processing fee.

Safety Tip: Never pay money to claim an unexpected prize.

🖥️ Screen Sharing Scam

Scammers may ask you to install remote-access software to "fix" your banking application.

Safety Tip: Never allow unknown people to remotely access your phone or computer.

🪪 Fake KYC Scam

A scammer may claim that your bank account will be blocked unless you immediately update your KYC.

Safety Tip: Contact your bank using its official website or customer-care number.

🔐 OTP Scam

Scammers may ask for your OTP, ATM PIN, CVV, or password.

Safety Tip: Never share confidential banking information with anyone.

👴 Senior Citizen Safety

SafePay AI provides simple cyber-safety information that can be easily understood by senior citizens.

Remember:
❌ Never share your OTP.
❌ Never share your ATM PIN.
❌ Never share your CVV.
❌ Never share your banking password.
❌ Never install applications requested by unknown callers.
❌ Never click suspicious payment links.
❌ Never transfer money because someone is threatening you.
✅ Verify suspicious calls with your bank.
✅ Ask a trusted person if you are unsure.
✅ Report suspicious transactions immediately.
🚨 Cybercrime Reporting

If you become a victim of financial cybercrime in India, report the incident as soon as possible.

Cyber Crime Helpline

1930

National Cyber Crime Reporting Portal

https://www.cybercrime.gov.in/

Always verify important contact information through official government sources.

🔐 Security Notice

SafePay AI is an academic and portfolio project developed for educational and demonstration purposes.

It should not be considered a replacement for a bank's official fraud detection system or professional cybersecurity service.

A real-world production system would require additional security measures such as:

Secure authentication
Data encryption
Secure database management
API security
Rate limiting
Security monitoring
Model monitoring
Privacy protection
Regular security testing
🔮 Future Improvements

Future versions of SafePay AI may include:

🚀 Real-time transaction monitoring
💳 UPI fraud detection
📱 SMS scam detection
📧 Email scam detection
🧠 Explainable AI using SHAP
🌐 Multilingual support
🗣️ Voice assistance for senior citizens
📲 Mobile application
🚨 Real-time fraud alerts
🏦 Banking API integration
📊 Advanced security dashboard
🗣️ Kannada language support
🎓 Project Purpose

SafePay AI was developed as an AI/ML academic and portfolio project to demonstrate the application of Machine Learning in financial fraud detection and cybersecurity awareness.

The project combines:

Artificial Intelligence
        +
Machine Learning
        +
Data Analysis
        +
Cybersecurity Awareness
        +
User-Friendly Design
👨‍💻 Author

Vishacharya29-max

GitHub:

https://github.com/vishacharya29-max/safepay-ai

📄 License

This project is licensed under the MIT License.

See the LICENSE file for details.

❤️ SafePay AI

Think before you click. Verify before you pay. Stay safe online.
