import streamlit as st
from components.data_loader import load_data
from components.filters import apply_filters
from components.charts import heatmap_sales, category_breakdown

st.title("Sales Analytics")

df = st.session_state.get("df")

if df is None:
    st.error("No dataset loaded.")
    st.stop()

filtered_df = apply_filters(df)

heatmap_sales(filtered_df)
category_breakdown(filtered_df)
