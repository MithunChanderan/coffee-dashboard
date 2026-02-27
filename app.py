import pandas as pd
import streamlit as st
from pathlib import Path

from components.data_loader import load_uploaded_or_demo, infer_column_types
from components.kpi_cards import render_kpis
from components.viz import render_overview_charts
from components.modeling import render_clustering, render_prediction
from components.ui import load_theme, hero_section, lottie_block, typed_badges

st.set_page_config(
    page_title="Coffee Analytics Pro",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_theme()

uploaded_file = st.sidebar.file_uploader("Upload CSV dataset", type=["csv"])
df, data_note = load_uploaded_or_demo(uploaded_file)
df, numeric_cols, categorical_cols, datetime_cols = infer_column_types(df)

st.session_state["df"] = df
st.session_state["numeric_cols"] = numeric_cols
st.session_state["categorical_cols"] = categorical_cols
st.session_state["datetime_cols"] = datetime_cols

with st.sidebar:
    st.markdown(f"**Dataset source:** {data_note}")
    typed_badges(numeric_cols, categorical_cols, datetime_cols)

hero_section()

with st.container():
    render_kpis(df, numeric_cols)
    render_overview_charts(df, numeric_cols, categorical_cols)

st.markdown("### Interactive Lab")
lottie_block("https://assets6.lottiefiles.com/packages/lf20_bhw1ul4g.json", height=120)
st.page_link("pages/2_Interactive_Lab.py", label="Open Interactive Lab →", icon="🧪")

st.markdown("### ML Playground")
col1, col2 = st.columns(2)
with col1:
    render_clustering(df, numeric_cols)
with col2:
    render_prediction(df, numeric_cols, categorical_cols)

st.markdown("### Dataset Preview")
st.dataframe(df.head(50), use_container_width=True)
