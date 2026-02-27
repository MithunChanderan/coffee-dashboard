import pandas as pd
import plotly.express as px
import streamlit as st

from components.filters import apply_filters
from components.utils import run_user_code
from components.ui import lottie_block, hero, load_theme
from components.kpi_cards import render_kpis


st.set_page_config(page_title="Interactive Lab", page_icon=":test_tube:", layout="wide")
load_theme()

df = st.session_state.get("df")
numeric_cols = st.session_state.get("numeric_cols", [])
categorical_cols = st.session_state.get("categorical_cols", [])
datetime_cols = st.session_state.get("datetime_cols", [])

if df is None or df.empty:
    st.error("No dataset loaded. Go to Home and upload or use the demo.")
    st.stop()

hero("Interactive Lab", "Experiment with filters, instant charts, and inline Python.")
lottie_block("https://assets4.lottiefiles.com/private_files/lf30_cgfdhxgx.json", height=120)

filtered_df = apply_filters(df, categorical_cols, datetime_cols)

st.markdown("### Quick Metrics")
render_kpis(filtered_df, numeric_cols)

tab1, tab2 = st.tabs(["Live Chart Builder", "Python Sandbox"])

with tab1:
    st.markdown("Build visuals on the fly.")
    chart_type = st.selectbox("Chart type", ["Histogram", "Bar", "Scatter", "Box"])

    if chart_type == "Histogram":
        if numeric_cols:
            x_col = st.selectbox("Numeric column", numeric_cols, key="lab_hist_col")
            bins = st.slider("Bins", 5, 80, 30, key="lab_hist_bins")
            fig = px.histogram(filtered_df, x=x_col, nbins=bins, color_discrete_sequence=["#d6ad60"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available.")

    elif chart_type == "Bar":
        if categorical_cols:
            x_col = st.selectbox("Categorical column", categorical_cols, key="lab_bar_col")
            y_col = st.selectbox("Optional numeric (aggregates mean)", [None] + numeric_cols, key="lab_bar_y")
            if y_col:
                data = filtered_df.groupby(x_col)[y_col].mean().reset_index()
                fig = px.bar(data, x=x_col, y=y_col, color_discrete_sequence=["#8c593b"])
            else:
                counts = filtered_df[x_col].value_counts().nlargest(20).reset_index()
                fig = px.bar(counts, x="index", y=x_col, color_discrete_sequence=["#8c593b"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categorical columns available.")

    elif chart_type == "Scatter":
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("X", numeric_cols, key="lab_scatter_x")
            y_col = st.selectbox("Y", [c for c in numeric_cols if c != x_col], key="lab_scatter_y")
            color_col = st.selectbox("Color (optional)", [None] + categorical_cols, key="lab_scatter_color")
            fig = px.scatter(
                filtered_df,
                x=x_col,
                y=y_col,
                color=color_col,
                color_discrete_sequence=px.colors.sequential.Copper,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least two numeric columns.")

    elif chart_type == "Box":
        if numeric_cols and categorical_cols:
            y_col = st.selectbox("Numeric", numeric_cols, key="lab_box_y")
            x_col = st.selectbox("Group by", categorical_cols, key="lab_box_x")
            fig = px.box(filtered_df, x=x_col, y=y_col, color_discrete_sequence=["#d6ad60"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least one numeric and one categorical column.")

with tab2:
    st.markdown(
        """
        Run Python against the filtered dataframe `df` (provided below).
        Use `result` / `output` / `out` to show a table; Plotly or Matplotlib figures will render automatically.
        """
    )
    default_code = """# df is a pandas DataFrame already filtered by sidebar selections.\nsummary = df.describe(include='all')\nprint(summary)\n"""
    code = st.text_area("Python code", value=default_code, height=320)
    if st.button("Run code", type="primary"):
        with st.spinner("Executing..."):
            try:
                result = run_user_code(code, filtered_df)
            except Exception as e:
                st.error(f"Execution failed: {e}")
            else:
                if result["stdout"].strip():
                    st.subheader("Logs")
                    st.code(result["stdout"])
                if result["stderr"].strip():
                    st.subheader("Errors")
                    st.code(result["stderr"], language="bash")
                if result.get("result") is not None:
                    st.subheader("Result")
                    if isinstance(result["result"], pd.DataFrame):
                        st.dataframe(result["result"], use_container_width=True)
                    else:
                        st.write(result["result"])
                for fig in result["plotly_figs"]:
                    st.plotly_chart(fig, use_container_width=True)
                for fig in result["figures"]:
                    st.pyplot(fig, clear_figure=True)

with st.expander("Data sample (filtered)"):
    st.dataframe(filtered_df.head(50), use_container_width=True)
