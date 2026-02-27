import streamlit as st

from components.data_loader import load_dataset, detect_column_types
from components.kpi_cards import render_kpis
from components.charts import histogram, bar_chart, correlation_heatmap
from components.modeling import render_clustering, render_prediction
from components.ui import load_theme, hero


st.set_page_config(
    page_title="Coffee Analytics Pro",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_theme()

# ---------- Sidebar: dataset ----------
uploaded_file = st.sidebar.file_uploader("Upload Dataset (CSV)", type=["csv"])
df, source_note = load_dataset(uploaded_file)
df, numeric_cols, categorical_cols, datetime_cols = detect_column_types(df)

st.session_state["df"] = df
st.session_state["numeric_cols"] = numeric_cols
st.session_state["categorical_cols"] = categorical_cols
st.session_state["datetime_cols"] = datetime_cols

st.sidebar.success(source_note)
st.sidebar.markdown(
    f"**Detected:** {len(numeric_cols)} numeric | {len(categorical_cols)} categorical | {len(datetime_cols)} datetime"
)

if df is None or df.empty:
    st.stop()

# ---------- Main content ----------
hero(
    "Coffee Sales Command Center",
    "Dynamic KPIs, automated visuals, clustering, and predictions for any CSV - upload or use the demo.",
)

st.markdown("#### Executive Snapshot")
render_kpis(df, numeric_cols)

st.markdown("### Automated Visuals")
col1, col2 = st.columns(2)
with col1:
    histogram(df, numeric_cols)
with col2:
    bar_chart(df, categorical_cols)

correlation_heatmap(df, numeric_cols)

st.markdown("### ML Quick Actions")
clust_col, pred_col = st.columns(2)
with clust_col:
    render_clustering(df, numeric_cols)
with pred_col:
    render_prediction(df, numeric_cols, categorical_cols)

st.markdown("### Dataset Preview")
st.dataframe(df.head(50), use_container_width=True)

st.caption(
    f"Rows: {df.shape[0]:,} | Columns: {df.shape[1]} | Source: {source_note}"
)
