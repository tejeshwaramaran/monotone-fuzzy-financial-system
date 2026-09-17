import pandas as pd
from modules.membership import fuzzify_value
from models.fuzzy_rules import MFIS_DOWN_RULES

def mfis_down_predict(debt_to_equity: float, beta: float, mf_de: dict, mf_beta: dict):
    de_membership = fuzzify_value(debt_to_equity, mf_de)
    beta_membership = fuzzify_value(beta, mf_beta)
    weighted_sum = 0.0
    total_weight = 0.0
    fired_rules = []
    for idx, (de_label, beta_label, consequent) in enumerate(MFIS_DOWN_RULES, start=1):
        strength = de_membership[de_label] * beta_membership[beta_label]
        contribution = strength * consequent
        weighted_sum += contribution
        total_weight += strength
        fired_rules.append({
            "Rule ID": f"D{idx}",
            "Rule": f"IF Debt-to-Equity is {de_label} AND Beta is {beta_label} THEN Stock Price is {consequent}",
            "Debt-to-Equity Term": de_label,
            "Beta Term": beta_label,
            "Firing Strength": round(float(strength), 4),
            "Consequent": consequent,
            "Contribution": round(float(contribution), 4),
            "Active": "Yes" if strength > 0 else "No"
        })
    output = float(weighted_sum / total_weight) if total_weight > 0 else 130.0
    return output, pd.DataFrame(fired_rules)
