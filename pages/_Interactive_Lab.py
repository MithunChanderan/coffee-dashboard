import streamlit as st
import pandas as pd
from components.utils import run_user_code
from components.ui import lottie_block

st.set_page_config(page_title="Interactive Lab", page_icon="🧪", layout="wide")
df = st.session_state.get("df")
if df is None:
    st.error("No dataset loaded.")
    st.stop()

st.markdown("## Interactive Lab")
lottie_block("https://assets4.lottiefiles.com/private_files/lf30_cgfdhxgx.json", height=120)

with st.expander("Column selectors", expanded=True):
    st.write(f"Rows: {len(df):,} | Columns: {df.shape[1]}")
    st.dataframe(df.head(), use_container_width=True)

default_code = """# df is ready to use
summary = df.describe(include='all')
print(summary)
"""
code = st.text_area("Python code", value=default_code, height=340)
run = st.button("Run code", type="primary")

if run:
    with st.spinner("Executing..."):
        try:
            result = run_user_code(code, df)
        except Exception as e:
            st.error(f"Execution failed: {e}")
        else:
            if result["stdout"].strip():
                st.subheader("Logs")
                st.code(result["stdout"])
            if result["stderr"].strip():
                st.subheader("Errors")
                st.code(result["stderr"], language="bash")
            if result["result"] is not None:
                st.subheader("Result")
                if isinstance(result["result"], pd.DataFrame):
                    st.dataframe(result["result"], use_container_width=True)
                else:
                    st.write(result["result"])
            for fig in result["plotly_figs"]:
                st.plotly_chart(fig, use_container_width=True)
            for fig in result["figures"]:
                st.pyplot(fig, clear_figure=True)
