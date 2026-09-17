import pandas as pd
import numpy as np
from modules.mfis_down import mfis_down_predict
from modules.mfis_up import mfis_up_predict
from modules.aggregation import aggregate_predictions

def run_mfis_prediction(de, beta, ic, mf_de, mf_beta, mf_ic):
    down, _ = mfis_down_predict(de, beta, mf_de, mf_beta)
    up, _ = mfis_up_predict(ic, mf_ic)
    return aggregate_predictions(down, up)

def verify_monotonicity(df, mf_de, mf_beta, mf_ic):
    fixed_de = float(df["Debt_to_Equity"].median())
    fixed_beta = float(df["Beta"].median())
    fixed_ic = float(df["Interest_Coverage"].median())
    rows = []
    de_values = np.linspace(df["Debt_to_Equity"].min(), df["Debt_to_Equity"].max(), 8)
    de_preds = [run_mfis_prediction(v, fixed_beta, fixed_ic, mf_de, mf_beta, mf_ic) for v in de_values]
    de_pass = all(de_preds[i] >= de_preds[i+1] - 1e-6 for i in range(len(de_preds)-1))
    rows.append({"Variable": "Debt_to_Equity", "Expected Relationship": "Input ↑, Stock Price ↓", "Result": "Pass" if de_pass else "Fail"})
    beta_values = np.linspace(df["Beta"].min(), df["Beta"].max(), 8)
    beta_preds = [run_mfis_prediction(fixed_de, v, fixed_ic, mf_de, mf_beta, mf_ic) for v in beta_values]
    beta_pass = all(beta_preds[i] >= beta_preds[i+1] - 1e-6 for i in range(len(beta_preds)-1))
    rows.append({"Variable": "Beta", "Expected Relationship": "Input ↑, Stock Price ↓", "Result": "Pass" if beta_pass else "Fail"})
    ic_values = np.linspace(df["Interest_Coverage"].min(), df["Interest_Coverage"].max(), 8)
    ic_preds = [run_mfis_prediction(fixed_de, fixed_beta, v, mf_de, mf_beta, mf_ic) for v in ic_values]
    ic_pass = all(ic_preds[i] <= ic_preds[i+1] + 1e-6 for i in range(len(ic_preds)-1))
    rows.append({"Variable": "Interest_Coverage", "Expected Relationship": "Input ↑, Stock Price ↑", "Result": "Pass" if ic_pass else "Fail"})
    details = {
        "Debt_to_Equity": pd.DataFrame({"Input Value": de_values, "Prediction": de_preds}),
        "Beta": pd.DataFrame({"Input Value": beta_values, "Prediction": beta_preds}),
        "Interest_Coverage": pd.DataFrame({"Input Value": ic_values, "Prediction": ic_preds}),
    }
    return pd.DataFrame(rows), details
