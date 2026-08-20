"""
SafePay AI™ - Easy Payment Safety & Scam Shield
Features:
- Simple, plain English options for spending money (no confusing jargon).
- Smart detection: Legitimate large self-spending/withdrawals are recognized as SAFE.
- High-contrast, clean dark theme.
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Path configurations
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, "src")
data_dir = os.path.join(base_dir, "data")
models_dir = os.path.join(base_dir, "models")

sys.path.insert(0, src_dir)
sys.path.insert(0, data_dir)

from preprocessing import prepare_data
from train import train_all_models
from predict import FraudDetector
from generate_data import generate_transaction_dataset

st.set_page_config(
    page_title="SafePay AI™ | Payment Safety & Scam Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Modern Dark Theme -----------------
st.sidebar.markdown("""
<div style="padding: 12px 0 18px 0; border-bottom: 1px solid #334155; margin-bottom: 18px;">
    <div style="font-size: 1.45rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.5px; display: flex; align-items: center; gap: 8px;">
        🛡️ SafePay <span style="color: #38BDF8;">AI™</span>
    </div>
    <div style="font-size: 0.78rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin-top: 4px;">
        Payment Safety & Scam Shield
    </div>
</div>
""", unsafe_allow_html=True)

senior_mode = st.sidebar.toggle("👵 Big Text Mode (Easy to Read)", value=True)

dark_theme_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* 1. Global App Background */
    .stApp {{
        background-color: #0A0F1D !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    
    /* 2. Sidebar */
    [data-testid="stSidebar"] {{
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }}
    
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}

    /* 3. Global Typography */
    html, body, [class*="css"], p, span, label, div, li {{
        color: #FFFFFF !important;
        font-size: {'1.15rem' if senior_mode else '1.0rem'};
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
    }}
    
    /* 4. Top Header & Hero Branding */
    .hero-container {{
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }}
    
    .hero-title {{
        font-size: {'2.3rem' if senior_mode else '1.95rem'} !important;
        font-weight: 900;
        color: #FFFFFF !important;
        letter-spacing: -0.8px;
        margin: 0;
    }}
    
    .hero-desc {{
        font-size: {'1.18rem' if senior_mode else '1.05rem'} !important;
        color: #94A3B8 !important;
        margin-top: 4px;
        margin-bottom: 0;
    }}
    
    .live-status-pill {{
        background-color: rgba(16, 185, 129, 0.15);
        border: 1px solid #10B981;
        color: #34D399 !important;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 0.88rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }}

    /* 5. Elevated Dark Cards */
    .pro-card {{
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }}
    
    .preset-box {{
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-left: 6px solid #38BDF8 !important;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    }}

    .tip-card {{
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-left: 5px solid #0EA5E9 !important;
        border-radius: 10px;
        padding: 15px 18px;
        margin-bottom: 12px;
    }}

    /* 6. Verdict Banners */
    .safe-banner {{
        background: linear-gradient(135deg, #064E3B 0%, #042F24 100%) !important;
        border: 2px solid #10B981 !important;
        border-left: 8px solid #10B981 !important;
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.25);
    }}
    
    .warn-banner {{
        background: linear-gradient(135deg, #78350F 0%, #451A03 100%) !important;
        border: 2px solid #F59E0B !important;
        border-left: 8px solid #F59E0B !important;
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.25);
    }}
    
    .danger-banner {{
        background: linear-gradient(135deg, #7F1D1D 0%, #450A0A 100%) !important;
        border: 2px solid #EF4444 !important;
        border-left: 8px solid #EF4444 !important;
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3);
    }}

    /* 7. Input Form Container */
    [data-testid="stForm"] {{
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 16px;
        padding: 26px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }}
    
    input, select, textarea, [data-baseweb="input"], [data-baseweb="select"] {{
        background-color: #0A0F1D !important;
        color: #FFFFFF !important;
        border: 1.5px solid #475569 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    
    input:focus, select:focus {{
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2) !important;
    }}

    /* 8. Modern Metric Ribbons */
    [data-testid="stMetric"] {{
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 14px;
        padding: 18px 22px;
    }}
    
    [data-testid="stMetricValue"] {{
        color: #38BDF8 !important;
        font-weight: 900 !important;
        font-size: 1.85rem !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: #94A3B8 !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* 9. Interactive Buttons */
    .stButton>button {{
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1.5px solid #475569 !important;
        border-radius: 10px;
        font-weight: 700;
        min-height: 48px;
        padding: 10px 20px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .stButton>button:hover {{
        background-color: #334155 !important;
        border-color: #38BDF8 !important;
        color: #38BDF8 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.25);
    }}
    
    button[kind="primary"] {{
        background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%) !important;
        color: #0A0F1D !important;
        border: none !important;
        font-weight: 900 !important;
        min-height: 52px !important;
        font-size: 1.15rem !important;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(56, 189, 248, 0.4);
    }}
    
    button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #0EA5E9 0%, #0369A1 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(56, 189, 248, 0.55);
    }}
    
    .sidebar-helpline {{
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #38BDF8;
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    }}
</style>
"""

