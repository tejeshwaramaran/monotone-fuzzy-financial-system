import numpy as np
import pandas as pd

def triangular_mf(x: float, a: float, b: float, c: float) -> float:
    x = float(x)
    if x <= a or x >= c:
        return 0.0
    if x == b:
        return 1.0
    if a < x < b:
        return (x - a) / ((b - a) + 1e-12)
    return (c - x) / ((c - b) + 1e-12)

def create_three_membership_functions(x_min: float, x_max: float) -> dict:
    span = x_max - x_min
    return {
        "Low": (x_min - 0.05 * span, x_min, x_min + 0.50 * span),
        "Medium": (x_min, x_min + 0.50 * span, x_max),
        "High": (x_min + 0.50 * span, x_max, x_max + 0.05 * span),
    }

def fuzzify_value(x: float, membership_functions: dict) -> dict:
    return {label: triangular_mf(x, *params) for label, params in membership_functions.items()}

def fuzzification_table(x: float, membership_functions: dict, variable_name: str) -> pd.DataFrame:
    memberships = fuzzify_value(x, membership_functions)
    return pd.DataFrame({
        "Variable": [variable_name] * len(memberships),
        "Linguistic Term": list(memberships.keys()),
        "Membership Degree": [round(v, 4) for v in memberships.values()]
    })

def membership_curve_data(membership_functions: dict, x_min: float, x_max: float, points: int = 200):
    xs = np.linspace(x_min, x_max, points)
    curves = {}
    for label, params in membership_functions.items():
        curves[label] = [triangular_mf(x, *params) for x in xs]
    return xs, curves
