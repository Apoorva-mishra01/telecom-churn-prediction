import streamlit as st
import pandas as pd
import joblib

st.title("Telecom Customer Churn Prediction")
st.write("Enter customer details to predict the likelihood of churn.")

st.header("Customer Demographics")

gender = st.selectbox("Gender", ["Male", "Female"])
senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
partner = st.selectbox("Has Partner", ["Yes", "No"])
dependents = st.selectbox("Has Dependents", ["Yes", "No"])
st.header("Account Information")

tenure = st.slider("Tenure (months)", min_value=0, max_value=72, value=12)
contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
payment_method = st.selectbox("Payment Method", [
    "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
])
st.header("Services")

phone_service = st.selectbox("Phone Service", ["Yes", "No"])
multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No"])
internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
online_security = st.selectbox("Online Security", ["Yes", "No"])
online_backup = st.selectbox("Online Backup", ["Yes", "No"])
device_protection = st.selectbox("Device Protection", ["Yes", "No"])
tech_support = st.selectbox("Tech Support", ["Yes", "No"])
streaming_tv = st.selectbox("Streaming TV", ["Yes", "No"])
streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No"])
st.header("Billing")

monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=70.0)
total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, value=1000.0)

if st.button("Predict Churn"):

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

    st.subheader("Prediction Result")

    if prediction == 1:
        st.error(f"⚠️ This customer is likely to churn. (Probability: {probability:.2%})")
    else:
        st.success(f"✅ This customer is likely to stay. (Probability of churn: {probability:.2%})")
