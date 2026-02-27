import pandas as pd
import streamlit as st


def render_kpis(df: pd.DataFrame, numeric_cols):
    """Dynamic KPI deck with graceful fallbacks."""
    total_rows = len(df)
    total_cols = df.shape[1]
    missing = int(df.isna().sum().sum())
    numeric_avg = df[numeric_cols].mean().mean() if numeric_cols else 0

    kpis = [
        ("Rows", f"{total_rows:,}", ""),
        ("Columns", total_cols, ""),
        ("Missing values", f"{missing:,}", ""),
        ("Avg numeric value", f"{numeric_avg:,.2f}", ""),
    ]

    st.markdown('<div class="card-grid">', unsafe_allow_html=True)
    for title, value, suffix in kpis:
        st.markdown(
            f"""
            <div class="glass-card kpi-card">
                <div class="kpi-label">{title}</div>
                <div class="kpi-value">{value}{suffix}</div>
                <div class="pulse"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
