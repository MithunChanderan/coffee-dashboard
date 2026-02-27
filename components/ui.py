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
        <div class="cinematic-hero fade-in">
            <div class="hero-glow"></div>
            <div class="particles">
                <span class="particle p1"></span>
                <span class="particle p2"></span>
                <span class="particle p3"></span>
                <span class="particle p4"></span>
            </div>
            <div class="glass-shell">
                <div class="pill">Coffee-grade • Auto ML • Live viz</div>
                <h1 class="glow-text shimmer">{title}</h1>
                <p class="subhead animated-gradient">{subtitle}</p>
            </div>
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


def empty_state_hero():
    """Premium animated hero shown when no upload is provided."""
    st.markdown(
        """
        <div class="coffee-hero">
          <div class="steam s1"></div>
          <div class="steam s2"></div>
          <div class="steam s3"></div>
          <div class="hero-copy">
            <div class="pill">Demo-ready • Secure • Reusable</div>
            <h1 class="glow-text floaty">Coffee Intelligence Platform</h1>
            <p class="subhead animated-gradient">AI-Powered Analytics. Elegant. Insightful. Dynamic.</p>
          </div>
        </div>
        <div class="feature-grid">
          <div class="feature-card glass-card slide-up"><span>☕</span><div>Smart Clustering Engine</div></div>
          <div class="feature-card glass-card slide-up" style="animation-delay:0.05s"><span>📈</span><div>Predictive Revenue Modeling</div></div>
          <div class="feature-card glass-card slide-up" style="animation-delay:0.1s"><span>🧭</span><div>Automated Data Profiling</div></div>
          <div class="feature-card glass-card slide-up" style="animation-delay:0.15s"><span>🧪</span><div>Interactive AI Lab</div></div>
        </div>
        <div class="cta-wrap">
          <button class="cta-glow" id="upload-cta">Upload Dataset to Begin Exploration</button>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_image_cards():
    st.markdown(
        """
        <div class="feature-img-grid">
            <div class="feature-img-card elevate" style="background-image:url('https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80');">
                <div class="overlay"></div>
                <div class="text"><h3>Smart Clustering Intelligence</h3><p>Adaptive KMeans insights tuned to your data.</p></div>
            </div>
            <div class="feature-img-card elevate" style="background-image:url('https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=1200&q=80');">
                <div class="overlay"></div>
                <div class="text"><h3>Predictive Revenue AI</h3><p>Auto-detects regression vs classification with rich metrics.</p></div>
            </div>
            <div class="feature-img-card elevate" style="background-image:url('https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=1200&q=80&sat=-65');">
                <div class="overlay"></div>
                <div class="text"><h3>Automated Data Profiling Engine</h3><p>Smart typing, KPIs, histograms, bars, and correlations.</p></div>
            </div>
            <div class="feature-img-card elevate" style="background-image:url('https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=1200&q=80&sat=-35');">
                <div class="overlay"></div>
                <div class="text"><h3>Interactive Machine Learning Lab</h3><p>Live chart builder and inline Python sandbox.</p></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
