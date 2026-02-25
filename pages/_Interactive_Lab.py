import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

from components.filters import apply_filters
from components.utils import run_user_code


st.title("Interactive Python Lab")
st.caption("Prototype analyses, transformations, and visualizations directly on the filtered dataset.")

df = st.session_state.get("df")

if df is None:
    st.error("No dataset loaded.")
    st.stop()

filtered_df = apply_filters(df)

st.markdown(
    """
Use the editor below to run Python against the filtered dataframe `df`.
Anything you `print` will show in **Logs**. Assign a Plotly figure to any variable
or use Matplotlib and we will render it automatically. Set `result` or `output`
to a DataFrame to preview it.
"""
)

default_code = """# `df` is a pandas DataFrame already filtered by the sidebar controls.
# Common imports are available: pd, np, px, plt

summary = df.groupby(["store_location", "Weekday"])["Revenue"].sum().reset_index()
fig = px.bar(summary, x="store_location", y="Revenue", color="Weekday",
             title="Revenue by store and weekday")

# Show a computed table
result = summary.sort_values("Revenue", ascending=False).head(10)

# Anything you print will appear in the Logs panel
print("Rows in filtered df:", len(df))
"""

code = st.text_area(
    "Python code",
    value=default_code,
    height=360,
    help="df, pd, np, px, plt, st are available. Use result/output/out to display a DataFrame.",
)

run = st.button("Run code")

if run:
    with st.spinner("Executing code..."):
        try:
            exec_result = run_user_code(code, filtered_df)
        except Exception as e:
            st.error(f"Execution failed: {e}")
        else:
            stdout, stderr = exec_result["stdout"], exec_result["stderr"]

            if stdout.strip():
                st.subheader("Logs")
                st.code(stdout, language="bash")

            if stderr.strip():
                st.subheader("Errors")
                st.code(stderr, language="bash")

            if exec_result["result"] is not None:
                st.subheader("Result table")
                if isinstance(exec_result["result"], pd.DataFrame):
                    st.dataframe(exec_result["result"], use_container_width=True)
                else:
                    st.write(exec_result["result"])

            if exec_result["plotly_figs"]:
                st.subheader("Plotly figures")
                for fig in exec_result["plotly_figs"]:
                    st.plotly_chart(fig, use_container_width=True)

            if exec_result["figures"]:
                st.subheader("Matplotlib figures")
                for fig in exec_result["figures"]:
                    st.pyplot(fig, clear_figure=True)

            if (
                not stdout.strip()
                and not stderr.strip()
                and not exec_result["plotly_figs"]
                and not exec_result["figures"]
                and exec_result["result"] is None
            ):
                st.info("No output generated. Print something or assign a figure/result.")

with st.expander("Data sample"):
    st.dataframe(filtered_df.head(), use_container_width=True)
