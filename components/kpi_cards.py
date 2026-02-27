import pandas as pd
import streamlit as st

def render_kpis(df: pd.DataFrame, numeric_cols):
    total_rows = len(df)
    total_cols = df.shape[1]
    missing = int(df.isna().sum().sum())
    avg_numeric = df[numeric_cols].mean().mean() if numeric_cols else 0

    st.markdown('<div class="card-grid">', unsafe_allow_html=True)
    for label, value, suffix in [
        ("Rows", f"{total_rows:,}", ""),
        ("Columns", total_cols, ""),
        ("Missing values", f"{missing:,}", ""),
        ("Avg numeric value", f"{avg_numeric:,.2f}", ""),
    ]:
        st.markdown(
            f"""
            <div class="glass-card kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}{suffix}</div>
                <div class="pulse"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
