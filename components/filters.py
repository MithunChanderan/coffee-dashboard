import streamlit as st
import pandas as pd


def apply_filters(df: pd.DataFrame, categorical_cols, datetime_cols):
    """Auto-build sidebar filters based on detected column types."""
    if df is None or df.empty:
        return df

    filtered = df.copy()
    st.sidebar.header("Filters")

    # Datetime range on first datetime column (if any)
    if datetime_cols:
        dt_col = datetime_cols[0]
        min_date = pd.to_datetime(filtered[dt_col].min())
        max_date = pd.to_datetime(filtered[dt_col].max())
        start, end = st.sidebar.date_input(
            "Date range",
            value=(min_date.date(), max_date.date()),
            min_value=min_date.date(),
            max_value=max_date.date(),
        )
        if start and end:
            mask = (pd.to_datetime(filtered[dt_col]).dt.date >= start) & (
                pd.to_datetime(filtered[dt_col]).dt.date <= end
            )
            filtered = filtered[mask]

    # Up to 4 categorical filters to avoid sidebar overload
    for col in categorical_cols[:4]:
        unique_vals = filtered[col].dropna().unique()
        default = unique_vals
        selection = st.sidebar.multiselect(
            f"{col}",
            options=unique_vals,
            default=default,
        )
        if selection:
            filtered = filtered[filtered[col].isin(selection)]

    return filtered
