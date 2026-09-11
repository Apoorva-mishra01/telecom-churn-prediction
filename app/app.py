import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Churn Predictor",
    page_icon="📊",
    layout="wide"
)

# ---- Custom CSS for polish ----
st.markdown("""
    <style>
    .block-container {
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    h1 {
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        margin-bottom: 0.5rem !important;
    }
    .subtitle {
        font-size: 1.15rem;
        color: #A1A1AA;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 14px 24px;
        font-size: 1.15rem;
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab"] p {
        font-size: 1.15rem !important;
    }
    div[data-testid="column"] {
        padding: 0 16px;
    }
    .stSelectbox, .stSlider, .stNumberInput {
        margin-bottom: 1.4rem;
    }
    .stSelectbox label, .stSlider label, .stNumberInput label {
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }
    .stButton>button {
        background-color: #8B5CF6;
        color: white;
        border-radius: 8px;
        padding: 0.85rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        width: 100%;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #7C3AED;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .stAlert {
        border-radius: 10px;
        padding: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Header ----
st.title("📊 Telecom Customer Churn Predictor")
st.markdown(
    '<p class="subtitle">🎯 Instantly assess a customer\'s risk of cancellation using their account, service, and billing profile — powered by a trained machine learning model.</p>',
    unsafe_allow_html=True
)
st.divider()

# ---- Input tabs ----
tab1, tab2, tab3, tab4 = st.tabs(["👤 Demographics", "📋 Account", "🌐 Services", "💳 Billing"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
    with col2:
        partner = st.selectbox("Has Partner", ["Yes", "No"])
        dependents = st.selectbox("Has Dependents", ["Yes", "No"])

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        tenure = st.slider("Tenure (months)", min_value=0, max_value=72, value=12)
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    with col2:
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
        ])

with tab3:
    col1, col2, col3 = st.columns(3)
    with col1:
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    with col2:
        online_security = st.selectbox("Online Security", ["Yes", "No"])
        online_backup = st.selectbox("Online Backup", ["Yes", "No"])
        device_protection = st.selectbox("Device Protection", ["Yes", "No"])
    with col3:
        tech_support = st.selectbox("Tech Support", ["Yes", "No"])
        streaming_tv = st.selectbox("Streaming TV", ["Yes", "No"])
        streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No"])

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=70.0)
    with col2:
        total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, value=1000.0)

st.divider()

# ---- Prediction ----
predict_clicked = st.button("🔮 Predict Churn")

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

    scaler = joblib.load('../models/scaler.pkl')
    model = joblib.load('../models/final_churn_model.pkl')

    input_scaled = scaler.transform(input_df)

    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    st.divider()
    st.subheader("Prediction Result")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(
            label="Churn Probability",
            value=f"{probability:.1%}",
            delta="High Risk" if prediction == 1 else "Low Risk",
            delta_color="inverse" if prediction == 1 else "normal"
        )

    with col2:
        if prediction == 1:
            st.error("⚠️ **This customer is likely to churn.** Consider proactive retention outreach — special offers, contract upgrade incentives, or a support check-in.")
        else:
            st.success("✅ **This customer is likely to stay.** No immediate retention action needed based on current profile.")

        st.progress(float(probability))

    st.caption("This is a demo project for educational purposes. Predictions are based on a simplified model and should not be used for actual business decisions.")