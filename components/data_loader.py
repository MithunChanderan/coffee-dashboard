from pathlib import Path
import pandas as pd
import streamlit as st

DEMO_PATH = Path(__file__).resolve().parents[1] / "data" / "coffee_sales.csv"

@st.cache_data(show_spinner=False)
def _read_csv(file_obj):
    return pd.read_csv(file_obj)

def load_uploaded_or_demo(uploaded_file):
    if uploaded_file:
        df = _read_csv(uploaded_file)
        return df, f"Uploaded file: {uploaded_file.name}"
    if DEMO_PATH.exists():
        df = _read_csv(DEMO_PATH)
        return df, "Built-in demo: data/coffee_sales.csv"
    sample = pd.DataFrame({"feature1":[1,2,3], "feature2":["A","B","A"]})
    return sample, "Fallback sample (demo file missing)"

def infer_column_types(df: pd.DataFrame):
    df = df.copy()
    datetime_cols = []
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            datetime_cols.append(col)
        elif df[col].dtype == "object":
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() > 0.6:
                df[col] = parsed
                datetime_cols.append(col)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols + datetime_cols]
    return df, numeric_cols, categorical_cols, datetime_cols
