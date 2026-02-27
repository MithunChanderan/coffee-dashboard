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
    """Return dataframe and source note. Falls back to bundled demo when no upload."""
    try:
        if uploaded_file is not None:
            df = _read_csv(uploaded_file)
            return df, f"Uploaded file: {uploaded_file.name}"
        if DEMO_PATH.exists():
            df = _read_csv(DEMO_PATH)
            st.info("Demo dataset loaded. Upload your own CSV to explore.")
            return df, "Demo dataset"
        st.warning("No dataset available. Please upload a CSV.")
        return pd.DataFrame(), "Missing dataset"
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return pd.DataFrame(), "Load error"


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
