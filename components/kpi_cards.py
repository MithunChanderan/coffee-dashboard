import streamlit as st

def show_kpis(df):
    total_revenue = df["Revenue"].sum()
    total_transactions = df.shape[0]
    avg_order = df["Revenue"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Transactions", total_transactions)
    col3.metric("Avg Order Value", f"${avg_order:.2f}")
