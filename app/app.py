import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import altair as alt

# ==============================================================================
# 1. PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="Telecom Churn Intelligence Hub",
    page_icon="📡",
    layout="wide"
)

# ==============================================================================
# 2. ADVANCED MODERN CSS STYLING
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        max-width: 1360px;
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    .hero-container {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(168, 85, 247, 0.08) 50%, rgba(59, 130, 246, 0.05) 100%);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 18px;
        padding: 2rem 2.4rem;
        margin-bottom: 1.8rem;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(129, 140, 248, 0.3);
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .hero-title {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin: 0 0 0.5rem 0 !important;
        background: linear-gradient(135deg, #ffffff 40%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        color: #94a3b8;
        line-height: 1.6;
        max-width: 820px;
        margin: 0;
    }

    .snapshot-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 0.9rem 1.4rem;
        margin-bottom: 1.6rem;
        align-items: center;
    }

    .snapshot-item {
        display: flex;
        flex-direction: column;
        gap: 2px;
        padding-right: 1.2rem;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    .snapshot-item:last-child {
        border-right: none;
    }
    .snapshot-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #64748b;
        font-weight: 600;
    }
    .snapshot-val {
        font-size: 0.95rem;
        font-weight: 600;
        color: #f1f5f9;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(15, 23, 42, 0.4);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.6rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 46px;
        padding: 0 20px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #94a3b8;
        transition: all 0.2s ease;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    }

    .custom-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.4rem;
        backdrop-filter: blur(12px);
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.05rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 1.2rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.85rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.12rem !important;
        border: none !important;
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35) !important;
        transition: all 0.25s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(124, 58, 237, 0.5) !important;
    }

    .risk-banner {
        border-radius: 16px;
        padding: 1.6rem 2rem;
        margin: 1.5rem 0 1.8rem 0;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .risk-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.16) 0%, rgba(185, 28, 28, 0.06) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    .risk-medium {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.16) 0%, rgba(180, 83, 9, 0.06) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .risk-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.16) 0%, rgba(5, 150, 105, 0.06) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .metric-chip {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
    }

    .metric-chip-label {
        font-size: 0.78rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .metric-chip-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #ffffff;
    }

    .badge-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .badge-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.35); }
    .badge-yellow { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.35); }
    .badge-green { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. ROBUST MODEL & SCALER LOADER
# ==============================================================================
@st.cache_resource(show_spinner=False)
def load_assets():
    candidate_paths = [
        Path(__file__).resolve().parent.parent / "models",
        Path(__file__).resolve().parent / "models",
        Path("models"),
        Path("../models"),
    ]
    
    scaler, model = None, None
    for folder in candidate_paths:
        s_file = folder / "scaler.pkl"
        m_file = folder / "final_churn_model.pkl"
        if s_file.exists() and m_file.exists():
            scaler = joblib.load(s_file)
            model = joblib.load(m_file)
            break
            
    if scaler is None or model is None:
        st.error("❌ Could not find scaler.pkl or final_churn_model.pkl in models/ directory.")
        st.stop()
        
    return scaler, model

scaler, model = load_assets()

THRESHOLD = 0.50

# ==============================================================================
# 4. HERO HEADER
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span>●</span> Telecom Enterprise AI Suite
    </div>
    <h1 class="hero-title">Customer Churn Intelligence Hub</h1>
    <p class="hero-subtitle">
        Predict a customer's likelihood of cancellation using their account, 
        service, and billing profile, powered by a trained machine learning model.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. INPUT SECTIONS
# ==============================================================================
tab_demo, tab_account, tab_services, tab_billing = st.tabs([
    "👤  Demographics",
    "📋  Contract & Account",
    "🌐  Services & Add-ons",
    "💳  Billing & Financials"
])

with tab_demo:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'>👤 Customer Demographic Profile</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen (65+)", ["No", "Yes"])
    with c2:
        partner = st.selectbox("Has Partner / Spouse", ["Yes", "No"])
        dependents = st.selectbox("Has Dependents", ["Yes", "No"])
    st.markdown("</div>", unsafe_allow_html=True)

with tab_account:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'>📋 Subscription Agreement & Account Details</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        tenure = st.slider(
            "Account Tenure (Months)",
            min_value=0, max_value=72,
            value=12,
            help="Length of time customer has stayed with company."
        )
        contract = st.selectbox("Contract Terms", ["Month-to-month", "One year", "Two year"])
    with c2:
        paperless_billing = st.selectbox("Paperless e-Billing", ["Yes", "No"])
        payment_method = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
        ])
    st.markdown("</div>", unsafe_allow_html=True)

