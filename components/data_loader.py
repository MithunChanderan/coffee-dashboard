import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/coffee_sales.csv")

    if df.empty:
        raise ValueError("Dataset is empty. Please load valid data.")

    df.columns = df.columns.str.strip()
    return df
