import pandas as pd
import streamlit as st
from components.data_loader import load_data
from components.kpi_cards import show_kpis
from components.charts import revenue_trend, heatmap_sales, category_breakdown


st.set_page_config(
    page_title="Coffee Analytics Pro",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# ---------- Sidebar ----------
st.sidebar.title("☕ Coffee Analytics Pro")
st.sidebar.markdown(
    "Enterprise-grade analytics, ML insights, and a built-in Python lab."
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset (CSV)",
    type=["csv"],
)

# ---------- Data Handling ----------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Dataset uploaded successfully.")
else:
    try:
        df = load_data()
        if df.empty:
            st.sidebar.warning("Local dataset is empty.")
            st.stop()
    except Exception:
        st.sidebar.warning("No dataset found. Please upload one.")
        st.stop()

# Store globally for pages
st.session_state["df"] = df

# ---------- Main Page ----------
st.sidebar.success("Select a page from the sidebar.")

st.markdown(
    """
<div class="hero">
    <div class="pill">Live data • ML ready • Interactive IDE</div>
    <h1>Coffee Sales Control Center</h1>
    <p>Performance overview, predictive models, and a sandbox to prototype analyses without leaving the dashboard.</p>
    <div class="cta-row">
        <span class="cta">Explore → Executive Overview</span>
        <span class="cta ghost">Build → Interactive Lab</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("#### Executive Snapshot")
show_kpis(df)

tab1, tab2, tab3 = st.tabs(
    ["Revenue trend", "Sales heatmap", "Category mix"]
)

with tab1:
    revenue_trend(df)
with tab2:
    heatmap_sales(df)
with tab3:
    category_breakdown(df)

st.markdown("#### Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

st.markdown(
    f"Rows: **{df.shape[0]:,}** • Columns: **{df.shape[1]}** • Time range: "
    f"{df['transaction_date'].min()} → {df['transaction_date'].max()}"
)
