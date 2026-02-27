import streamlit as st

from components.charts import histogram, bar_chart, correlation_heatmap
from components.ui import hero, load_theme


st.set_page_config(page_title="Sales Analytics", page_icon=":bar_chart:", layout="wide")
load_theme()

df = st.session_state.get("df")
numeric_cols = st.session_state.get("numeric_cols", [])
categorical_cols = st.session_state.get("categorical_cols", [])

if df is None or df.empty:
    st.error("No dataset loaded. Go to Home and upload or use the demo.")
    st.stop()

hero("Analytics Lab", "Explore distributions, category mix, and correlations.")

col1, col2 = st.columns(2)
with col1:
    histogram(df, numeric_cols)
with col2:
    bar_chart(df, categorical_cols)

correlation_heatmap(df, numeric_cols)
