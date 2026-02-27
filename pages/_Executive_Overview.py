import streamlit as st
from components.kpi_cards import render_kpis
from components.viz import render_overview_charts
from components.ui import lottie_block

st.set_page_config(page_title="Executive Overview", page_icon="📊", layout="wide")
df = st.session_state.get("df")
num = st.session_state.get("numeric_cols", [])
cat = st.session_state.get("categorical_cols", [])

if df is None:
    st.error("No dataset loaded. Go back and upload or use the demo.")
    st.stop()

lottie_block("https://assets9.lottiefiles.com/packages/lf20_svlqmi3v.json", height=140)
render_kpis(df, num)
render_overview_charts(df, num, cat)
