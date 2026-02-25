import io
import types
import traceback
from contextlib import redirect_stdout, redirect_stderr

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import streamlit as st


def run_user_code(code: str, df: pd.DataFrame):
    """
    Execute arbitrary Python code with a constrained toolbox and capture outputs.
    Exposes:
      - df : the (filtered) dataframe from the app
      - pd, np, px, plt : common analytics/visualization packages
    Returns stdout, stderr, matplotlib figures, and Plotly figures.
    """
    stdout, stderr = io.StringIO(), io.StringIO()
    figures = []
    plotly_figs = []

    sandbox_globals = {
        "df": df,
        "pd": pd,
        "np": np,
        "px": px,
        "plt": plt,
        "st": st,
    }
    local_env = {}

    with redirect_stdout(stdout), redirect_stderr(stderr):
        exec(code, sandbox_globals, local_env)

    # Collect matplotlib figures generated during execution
    for num in plt.get_fignums():
        figures.append(plt.figure(num))
    plt.close("all")

    # Collect Plotly figures from locals
    for val in local_env.values():
        if isinstance(val, go.Figure):
            plotly_figs.append(val)

    # Detect a primary result (if user sets `result` or `output`)
    main_result = None
    for key in ("result", "output", "out"):
        if key in local_env:
            main_result = local_env[key]
            break

    return {
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "figures": figures,
        "plotly_figs": plotly_figs,
        "locals": local_env,
        "result": main_result,
    }
