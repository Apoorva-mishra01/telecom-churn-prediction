# 📊 Telecom Customer Churn Prediction

A machine learning project that predicts whether a telecom customer is likely to cancel their subscription, based on their account, service, and billing details. Built as an end-to-end ML pipeline, from raw data to a deployed, interactive web application.

**🔗 Live App:** [telecom-churn-prediction08.streamlit.app](https://telecom-churn-prediction08.streamlit.app)

## Overview

Customer churn, when a customer stops using a company's service, is a major concern for subscription-based businesses like telecom providers, since acquiring a new customer typically costs far more than retaining an existing one. This project builds a classification model that predicts churn risk from customer data, allowing a business to proactively identify at-risk customers before they leave.

The project covers the full ML lifecycle: exploratory data analysis, data preprocessing, training and comparing 5 different classification models, hyperparameter tuning, feature importance interpretation, and deployment as an interactive Streamlit web application.

## Problem Statement

Telecom companies lose significant revenue when customers cancel their subscriptions. Identifying which customers are likely to churn, and understanding why, allows a business to intervene early with targeted retention efforts, rather than reacting after a customer has already left.

## Objectives

- Perform exploratory data analysis to understand patterns behind customer churn.
- Preprocess and clean real-world data, including handling data quality issues.
- Train and compare multiple classification models using appropriate evaluation metrics for an imbalanced dataset.
- Interpret which features most influence churn predictions.
- Deploy a working, interactive prediction tool.

## Dataset

- **Source:** [Telco Customer Churn dataset (Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn), originally provided by IBM.
- **Size:** 7,043 customers, 21 columns.
- **Target variable:** `Churn` (Yes/No), imbalanced, with ~73.5% "No" and ~26.5% "Yes".
- **Features:** customer demographics (gender, senior citizen status, partner/dependents), account details (tenure, contract type, payment method), subscribed services (internet, phone, streaming, security add-ons), and billing information (monthly and total charges).

## Tech Stack

- **Language:** Python
- **Data handling:** pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Altair
- **Machine learning:** scikit-learn
- **Model serialization:** joblib
- **Web application:** Streamlit
- **Deployment:** Streamlit Community Cloud
- **Version control:** Git, GitHub

## Exploratory Data Analysis

Key findings from EDA:
- **Contract type** is a strong predictor: month-to-month customers churn far more than one-year or two-year contract holders.
- **Tenure** is strongly inversely related to churn: churn is concentrated in the first few months of the customer relationship.
- **Monthly charges** show a moderate relationship: churned customers tend to pay somewhat more, though the effect is less pronounced than tenure or contract type.

## Data Preprocessing

- Dropped `customerID` (unique identifier, no predictive value).
- Fixed a data quality issue in `TotalCharges`, which was stored as text due to 11 blank-value rows (all corresponding to brand-new customers with `tenure = 0`); converted to numeric and imputed with 0.
- Encoded binary Yes/No columns directly to 0/1.
- Simplified service-dependent columns (e.g., `OnlineSecurity`) by merging the "No internet service" category into "No", since it was a structural artifact rather than a distinct answer choice.
- One-hot encoded multi-category columns (`InternetService`, `Contract`, `PaymentMethod`) with `drop_first=True` to avoid redundant, correlated columns.
- Split data into training (80%) and test (20%) sets using stratified sampling to preserve class balance.
- Applied `StandardScaler`, fit only on training data to avoid data leakage.

## Models Used

Five classification models were trained and compared: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, and K-Nearest Neighbors.

## Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| **Logistic Regression** | 0.807 | 0.659 | 0.564 | **0.608** | **0.842** |
| Decision Tree | 0.794 | 0.631 | 0.540 | 0.582 | 0.827 |
| Random Forest | 0.806 | 0.675 | 0.516 | 0.585 | 0.842 |
| Gradient Boosting | 0.798 | 0.654 | 0.505 | 0.570 | 0.841 |
| KNN | 0.747 | 0.525 | 0.500 | 0.512 | 0.772 |

Accuracy alone is misleading here given the ~73.5%/26.5% class imbalance, so F1-score and ROC-AUC were prioritized when comparing models.

## Final Model

**Logistic Regression** (tuned: `C=10`, `penalty='l2'`) was selected as the final model. Despite being the simplest model tried, it achieved the best F1-score and tied for the best ROC-AUC, even after hyperparameter tuning of Random Forest. This suggests the churn patterns in this dataset are largely linear and well-captured by a simple, interpretable model. Logistic Regression's interpretability is also a practical advantage in a business context, where stakeholders benefit from understanding *why* a customer was flagged as high-risk.

## Feature Importance

The model's coefficients revealed the strongest predictors: `MonthlyCharges` and `tenure` (both negative), `InternetService_Fiber optic` (positive, a non-obvious churn driver), and `Contract_Two year`/`Contract_One year` (both negative, confirming EDA). Notably, `MonthlyCharges`' negative coefficient reflects its effect *after controlling for* other features like `InternetService`, which can differ from raw EDA correlations that don't account for interactions between features.

## Application

The Streamlit application allows a user to input a customer's demographic, account, service, and billing details across four organized tabs, then generates:
- A churn probability percentage
- A risk classification (Low / Moderate / High)
- A feature attribution chart showing which inputs most influenced that specific prediction
- A downloadable CSV report of the prediction

## Installation & Running Locally

```bash
git clone https://github.com/Apoorva-mishra01/telecom-churn-prediction.git
cd telecom-churn-prediction
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
cd app
streamlit run app.py
```

## Project Structure
telecom-churn-prediction/
├── data/
│ ├── raw/ # Original dataset
│ └── processed/ # Saved train/test splits
├── notebooks/ # EDA, preprocessing, modeling notebooks
├── models/ # Saved model and scaler (.pkl)
├── app/ # Streamlit application
├── requirements.txt
└── README.md


## Limitations

- Recall was moderate across all models (0.50–0.56), meaning even the best model misses close to half of actual churners. This could be improved with class-weighting or resampling techniques (e.g., SMOTE) in future work.
- The application does not validate logical dependencies between related fields (e.g., a user can select "No" for Phone Service but "Yes" for Multiple Lines, a combination that shouldn't be possible).
- Numerically inconsistent inputs (e.g., a `TotalCharges` value far outside what `tenure × MonthlyCharges` would suggest) can produce extreme predictions that may not be reliable, since such combinations were unlikely to appear in training data.

## Future Improvements

- Address class imbalance more directly through resampling or class-weighting to improve recall.
- Add input validation for logically dependent fields in the app.
- Experiment with additional models (e.g., XGBoost, LightGBM) and more extensive hyperparameter search.
- Explore SHAP values for more rigorous per-prediction interpretability.

## Author

**Apoorva Mishra**
B.Tech CSE 
[GitHub](https://github.com/Apoorva-mishra01)