with tab_services:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'>🌐 Telecommunication & Digital Services</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Core Connectivity**")
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Phone Lines", ["Yes", "No"])
        internet_service = st.selectbox("Internet Service Type", ["DSL", "Fiber optic", "No"])
    with c2:
        st.markdown("**Security & Protection**")
        online_security = st.selectbox("Online Security Shield", ["Yes", "No"])
        online_backup = st.selectbox("Cloud Backup", ["Yes", "No"])
        device_protection = st.selectbox("Device Protection Plan", ["Yes", "No"])
    with c3:
        st.markdown("**Support & Media**")
        tech_support = st.selectbox("Premium Tech Support", ["Yes", "No"])
        streaming_tv = st.selectbox("Streaming TV Service", ["Yes", "No"])
        streaming_movies = st.selectbox("Streaming Movies Service", ["Yes", "No"])
    st.markdown("</div>", unsafe_allow_html=True)

with tab_billing:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'>💳 Revenue & Invoicing Metrics</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        monthly_charges = st.number_input(
            "Current Monthly Charge ($)",
            min_value=10.0, max_value=250.0,
            value=70.0,
            step=2.5
        )
    with c2:
        total_charges = st.number_input(
            "Cumulative Lifetime Charges ($)",
            min_value=0.0, max_value=15000.0,
            value=1000.0,
            step=50.0,
            help="Cumulative amount billed over customer lifetime."
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="snapshot-bar">
    <div class="snapshot-item">
        <span class="snapshot-label">Tenure</span>
        <span class="snapshot-val">{tenure} mo</span>
    </div>
    <div class="snapshot-item">
        <span class="snapshot-label">Contract</span>
        <span class="snapshot-val">{contract}</span>
    </div>
    <div class="snapshot-item">
        <span class="snapshot-label">Internet</span>
        <span class="snapshot-val">{internet_service}</span>
    </div>
    <div class="snapshot-item">
        <span class="snapshot-label">Monthly Bill</span>
        <span class="snapshot-val">${monthly_charges:.2f}/mo</span>
    </div>
    <div class="snapshot-item">
        <span class="snapshot-label">Payment Method</span>
        <span class="snapshot-val">{payment_method}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. PREDICTION & ANALYTICS
# ==============================================================================
predict_clicked = st.button("🔮 Calculate Customer Churn Probability", use_container_width=True)

if predict_clicked:
    input_dict = {
        'gender': 1 if gender == 'Male' else 0,
        'SeniorCitizen': 1 if senior_citizen == 'Yes' else 0,
        'Partner': 1 if partner == 'Yes' else 0,
        'Dependents': 1 if dependents == 'Yes' else 0,
        'tenure': tenure,
        'PhoneService': 1 if phone_service == 'Yes' else 0,
        'MultipleLines': 1 if multiple_lines == 'Yes' else 0,
        'OnlineSecurity': 1 if online_security == 'Yes' else 0,
        'OnlineBackup': 1 if online_backup == 'Yes' else 0,
        'DeviceProtection': 1 if device_protection == 'Yes' else 0,
        'TechSupport': 1 if tech_support == 'Yes' else 0,
        'StreamingTV': 1 if streaming_tv == 'Yes' else 0,
        'StreamingMovies': 1 if streaming_movies == 'Yes' else 0,
        'PaperlessBilling': 1 if paperless_billing == 'Yes' else 0,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges,
        'InternetService_Fiber optic': 1 if internet_service == 'Fiber optic' else 0,
        'InternetService_No': 1 if internet_service == 'No' else 0,
        'Contract_One year': 1 if contract == 'One year' else 0,
        'Contract_Two year': 1 if contract == 'Two year' else 0,
        'PaymentMethod_Credit card (automatic)': 1 if payment_method == 'Credit card (automatic)' else 0,
        'PaymentMethod_Electronic check': 1 if payment_method == 'Electronic check' else 0,
        'PaymentMethod_Mailed check': 1 if payment_method == 'Mailed check' else 0,
    }

    input_df = pd.DataFrame([input_dict])
    input_scaled = scaler.transform(input_df)

    raw_probability = model.predict_proba(input_scaled)[0][1]
    is_churn = raw_probability >= THRESHOLD

    if raw_probability >= 0.60:
        risk_class = "HIGH"
        risk_banner_css = "risk-high"
        risk_badge = '<span class="badge-pill badge-red">CRITICAL RISK</span>'
        risk_headline = "⚠️ Severe Churn Risk Detected"
        risk_desc = "This customer demonstrates strong attrition indicators based on the model's learned patterns."
    elif raw_probability >= 0.35:
        risk_class = "MODERATE"
        risk_banner_css = "risk-medium"
        risk_badge = '<span class="badge-pill badge-yellow">MODERATE RISK</span>'
        risk_headline = "⚡ Elevated Churn Risk"
        risk_desc = "Customer profile exhibits some warning signals identified by the model."
    else:
        risk_class = "LOW"
        risk_banner_css = "risk-low"
        risk_badge = '<span class="badge-pill badge-green">LOW RISK</span>'
        risk_headline = "✅ Highly Stable Customer"
        risk_desc = "This customer shows strong retention characteristics based on the model's learned patterns."

    st.markdown(f"""
    <div class="risk-banner {risk_banner_css}">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.45rem; font-weight: 800; color: #fff;">{risk_headline}</span>
                {risk_badge}
            </div>
        </div>
        <p style="margin: 0; color: #e2e8f0; font-size: 1.05rem; line-height: 1.5;">{risk_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="metric-chip">
            <div class="metric-chip-label">Churn Probability</div>
            <div class="metric-chip-value" style="color: {'#ef4444' if raw_probability>=0.6 else '#f59e0b' if raw_probability>=0.35 else '#10b981'};">{raw_probability:.1%}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-chip">
            <div class="metric-chip-label">Prediction</div>
            <div class="metric-chip-value" style="font-size: 1.45rem;">{'🚨 Will Churn' if is_churn else '🟢 Will Stay'}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-chip">
            <div class="metric-chip-label">Monthly Revenue</div>
            <div class="metric-chip-value">${monthly_charges:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.progress(float(raw_probability))

    st.markdown("### 📊 Feature Attribution Breakdown")

    feature_names = scaler.feature_names_in_
    coefs = model.coef_[0]

    friendly_labels = {
        'tenure': 'Tenure Length',
        'MonthlyCharges': 'Monthly Bill Amount',
        'TotalCharges': 'Total Lifetime Charges',
        'InternetService_Fiber optic': 'Fiber Optic Service',
        'InternetService_No': 'No Internet Service',
        'Contract_Two year': 'Two-Year Contract',
        'Contract_One year': 'One-Year Contract',
        'PaymentMethod_Electronic check': 'Electronic Check Payment',
        'PaymentMethod_Credit card (automatic)': 'Auto Credit Card',
        'PaymentMethod_Mailed check': 'Mailed Check Payment',
        'StreamingMovies': 'Streaming Movies Add-on',
        'StreamingTV': 'Streaming TV Add-on',
        'MultipleLines': 'Multiple Phone Lines',
        'PhoneService': 'Phone Service',
        'PaperlessBilling': 'Paperless Billing',
        'DeviceProtection': 'Device Protection',
        'OnlineBackup': 'Online Backup Service',
        'OnlineSecurity': 'Online Security Add-on',
        'TechSupport': 'Tech Support Plan',
        'SeniorCitizen': 'Senior Citizen Status',
        'Partner': 'Has Partner',
        'Dependents': 'Has Dependents',
        'gender': 'Gender'
    }

    factors = []
    for f, s_val, c in zip(feature_names, input_scaled[0], coefs):
        impact = float(s_val * c)
        factors.append({
            'Feature': friendly_labels.get(f, f),
            'Impact': impact,
            'AbsImpact': abs(impact),
            'Direction': 'Pushes toward Churn 🔴' if impact > 0 else 'Protects from Churn 🟢'
        })

    factors_df = pd.DataFrame(factors).sort_values(by='AbsImpact', ascending=False).head(7)

    chart = alt.Chart(factors_df).mark_bar(cornerRadius=6, height=22).encode(
        x=alt.X('Impact:Q', title='Impact on Churn Log-Odds'),
        y=alt.Y('Feature:N', sort='-x', title=None),
        color=alt.Color(
            'Direction:N',
            scale=alt.Scale(
                domain=['Pushes toward Churn 🔴', 'Protects from Churn 🟢'],
                range=['#f87171', '#34d399']
            ),
            legend=alt.Legend(orient='bottom', title=None)
        ),
        tooltip=['Feature', 'Direction', alt.Tooltip('Impact:Q', format='+.2f')]
    ).properties(height=320).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)

    st.divider()
    report_data = {
        **input_dict,
        "ChurnProbability": round(float(raw_probability), 4),
        "PredictedChurn": int(is_churn),
        "RiskClassification": risk_class
    }
    report_df = pd.DataFrame([report_data])
    csv_bytes = report_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Prediction Report (CSV)",
        data=csv_bytes,
        file_name=f"churn_prediction_{tenure}m.csv",
        mime="text/csv",
        use_container_width=True
    )