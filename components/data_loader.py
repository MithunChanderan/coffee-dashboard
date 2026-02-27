from pathlib import Path

import pandas as pd
import streamlit as st


DEMO_PATH = Path(__file__).resolve().parents[1] / "data" / "coffee_sales.csv"


@st.cache_data(show_spinner=False)
def _read_csv(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    return df


def load_dataset(uploaded_file):
    """Return dataframe, source note, and status. UI messaging is handled by caller."""
    try:
        if uploaded_file is not None:
            df = _read_csv(uploaded_file)
            return df, f"Uploaded file: {uploaded_file.name}", "uploaded"
        if DEMO_PATH.exists():
            df = _read_csv(DEMO_PATH)
            return df, "Demo dataset", "demo"
        return pd.DataFrame(), "No dataset available", "missing"
    except Exception as e:
        return pd.DataFrame(), f"Load error: {e}", "error"


def detect_column_types(df: pd.DataFrame):
    """Infer numeric, categorical, and datetime columns (attempt parsing objects to datetime)."""
    if df is None or df.empty:
        return df, [], [], []

    df = df.copy()
    datetime_cols = []

    for col in df.columns:
        series = df[col]
        if pd.api.types.is_datetime64_any_dtype(series):
            datetime_cols.append(col)
            continue
        if series.dtype == object:
            parsed = pd.to_datetime(series, errors="coerce", utc=False)
            if parsed.notna().mean() >= 0.6:
                df[col] = parsed
                datetime_cols.append(col)

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols + datetime_cols]

    return df, numeric_cols, categorical_cols, datetime_cols
