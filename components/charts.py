import streamlit as st
import plotly.express as px
import pandas as pd


def histogram(df: pd.DataFrame, numeric_cols):
    if not numeric_cols:
        st.info("No numeric columns for histogram.")
        return
    col = st.selectbox("Numeric column", numeric_cols, key="hist_col")
    bins = st.slider("Bins", 5, 80, 30, key="hist_bins")
    fig = px.histogram(df, x=col, nbins=bins, color_discrete_sequence=["#d6ad60"])
    fig.update_layout(title=f"Distribution of {col}")
    st.plotly_chart(fig, use_container_width=True)


def bar_chart(df: pd.DataFrame, categorical_cols):
    if not categorical_cols:
        st.info("No categorical columns for bar chart.")
        return
    col = st.selectbox("Categorical column", categorical_cols, key="cat_col")
    # Guard against very high cardinality to avoid overplotting or Plotly issues
    if df[col].nunique(dropna=True) > 50:
        st.info("Selected column has more than 50 unique values. Choose another column or reduce categories.")
        return
    top = st.slider("Top categories", 3, 25, 10, key="cat_top")
    counts = df[col].value_counts().nlargest(top).reset_index()
    counts.columns = ["category", "count"]
    if counts.empty:
        st.info("No data available for the selected column.")
        return
    fig = px.bar(counts, x="category", y="count", color_discrete_sequence=["#8c593b"])
    fig.update_layout(xaxis_title=col, yaxis_title="Count", title=f"{col} frequency")
    st.plotly_chart(fig, use_container_width=True)


def correlation_heatmap(df: pd.DataFrame, numeric_cols):
    if len(numeric_cols) < 2:
        st.info("Need at least two numeric columns for correlation heatmap.")
        return
    corr = df[numeric_cols].corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="inferno",
        title="Correlation heatmap",
    )
    st.plotly_chart(fig, use_container_width=True)
