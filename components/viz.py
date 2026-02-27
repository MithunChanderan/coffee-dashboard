import streamlit as st
import plotly.express as px
import pandas as pd

def render_overview_charts(df, numeric_cols, categorical_cols):
    st.markdown("### Automated Explorations")
    col1, col2 = st.columns(2)

    with col1:
        if numeric_cols:
            num_col = st.selectbox("Histogram column", numeric_cols, key="hist_col")
            fig = px.histogram(df, x=num_col, nbins=30, color_discrete_sequence=["#d6ad60"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns found for histogram.")

    with col2:
        if categorical_cols:
            cat_col = st.selectbox("Categorical bar", categorical_cols, key="cat_col")
            top_cats = df[cat_col].value_counts().nlargest(12).reset_index()
            fig = px.bar(top_cats, x="index", y=cat_col, color_discrete_sequence=["#8c593b"])
            fig.update_layout(xaxis_title=cat_col, yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categorical columns found for bar chart.")

    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="copper", title="Correlation heatmap")
        st.plotly_chart(fig, use_container_width=True)
