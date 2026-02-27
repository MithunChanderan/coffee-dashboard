import streamlit as st

from components.filters import apply_filters
from components.kpi_cards import render_kpis
from components.charts import histogram, bar_chart, correlation_heatmap
from components.ui import hero, lottie_block, load_theme


st.set_page_config(page_title="Executive Overview", page_icon=":bar_chart:", layout="wide")
load_theme()

df = st.session_state.get("df")
numeric_cols = st.session_state.get("numeric_cols", [])
categorical_cols = st.session_state.get("categorical_cols", [])
datetime_cols = st.session_state.get("datetime_cols", [])

if df is None or df.empty:
    st.stop()

hero(
    "Executive Overview",
    "Filters, KPIs, and smart visuals refresh automatically with your dataset.",
)
lottie_block("https://assets9.lottiefiles.com/packages/lf20_svlqmi3v.json", height=120)

filtered_df = apply_filters(df, categorical_cols, datetime_cols)

st.markdown("### KPIs")
render_kpis(filtered_df, numeric_cols)

st.markdown("### Visuals")
col1, col2 = st.columns(2)
with col1:
    histogram(filtered_df, numeric_cols)
with col2:
    bar_chart(filtered_df, categorical_cols)

correlation_heatmap(filtered_df, numeric_cols)

with st.expander("Preview (filtered)"):
    st.dataframe(filtered_df.head(50), use_container_width=True)
