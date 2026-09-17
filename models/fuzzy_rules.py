PRICE_LOW = 80.0
PRICE_MEDIUM = 130.0
PRICE_HIGH = 180.0

# Risk-related variables. Higher D/E and Beta reduce predicted stock price.
MFIS_DOWN_RULES = [
    ("Low", "Low", PRICE_HIGH),
    ("Medium", "Medium", PRICE_MEDIUM),
    ("High", "High", PRICE_LOW),
]

# Solvency-related variable. Higher Interest Coverage increases predicted stock price.
MFIS_UP_RULES = [
    ("Low", PRICE_LOW),
    ("Medium", PRICE_MEDIUM),
    ("High", PRICE_HIGH),
]
