import pandas as pd
from modules.membership import fuzzify_value
from models.fuzzy_rules import MFIS_UP_RULES

def mfis_up_predict(interest_coverage: float, mf_ic: dict):
    ic_membership = fuzzify_value(interest_coverage, mf_ic)
    weighted_sum = 0.0
    total_weight = 0.0
    fired_rules = []
    for idx, (ic_label, consequent) in enumerate(MFIS_UP_RULES, start=1):
        strength = ic_membership[ic_label]
        contribution = strength * consequent
        weighted_sum += contribution
        total_weight += strength
        fired_rules.append({
            "Rule ID": f"U{idx}",
            "Rule": f"IF Interest Coverage is {ic_label} THEN Stock Price is {consequent}",
            "Interest Coverage Term": ic_label,
            "Firing Strength": round(float(strength), 4),
            "Consequent": consequent,
            "Contribution": round(float(contribution), 4),
            "Active": "Yes" if strength > 0 else "No"
        })
    output = float(weighted_sum / total_weight) if total_weight > 0 else 130.0
    return output, pd.DataFrame(fired_rules)
