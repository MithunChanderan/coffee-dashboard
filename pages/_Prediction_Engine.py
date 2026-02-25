import streamlit as st
import pickle

st.title("Revenue Prediction Engine")

model = pickle.load(open("models/revenue_model.pkl","rb"))

hour = st.slider("Hour",0,23)
qty = st.number_input("Quantity",1,20)
price = st.number_input("Unit Price",1.0,20.0)

if st.button("Predict Revenue"):
    prediction = model.predict([[hour,qty,price]])
    st.success(f"Predicted Revenue: ${prediction[0]:.2f}")
