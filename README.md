# 🚗 End-to-End Insurance Risk Analytics & Predictive Modeling

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-purple)
![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📖 Executive Summary
This project was conducted for **AlphaCare Insurance Solutions (ACIS)** to analyze historical car insurance claim data. The goal was to optimize marketing strategies and pricing models by identifying "low-risk" customer segments. 

Using statistical hypothesis testing and machine learning, we developed a predictive analytics pipeline that allows ACIS to tailor premiums based on risk factors such as location, vehicle attributes, and policy details.

---

## 🎯 Business Objectives
1.  **Risk Segmentation:** Identify which geographic regions (Provinces/ZipCodes) and demographic groups present the highest risk.
2.  **Predictive Modeling:** Build a machine learning model to estimate **Total Claims (Severity)** to enable dynamic pricing.
3.  **Data Engineering:** Establish a robust, version-controlled data pipeline using **DVC** and **Git**.

---

## 📊 Key Insights & Hypothesis Testing (Task 3)

I performed rigorous A/B testing (Chi-Squared & ANOVA) to validate business assumptions.

| Hypothesis | Test Used | Outcome | Business Implication |
| :--- | :--- | :--- | :--- |
| **"Risk differs across Provinces"** | Chi-Squared | **Rejected Null** (p < 0.05) | Premiums must be adjusted regionally; some provinces have significantly higher claim frequencies. |
| **"Risk differs across ZipCodes"** | Chi-Squared | **Rejected Null** (p < 0.05) | Granular pricing at the postal code level is recommended over broad regional pricing. |
| **"Margin (Profit) differs by ZipCode"** | ANOVA | **Rejected Null** (p < 0.05) | Certain areas are significantly more profitable; marketing should target these high-margin zones. |
| **"Risk differs between Gender"** | Chi-Squared | **Failed to Reject Null** | Gender is **not** a significant driver of risk in this dataset. Pricing should remain gender-neutral. |

---

## 🤖 Predictive Modeling (Task 4)

I built and evaluated three models to predict **Claim Severity** (Total Claim Amount) for high-risk policies.

### Model Performance
| Model | R2 Score | RMSE | Observation |
| :--- | :--- | :--- | :--- |
| **Linear Regression** | *Baseline* | *High* | Failed to capture non-linear relationships. |
| **Random Forest** | *Moderate* | *Medium* | Good performance but showed signs of overfitting. |
| **XGBoost** | **Best** | **Low** | Best generalization; handled categorical data (Vehicle Type) effectively. |

### Feature Importance (SHAP Analysis)
Our XGBoost model identified the following as the top drivers of high insurance claims:
1.  **SumInsured:** The insured value of the vehicle is the #1 predictor of claim size.
2.  **VehicleType:** Heavy/Commercial vehicles carry disproportionately higher risk.
3.  **CalculatedPremium:** Existing premiums correlate with risk, but the model suggests further optimization is possible.

---

## 🛠️ Project Structure
```bash
alphacare-insurance-analytics/
├── .github/workflows/   # CI/CD Pipelines
├── data/                # Raw and processed data (tracked by DVC)
├── dvc/                 # Data Version Control configuration
├── results/figures/     # EDA plots and SHAP analysis images
├── src/                 # Source code
│   ├── loader.py        # Data ingestion
│   ├── cleaning.py      # Preprocessing pipelines
│   ├── hypothesis_testing.py  # Statistical tests (Task 3)
│   └── modeling.py      # ML Training & Evaluation (Task 4)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation