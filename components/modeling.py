import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    accuracy_score,
    f1_score,
)
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


def render_clustering(df: pd.DataFrame, numeric_cols):
    st.subheader("Clustering (KMeans + Elbow)")
    if len(numeric_cols) < 2:
        st.info("Need at least two numeric columns for clustering.")
        return

    feature_cols = st.multiselect(
        "Select numeric features",
        numeric_cols,
        default=numeric_cols[: min(3, len(numeric_cols))],
    )
    if len(feature_cols) < 2:
        st.warning("Select two or more numeric features.")
        return

    X = df[feature_cols].dropna()
    if X.empty:
        st.warning("No rows available after dropping NA for selected features.")
        return

    if len(X) < 2:
        st.warning("Need at least two rows to compute clusters.")
        return

    max_k = min(8, len(X))
    k_range = range(2, max_k + 1)
    inertias = []
    with st.spinner("Computing elbow curve..."):
        for k in k_range:
            model = KMeans(n_clusters=k, n_init="auto", random_state=42)
            model.fit(X)
            inertias.append(model.inertia_)

    fig = px.line(x=list(k_range), y=inertias, markers=True, labels={"x": "k", "y": "Inertia"})
    fig.update_layout(title="Elbow method")
    st.plotly_chart(fig, use_container_width=True)

    k_choice = st.slider("Choose k", min_value=2, max_value=max_k, value=min(3, max_k))
    final_model = KMeans(n_clusters=k_choice, n_init="auto", random_state=42)
    labels = final_model.fit_predict(X)
    X_plot = X.copy()
    X_plot["cluster"] = labels

    # 2D scatter using first two features
    fig2 = px.scatter(
        X_plot,
        x=feature_cols[0],
        y=feature_cols[1],
        color="cluster",
        title="Cluster scatter (first two features)",
        color_continuous_scale="copper",
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(f"Computed on {len(X_plot)} rows (rows with NA removed).")


def render_prediction(df: pd.DataFrame, numeric_cols, categorical_cols):
    st.subheader("Prediction (Auto Regression vs Classification)")
    if df is None or df.empty:
        st.info("Load a dataset to train a model.")
        return

    target = st.selectbox("Target column", df.columns, key="pred_target")
    feature_candidates = [c for c in df.columns if c != target]
    features = st.multiselect(
        "Feature columns",
        feature_candidates,
        default=feature_candidates[: min(4, len(feature_candidates))],
    )
    if not features:
        st.warning("Select at least one feature.")
        return

    y = df[target]
    X = df[features]

    num_feats = [c for c in features if c in numeric_cols]
    cat_feats = [c for c in features if c in categorical_cols]

    task = "regression" if pd.api.types.is_numeric_dtype(y) else "classification"

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                num_feats,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                cat_feats,
            ),
        ],
        remainder="drop",
    )

    if task == "regression":
        model = RandomForestRegressor(n_estimators=220, random_state=42)
    else:
        model = RandomForestClassifier(n_estimators=240, random_state=42, class_weight="balanced")

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y if task == "classification" else None
        )
    except ValueError as e:
        st.error(f"Unable to split data: {e}")
        return

    pipe = Pipeline([("prep", preprocessor), ("model", model)])

    with st.spinner("Training model..."):
        pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    if task == "regression":
        st.metric("R²", f"{r2_score(y_test, y_pred):.3f}")
        st.metric("MAE", f"{mean_absolute_error(y_test, y_pred):.3f}")
    else:
        st.metric("Accuracy", f"{accuracy_score(y_test, y_pred):.3f}")
        st.metric("F1 (weighted)", f"{f1_score(y_test, y_pred, average='weighted'):.3f}")

    st.caption(f"Task auto-detected as **{task}** based on target dtype.")
