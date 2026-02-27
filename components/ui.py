from pathlib import Path
import streamlit as st

THEME_PATH = Path(__file__).resolve().parents[1] / "assets" / "style.css"

def load_theme():
    if THEME_PATH.exists():
        with open(THEME_PATH) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.markdown('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>', unsafe_allow_html=True)

def hero_section():
    st.markdown(
        """
        <div class="hero glass-card fade-in">
            <div class="pill">Coffee-grade • Auto ML • Live viz</div>
            <h1>Dynamic Data Command Center</h1>
            <p>Drop any CSV, get instant KPIs, visuals, clustering, and predictions with zero setup.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def lottie_block(url, height=180):
    st.markdown(
        f"""
        <div class="lottie-wrap glass-card">
            <lottie-player src="{url}" background="transparent" speed="1" loop autoplay style="height:{height}px;"></lottie-player>
        </div>
        """,
        unsafe_allow_html=True,
    )

def typed_badges(num_cols, cat_cols, dt_cols):
    st.markdown(
        f"""
        <div class="type-badges">
          <span class="badge primary">Numeric: {len(num_cols)}</span>
          <span class="badge">Categorical: {len(cat_cols)}</span>
          <span class="badge">Datetime: {len(dt_cols)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