st.markdown(dark_theme_css, unsafe_allow_html=True)

# ----------------- Data & Model Engine -----------------
@st.cache_data
def get_dataset():
    csv_file = os.path.join(data_dir, "transactions.csv")
    if not os.path.exists(csv_file):
        os.makedirs(data_dir, exist_ok=True)
        df_gen = generate_transaction_dataset(n_samples=15000, fraud_ratio=0.03, random_state=42)
        df_gen.to_csv(csv_file, index=False)
    else:
        df_gen = pd.read_csv(csv_file)
    return df_gen

df = get_dataset()

# Ensure model artifacts exist
best_model_file = os.path.join(models_dir, "best_model.joblib")
if not os.path.exists(best_model_file):
    with st.spinner("Initializing SafePay AI Threat Shield..."):
        train_all_models(data_path=os.path.join(data_dir, "transactions.csv"), models_dir=models_dir)

detector = FraudDetector(models_dir=models_dir)

# ----------------- Sidebar Navigation -----------------
st.sidebar.markdown("### 📍 What would you like to do?")
menu_choice = st.sidebar.radio(
    "Choose a page:",
    [
        "🔍 Check If a Payment is Safe",
        "🛡️ Common Scams & How to Protect Yourself",
        "📊 Live Cyber Fraud Statistics & Trends"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-helpline">
    <div style="font-size: 0.8rem; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.5px;">🚨 Emergency Cyber Helpline</div>
    <div style="font-size: 1.45rem; font-weight: 900; color: #FFFFFF; margin: 4px 0;">📞 Dial: 1930</div>
    <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.4;">Toll-Free National Government Helpline (24x7).</div>
    <div style="margin-top: 8px;"><a href="https://cybercrime.gov.in" target="_blank" style="color: #38BDF8; text-decoration: underline; font-weight: 700; font-size: 0.85rem;">Official Portal: cybercrime.gov.in</a></div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SECTION 1: CHECK IF A PAYMENT IS SAFE
# ==============================================================================
if menu_choice == "🔍 Check If a Payment is Safe":
    st.markdown("""
    <div class="hero-container">
        <div>
            <h1 class="hero-title">Check If a Payment is Safe</h1>
            <div class="hero-desc">Before sending money or paying an unknown person, enter the details below. Our AI will tell you if it is safe or a scam.</div>
        </div>
        <div class="live-status-pill">
            <span style="font-size: 10px;">🟢</span> AI PROTECTION ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="preset-box">
        <b style="color: #FFFFFF; font-size: 1.12rem;">💡 Try a Common Example: Click any story button below to test:</b>
    </div>
    """, unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    
    # Defaults
    spending_choice = "🛍️ Buying something at a store or online (Shopping, Groceries, Medicines)"
    amount_val = 65.00
    old_orig_val = 3500.00
    new_orig_val = 3435.00
    old_dest_val = 200.00
    new_dest_val = 265.00
    hour_val = 15
    dist_val = 4.0
    abroad_val = False
    is_self_val = True
    
    if col_s1.button("🛒 Story 1: Buying Groceries / Medicine", key="btn_story_1", use_container_width=True):
        spending_choice = "🛍️ Buying something at a store or online (Shopping, Groceries, Medicines)"
        amount_val = 45.50
        old_orig_val = 2800.00
        new_orig_val = 2754.50
        old_dest_val = 150.00
        new_dest_val = 195.50
        hour_val = 16
        dist_val = 3.5
        abroad_val = False
        is_self_val = True
        st.success("Loaded Story 1: Everyday shopping at 4:00 PM.")

    if col_s2.button("🏧 Story 2: Large Cash Withdrawal for Myself", key="btn_story_2", use_container_width=True):
        spending_choice = "🏧 Withdrawing cash from ATM for myself"
        amount_val = 25000.00
        old_orig_val = 80000.00
        new_orig_val = 55000.00
        old_dest_val = 0.00
        new_dest_val = 25000.00
        hour_val = 11
        dist_val = 2.0
        abroad_val = False
        is_self_val = True
        st.success("Loaded Story 2: Authorized cash withdrawal of ₹25,000 for personal use.")

    if col_s3.button("📱 Story 3: Urgent Bill Threat Phone Call", key="btn_story_3", use_container_width=True):
        spending_choice = "📲 Sending money to another person (Friend, Unknown person, Seller)"
        amount_val = 12000.00
        old_orig_val = 15000.00
        new_orig_val = 3000.00
        old_dest_val = 0.00
        new_dest_val = 12000.00
        hour_val = 22
        dist_val = 85.0
        abroad_val = False
        is_self_val = False
        st.warning("Loaded Story 3: Late-night phone call demanding urgent money to stop electricity cut-off.")

    if col_s4.button("🚨 Story 4: Fake Lottery Account Drain", key="btn_story_4", use_container_width=True):
        spending_choice = "📲 Sending money to another person (Friend, Unknown person, Seller)"
        amount_val = 75000.00
        old_orig_val = 75000.00
        new_orig_val = 0.00
        old_dest_val = 0.00
        new_dest_val = 75000.00
        hour_val = 2
        dist_val = 450.0
        abroad_val = True
        is_self_val = False
        st.error("Loaded Story 4: Entire bank balance emptied at 2:00 AM to an unknown overseas account.")

    st.markdown("---")
    
    with st.form("scanner_form"):
        st.markdown("<h3 style='color: #38BDF8; margin-top: 0; font-size: 1.3rem; font-weight: 800;'>📝 Step 1: Tell us about this payment</h3>", unsafe_allow_html=True)
        
        spending_options = [
            "🛍️ Buying something at a store or online (Shopping, Groceries, Medicines)",
            "🏧 Withdrawing cash from ATM for myself",
            "🔄 Paying a regular bill or auto-debit (Electricity, Rent, Insurance, EMIs)",
            "📲 Sending money to another person (Friend, Unknown person, Seller)",
            "🏦 Depositing cash into my bank account"
        ]
        
        current_index = 0
        for i, opt in enumerate(spending_options):
            if opt == spending_choice:
                current_index = i
                break
                
        ui_purpose = st.selectbox(
            "1. What are you doing with this money?",
            spending_options,
            index=current_index
        )
        
        # Map simple english to internal model types
        if "Buying" in ui_purpose:
            raw_type = "PAYMENT"
        elif "Withdrawing" in ui_purpose:
            raw_type = "CASH_OUT"
        elif "Paying a regular bill" in ui_purpose:
            raw_type = "DEBIT"
        elif "Sending money" in ui_purpose:
            raw_type = "TRANSFER"
        else:
            raw_type = "CASH_IN"

        c1, c2 = st.columns(2)
        with c1:
            ui_amount = st.number_input("2. How much money is being sent or withdrawn? (₹ / $)", min_value=1.0, max_value=1000000.0, value=float(amount_val), step=100.0)
            ui_hour = st.slider("3. What time of the day is it? (24-Hour Clock)", 0, 23, int(hour_val), format="%02d:00 hrs")
            
        with c2:
            ui_old_orig = st.number_input("4. Your Bank Balance BEFORE this payment", min_value=0.0, max_value=2000000.0, value=float(old_orig_val), step=500.0)
            ui_new_orig = st.number_input("5. Your Bank Balance AFTER this payment", min_value=0.0, max_value=2000000.0, value=float(new_orig_val), step=500.0)

        c3, c4 = st.columns(2)
        with c3:
            ui_dist = st.slider("6. Distance from your home (in km)", 0.5, 500.0, float(dist_val), step=1.0)
            ui_self = st.checkbox("👤 Is this for yourself or your family? (Self withdrawal, own shopping, own bills)", value=bool(is_self_val))
            
        with c4:
            ui_abroad = st.checkbox("🚩 Is the money going to a foreign / international account?", value=bool(abroad_val))

        scan_btn = st.form_submit_button("🔍 CHECK THIS PAYMENT NOW", type="primary", use_container_width=True)
        
    if scan_btn:
        tx_dict = {
            'type': raw_type,
            'amount': ui_amount,
            'oldbalanceOrg': ui_old_orig,
            'newbalanceOrig': ui_new_orig,
            'oldbalanceDest': 0.0,
            'newbalanceDest': ui_amount,
            'hour_of_day': ui_hour,
            'distance_from_home': ui_dist,
            'is_abroad': 1 if ui_abroad else 0,
            'is_self_use': ui_self
        }
        
        res = detector.predict_transaction(tx_dict)
        risk = res['risk_score_percentage']
        
        st.markdown("---")
        st.markdown("<h2 style='color: #FFFFFF; font-size: 1.55rem; font-weight: 800;'>📋 Safety Verdict & AI Advice</h2>", unsafe_allow_html=True)
        
        v_col1, v_col2 = st.columns([1, 2])
        
        with v_col1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Danger Meter", 'font': {'size': 22, 'color': '#FFFFFF'}},
                number={'suffix': "%", 'font': {'color': '#38BDF8', 'size': 40, 'weight': 'bold'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#94A3B8"},
                    'bar': {'color': "#EF4444" if risk >= 75 else ("#F59E0B" if risk >= 40 else "#10B981")},
                    'bgcolor': "#0A0F1D",
                    'steps': [
                        {'range': [0, 40], 'color': "#064E3B"},
                        {'range': [40, 75], 'color': "#78350F"},
                        {'range': [75, 100], 'color': "#7F1D1D"}
                    ],
                    'threshold': {'line': {'color': "#38BDF8", 'width': 4}, 'thickness': 0.85, 'value': risk}
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="#1E293B",
                plot_bgcolor="#1E293B",
                height=270,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_gauge, use_container_width=True, key="live_scanner_gauge_chart")
            
        with v_col2:
            if risk >= 75:
                st.markdown(f"""
                <div class="danger-banner">
                    <div style="font-size: 0.85rem; font-weight: 800; color: #FCA5A5; text-transform: uppercase; letter-spacing: 0.5px;">Safety Verdict: STOP / HIGH DANGER</div>
                    <h2 style="margin: 4px 0 8px 0; color: #FFFFFF; font-size: 1.65rem; font-weight: 900;">🚨 STOP! HIGH SCAM DANGER ({risk}%)</h2>
                    <p style="color: #FFFFFF; margin-bottom: 0; font-size: 1.15rem; font-weight: 800;">DO NOT SEND THIS MONEY!</p>
                    <p style="color: #CBD5E1; margin-top: 4px;">This payment looks like a real phone scam or account theft attempting to take your money.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<h4 style='color: #F87171; margin-top: 16px; font-weight: 800;'>🛑 Immediate Safety Actions:</h4>", unsafe_allow_html=True)
                st.error("1. Hang up any phone call asking you to transfer money or install AnyDesk.")
                st.error("2. Never tell your 6-digit OTP, UPI PIN, or bank password to anyone.")
                st.error("3. If you already sent money, call helpline 1930 immediately.")
                
            elif risk >= 40:
                st.markdown(f"""
                <div class="warn-banner">
                    <div style="font-size: 0.85rem; font-weight: 800; color: #FDE68A; text-transform: uppercase; letter-spacing: 0.5px;">Safety Verdict: CHECK CAREFULLY</div>
                    <h2 style="margin: 4px 0 8px 0; color: #FFFFFF; font-size: 1.65rem; font-weight: 900;">⚠️ CAUTION! SUSPICIOUS PAYMENT ({risk}%)</h2>
                    <p style="color: #FFFFFF; margin-bottom: 0; font-size: 1.15rem; font-weight: 800;">VERIFY BEFORE SENDING</p>
                    <p style="color: #CBD5E1; margin-top: 4px;">This payment has unusual signs (such as late-night timing, large amount, or unfamiliar receiver).</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<h4 style='color: #FBBF24; margin-top: 16px; font-weight: 800;'>💡 Safety Checklist:</h4>", unsafe_allow_html=True)
                st.warning("• Call the receiver on their official phone number to double check.")
                st.warning("• If you received an SMS threatening disconnection, pay only on the official government website.")
                
            else:
                st.markdown(f"""
                <div class="safe-banner">
                    <div style="font-size: 0.85rem; font-weight: 800; color: #A7F3D0; text-transform: uppercase; letter-spacing: 0.5px;">Safety Verdict: VERIFIED SAFE</div>
                    <h2 style="margin: 4px 0 8px 0; color: #FFFFFF; font-size: 1.65rem; font-weight: 900;">✅ ALL CLEAR! SAFE PAYMENT ({risk}%)</h2>
                    <p style="color: #FFFFFF; margin-bottom: 0; font-size: 1.15rem; font-weight: 800;">AUTHORIZED PERSONAL TRANSACTION</p>
                    <p style="color: #CBD5E1; margin-top: 4px;">This payment is completely safe and normal. You have sufficient balance for your personal use.</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<h4 style='color: #38BDF8; margin-top: 18px; font-weight: 800;'>🔍 What our AI checked for you:</h4>", unsafe_allow_html=True)
            for reason in res['reasons']:
                st.markdown(f"""
                <div class="tip-card">
                    <span style="color: #38BDF8; font-weight: 900;">✓</span> <b style="color: #FFFFFF;">{reason}</b>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# SECTION 2: COMMON SCAMS & PROTECTION GUIDE
# ==============================================================================
elif menu_choice == "🛡️ Common Scams & How to Protect Yourself":
    st.markdown("""
    <div class="hero-container">
        <div>
            <h1 class="hero-title">Common Cyber Scams & How to Stay Safe</h1>
            <div class="hero-desc">Learn the common tricks scammers use to steal money from people, and simple rules to protect yourself.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="pro-card" style="border: 2px solid #EF4444; border-left: 8px solid #EF4444;">
        <h3 style="color: #F87171; margin: 0 0 8px 0; font-size: 1.35rem; font-weight: 900;">🔒 The Golden Rule of Banking:</h3>
        <p style="font-size: 1.15rem; color: #FFFFFF; margin: 0; line-height: 1.6; font-weight: 700;">
            NO REAL BANK MANAGER, POLICE OFFICER, OR ELECTRICITY OFFICER WILL EVER ASK FOR YOUR 6-DIGIT OTP, PIN, OR PASSWORD OVER THE PHONE.<br>
            <span style="color: #FCA5A5;">If anyone on a call asks for your OTP, they are 100% a fraudster. Hang up immediately!</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    scam_tab1, scam_tab2, scam_tab3, scam_tab4 = st.tabs([
        "⚡ 1. Fake Electricity Bill Threat",
        "🎁 2. Fake Lottery & Prize Call",
        "📲 3. Screen Sharing App Trap (AnyDesk)",
        "👵 4. Fake Pension / KYC Call"
    ])
    
    with scam_tab1:
        st.markdown("""
        <div class="tip-card">
            <h4 style="color: #FFFFFF; margin-top: 0; font-weight: 800;">⚡ 1. The Fake Electricity Bill Scam</h4>
            <p><b>The Trick:</b> You get an SMS: <i>"Your electricity will be cut off tonight at 9:30 PM because your bill is unpaid. Call this officer immediately at 98xxxxxx."</i></p>
            <p><b>What Happens:</b> When you call, the scammer asks you to pay ₹10 on a mobile link. Once you enter your UPI PIN, they steal ₹50,000 from your account!</p>
            <p><b style="color: #38BDF8;">How to stay safe:</b> Never call numbers received via SMS. Pay bills only at the official office or your official utility app.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with scam_tab2:
        st.markdown("""
        <div class="tip-card">
            <h4 style="color: #FFFFFF; margin-top: 0; font-weight: 800;">🎁 2. The Fake Lottery & Prize Draw</h4>
            <p><b>The Trick:</b> A message or call congratulates you on winning a ₹25 Lakh lottery or celebrity lucky draw.</p>
            <p><b>What Happens:</b> They ask you to transfer ₹5,000 as 'government processing fees' to release your prize money. Once paid, they demand more and vanish.</p>
            <p><b style="color: #38BDF8;">How to stay safe:</b> You can never win a lottery that you did not purchase a ticket for.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with scam_tab3:
        st.markdown("""
        <div class="tip-card">
            <h4 style="color: #FFFFFF; margin-top: 0; font-weight: 800;">📲 3. Screen Sharing App Trap (AnyDesk / TeamViewer)</h4>
            <p><b>The Trick:</b> A caller claiming to be a technical support executive says: <i>"Sir, your banking app has a technical bug. Install 'AnyDesk' so we can fix it for you."</i></p>
            <p><b>What Happens:</b> AnyDesk allows the caller to see your phone screen live, view your passwords, and read your banking OTPs in real-time.</p>
            <p><b style="color: #38BDF8;">How to stay safe:</b> NEVER install AnyDesk, TeamViewer, or QuickSupport on the instructions of any caller.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with scam_tab4:
        st.markdown("""
        <div class="tip-card">
            <h4 style="color: #FFFFFF; margin-top: 0; font-weight: 800;">👵 4. Fake Pension & Bank Account KYC Update</h4>
            <p><b>The Trick:</b> A caller claims your pension is on hold because your Aadhaar KYC has expired, demanding your card details and OTP.</p>
            <p><b>What Happens:</b> They initiate an unauthorized transaction and ask you for the OTP received on your mobile.</p>
            <p><b style="color: #38BDF8;">How to stay safe:</b> Always complete KYC updates in-person at your official bank branch or through official verified apps.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("<h3 style='color: #FFFFFF; font-size: 1.3rem; font-weight: 800;'>❓ Quick Safety Quiz: What Would You Do?</h3>", unsafe_allow_html=True)
    
    q1 = st.radio(
        "A caller says they represent your bank and asks for the 6-digit OTP sent to your phone to reverse a fraud transaction. What should you do?",
        [
            "A) Share the OTP quickly so they can stop the transaction.",
            "B) Hang up immediately and NEVER share the OTP with anyone.",
            "C) Send a screenshot of the SMS via WhatsApp."
        ],
        key="senior_safety_quiz_q1"
    )
    if st.button("Check My Answer", key="btn_check_q1"):
        if "B)" in q1:
            st.success("✅ CORRECT! Never share your OTP. Real banks will never ask for your OTP or PIN over the phone.")
        else:
            st.error("❌ CRITICAL RISK! Sharing your OTP allows the scammer to take money out of your account!")

# ==============================================================================
# SECTION 3: LIVE CYBER FRAUD STATISTICS & TRENDS
# ==============================================================================
elif menu_choice == "📊 Live Cyber Fraud Statistics & Trends":
    st.markdown("""
    <div class="hero-container">
        <div>
            <h1 class="hero-title">Live Cyber Fraud Statistics & Trends</h1>
            <div class="hero-desc">Aggregated telemetry, distribution patterns, and insights across 15,000 analyzed financial transactions.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    total = len(df)
    n_fraud = (df['isFraud'] == 1).sum()
    n_legit = (df['isFraud'] == 0).sum()
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Payments Analyzed", f"{total:,}")
    m2.metric("Verified Safe Payments", f"{n_legit:,}", "97.0%")
    m3.metric("Scam Attempts Stopped", f"{n_fraud:,}", "-3.0%", delta_color="inverse")
    m4.metric("Incident Ratio", f"1 in {int(n_legit/n_fraud)} events")
    
    st.markdown("---")
    
    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("1. Which Payment Types Are Targeted Most?")
        fig_bar = px.histogram(
            df, x="type", color="isFraud", barmode="group",
            labels={"isFraud": "Status (0=Safe, 1=Fraud)", "type": "Payment Method"},
            color_discrete_map={0: "#38BDF8", 1: "#EF4444"},
            title="Fraud attempts are concentrated in Bank Transfers and Cash Withdrawals"
        )
        fig_bar.update_layout(
            paper_bgcolor="#1E293B",
            plot_bgcolor="#0A0F1D",
            font_color="#FFFFFF",
            legend=dict(font=dict(color="#FFFFFF")),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig_bar.update_xaxes(gridcolor="#334155")
        fig_bar.update_yaxes(gridcolor="#334155")
        st.plotly_chart(fig_bar, use_container_width=True, key="eda_bar_chart")
        
    with c_right:
        st.subheader("2. What Time Do Scammers Strike Most?")
        hourly = df.groupby(['hour_of_day', 'isFraud']).size().reset_index(name='count')
        fig_line = px.line(
            hourly, x="hour_of_day", y="count", color="isFraud",
            labels={"hour_of_day": "Hour of Day (0 to 23 hrs)", "count": "Transaction Volume", "isFraud": "Status"},
            color_discrete_map={0: "#10B981", 1: "#EF4444"},
            title="Notice peak fraud activity during late-night hours (11 PM - 4 AM)"
        )
        fig_line.update_layout(
            paper_bgcolor="#1E293B",
            plot_bgcolor="#0A0F1D",
            font_color="#FFFFFF",
            legend=dict(font=dict(color="#FFFFFF")),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig_line.update_xaxes(gridcolor="#334155")
        fig_line.update_yaxes(gridcolor="#334155")
        st.plotly_chart(fig_line, use_container_width=True, key="eda_line_chart")
        
    st.subheader("3. Comparison of Payment Amounts (Safe vs Fraud)")
    fig_b = px.box(
        df, x="isFraud", y="amount", color="isFraud", log_y=True,
        labels={"isFraud": "Status (0 = Safe, 1 = Fraud)", "amount": "Amount in ₹ / $"},
        color_discrete_map={0: "#38BDF8", 1: "#EF4444"},
        title="Fraud transactions attempt to steal significantly larger amounts than normal spending"
    )
    fig_b.update_layout(
        paper_bgcolor="#1E293B",
        plot_bgcolor="#0A0F1D",
        font_color="#FFFFFF",
        legend=dict(font=dict(color="#FFFFFF")),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig_b.update_xaxes(gridcolor="#334155")
    fig_b.update_yaxes(gridcolor="#334155")
    st.plotly_chart(fig_b, use_container_width=True, key="eda_box_chart")
    
    st.subheader("📄 Transaction Ledger Records")
    st.dataframe(df.head(15), use_container_width=True)