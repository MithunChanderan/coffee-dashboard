from pathlib import Path
import streamlit as st


THEME_PATH = Path(__file__).resolve().parents[1] / "assets" / "style.css"


def load_theme():
    if THEME_PATH.exists():
        with open(THEME_PATH) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    # Lottie web component
    st.markdown(
        '<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>',
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero glass-card fade-in">
            <div class="pill">Coffee-grade • Auto ML • Live viz</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def lottie_block(url: str, height: int = 140):
    st.markdown(
        f"""
        <div class="lottie-wrap glass-card">
            <lottie-player src="{url}" background="transparent" speed="1" loop autoplay style="height:{height}px;"></lottie-player>
        </div>
        """,
        unsafe_allow_html=True,
    )
