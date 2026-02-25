import plotly.express as px
import streamlit as st

def revenue_trend(df):
    trend = df.groupby("Month")["Revenue"].sum().reset_index()
    fig = px.line(trend, x="Month", y="Revenue", markers=True,
                  title="Revenue Trend")
    st.plotly_chart(fig, use_container_width=True)

def heatmap_sales(df):
    heat = df.groupby(["Weekday","Hour"])["Revenue"].sum().reset_index()
    fig = px.density_heatmap(
        heat,
        x="Hour",
        y="Weekday",
        z="Revenue",
        title="Sales Heatmap"
    )
    st.plotly_chart(fig, use_container_width=True)

def category_breakdown(df):
    cat = df.groupby("product_category")["Revenue"].sum().reset_index()
    fig = px.bar(cat, x="product_category", y="Revenue",
                 title="Revenue by Category")
    st.plotly_chart(fig, use_container_width=True)
