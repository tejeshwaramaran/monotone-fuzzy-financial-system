# Data-Driven Monotone Fuzzy System Using Financial Data

A Python and Streamlit prototype implementing a monotone
Takagi-Sugeno-Kang (TSK) fuzzy inference system for financial
prediction.

## Overview

This project explores the use of monotonic constraints in an
interpretable fuzzy inference system.

The model evaluates relationships between financial indicators
and stock price using Spearman correlation analysis. Variables
with increasing and decreasing relationships are processed by
separate monotone fuzzy models before being aggregated into a
final prediction.

A synthetic financial dataset is used to provide a controlled
environment for prototype development and monotonicity testing.

## Financial Indicators

The system uses:

- Debt-to-Equity Ratio
- Beta
- Interest Coverage

## Key Features

- Data preprocessing
- Spearman correlation analysis
- Triangular membership functions
- Fuzzification
- TSK fuzzy-rule inference
- Separate increasing and decreasing MFIS components
- Aggregated stock-price prediction
- RMSE evaluation
- Conventional TSK baseline comparison
- Explicit monotonicity verification
- Actual vs. predicted visualization
- Interactive Streamlit dashboard
- System test cases

## Technologies

- Python
- Streamlit
- Pandas
- NumPy
- SciPy
- Scikit-learn
- Matplotlib

## System Architecture

Financial Data
→ Preprocessing
→ Monotonicity Analysis
→ Increasing / Decreasing Variable Separation
→ MFIS Up / MFIS Down
→ Aggregation
→ Final Prediction

## Model Logic

### Decreasing MFIS

Debt-to-Equity and Beta are treated as negatively related
financial indicators.

Higher values result in lower fuzzy consequents.

### Increasing MFIS

Interest Coverage is treated as positively related.

Higher Interest Coverage results in higher fuzzy consequents.

## Evaluation

The proposed model is evaluated using:

- Root Mean Squared Error (RMSE)
- Monotonicity verification
- Comparison against a conventional TSK baseline
- Actual-versus-predicted visualization

## Running the Project

Clone the repository:

```bash
git clone https://github.com/tejeshwaramaran/monotone-fuzzy-financial-system.git