import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates().copy()
    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(df[col].median())
    return df

def normalize_columns(df: pd.DataFrame, columns: list[str]):
    scaler = MinMaxScaler()
    df_norm = df.copy()
    df_norm[columns] = scaler.fit_transform(df_norm[columns])
    return df_norm, scaler
