import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, f1_score
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

def render_clustering(df, numeric_cols):
    st.subheader("KMeans Clustering (Elbow)")
    feature_cols = st.multiselect("Select numeric features", numeric_cols, default=numeric_cols[:2])
    if len(feature_cols) < 2:
        st.info("Pick at least two numeric columns.")
        return
    X = df[feature_cols].dropna()
    inertias = []
    k_range = range(2, min(9, len(X)))
    for k in k_range:
        model = KMeans(n_clusters=k, n_init="auto", random_state=42)
        model.fit(X)
        inertias.append(model.inertia_)
    elbow_fig = px.line(x=list(k_range), y=inertias, markers=True, labels={"x":"k", "y":"Inertia"})
    st.plotly_chart(elbow_fig, use_container_width=True)
    k_choice = st.slider("Clusters (k)", min_value=2, max_value=max(k_range), value=3)
    final_model = KMeans(n_clusters=k_choice, n_init="auto", random_state=42)
    labels = final_model.fit_predict(X)
    df_view = X.copy()
    df_view["cluster"] = labels
    scatter = px.scatter(df_view, x=feature_cols[0], y=feature_cols[1], color="cluster", title="Clusters")
    st.plotly_chart(scatter, use_container_width=True)
    st.caption(f"Shown on {len(df_view)} rows (dropped NA).")

def render_prediction(df, numeric_cols, categorical_cols):
    st.subheader("Auto Prediction (Regression or Classification)")
    target = st.selectbox("Target column", df.columns)
    feature_candidates = [c for c in df.columns if c != target]
    features = st.multiselect("Feature columns", feature_candidates, default=feature_candidates[:4])
    if not features:
        st.info("Select at least one feature.")
        return

    y = df[target]
    X = df[features]
    num_feats = [c for c in features if c in numeric_cols]
    cat_feats = [c for c in features if c in categorical_cols]

    task = "regression" if pd.api.types.is_numeric_dtype(y) else "classification"

    preprocessor = ColumnTransformer(
        [
            ("num", StandardScaler(), num_feats),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_feats),
        ],
        remainder="drop",
    )

    if task == "regression":
        model = RandomForestRegressor(n_estimators=180, random_state=42)
    else:
        model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y if task=="classification" else None)

    pipe = Pipeline([("prep", preprocessor), ("model", model)])
    with st.spinner("Training model..."):
        pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    if task == "regression":
        st.metric("R²", f"{r2_score(y_test, y_pred):.3f}")
        st.metric("MAE", f"{mean_absolute_error(y_test, y_pred):.3f}")
    else:
        st.metric("Accuracy", f"{accuracy_score(y_test, y_pred):.3f}")
        st.metric("F1", f"{f1_score(y_test, y_pred, average='weighted'):.3f}")

    st.caption(f"Task auto-detected as **{task}** based on target dtype.")
