import streamlit as st
from components.modeling import render_clustering, render_prediction

st.set_page_config(page_title="ML Insights", page_icon="🤖", layout="wide")
df = st.session_state.get("df")
num = st.session_state.get("numeric_cols", [])
cat = st.session_state.get("categorical_cols", [])

if df is None:
    st.error("No dataset loaded.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    render_clustering(df, num)
with col2:
    render_prediction(df, num, cat)
