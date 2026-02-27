import streamlit as st

from components.modeling import render_prediction
from components.ui import hero, load_theme


st.set_page_config(page_title="Prediction Engine", page_icon=":chart_with_upwards_trend:", layout="wide")
load_theme()

df = st.session_state.get("df")
numeric_cols = st.session_state.get("numeric_cols", [])
categorical_cols = st.session_state.get("categorical_cols", [])

if df is None or df.empty:
    st.stop()

hero("Prediction Engine", "Auto-selects regression or classification based on your target.")
render_prediction(df, numeric_cols, categorical_cols)
