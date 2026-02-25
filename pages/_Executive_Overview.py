import streamlit as st
from components.data_loader import load_data
from components.filters import apply_filters
from components.kpi_cards import show_kpis
from components.charts import revenue_trend

st.title("Executive Overview")

df = st.session_state.get("df")

if df is None:
    st.error("No dataset loaded.")
    st.stop()

filtered_df = apply_filters(df)

show_kpis(filtered_df)
revenue_trend(filtered_df)
