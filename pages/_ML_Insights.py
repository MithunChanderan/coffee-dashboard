import streamlit as st
import pickle
import plotly.express as px
from components.data_loader import load_data
from components.filters import apply_filters

st.title("ML Insights")

df = st.session_state.get("df")

if df is None:
    st.error("No dataset loaded.")
    st.stop()

filtered_df = apply_filters(df)

cluster_model = pickle.load(open("models/cluster_model.pkl","rb"))
classifier = pickle.load(open("models/classifier.pkl","rb"))

features = filtered_df[["transaction_qty","unit_price","Hour","Revenue"]]
filtered_df["Cluster"] = cluster_model.predict(features)

fig = px.scatter(
    filtered_df,
    x="Hour",
    y="Revenue",
    color="Cluster",
    title="Customer Purchase Clusters"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Classification Model Accuracy")
st.write("Model trained to classify High vs Low Sales transactions.")
