import streamlit as st

from components.modeling import render_clustering, render_prediction
from components.ui import hero, lottie_block, load_theme


st.set_page_config(page_title="ML Insights", page_icon=":robot_face:", layout="wide")
load_theme()

df = st.session_state.get("df")
numeric_cols = st.session_state.get("numeric_cols", [])
categorical_cols = st.session_state.get("categorical_cols", [])

if df is None or df.empty:
    st.error("No dataset loaded. Go to Home and upload or use the demo.")
    st.stop()

hero("ML Insights", "Cluster and predict automatically based on your selected columns.")
lottie_block("https://assets7.lottiefiles.com/packages/lf20_zh6xtlj9.json", height=120)

col1, col2 = st.columns(2)
with col1:
    render_clustering(df, numeric_cols)
with col2:
    render_prediction(df, numeric_cols, categorical_cols)
