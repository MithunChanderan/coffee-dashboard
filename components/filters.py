import streamlit as st

def apply_filters(df):
    st.sidebar.header("Filters")

    store = st.sidebar.multiselect(
        "Store Location",
        df["store_location"].unique(),
        default=df["store_location"].unique()
    )

    category = st.sidebar.multiselect(
        "Product Category",
        df["product_category"].unique(),
        default=df["product_category"].unique()
    )

    month = st.sidebar.multiselect(
        "Month",
        df["Month"].unique(),
        default=df["Month"].unique()
    )

    filtered_df = df[
        (df["store_location"].isin(store)) &
        (df["product_category"].isin(category)) &
        (df["Month"].isin(month))
    ]

    return filtered_df
