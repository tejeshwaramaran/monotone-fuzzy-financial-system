import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def conventional_tsk_baseline(df, input_cols, target_col):
    X = df[input_cols].values
    y = df[target_col].values
    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)
    rmse_value = float(np.sqrt(mean_squared_error(y, preds)))
    return model, preds, rmse_value
