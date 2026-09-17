import pandas as pd
from scipy.stats import spearmanr

def spearman_analysis(df: pd.DataFrame, input_cols: list[str], target_col: str) -> pd.DataFrame:
    rows = []
    for col in input_cols:
        rho, p_value = spearmanr(df[col], df[target_col])
        if rho > 0:
            direction = "Positive / Increasing"
        elif rho < 0:
            direction = "Negative / Decreasing"
        else:
            direction = "No clear monotonicity"
        rows.append({
            "Variable": col,
            "Spearman_rho": round(float(rho), 4),
            "p_value": round(float(p_value), 6),
            "Direction": direction
        })
    return pd.DataFrame(rows)

def split_by_direction(correlation_df: pd.DataFrame):
    increasing = correlation_df[correlation_df["Spearman_rho"] > 0]["Variable"].tolist()
    decreasing = correlation_df[correlation_df["Spearman_rho"] < 0]["Variable"].tolist()
    return increasing, decreasing
