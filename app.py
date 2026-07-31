import streamlit as st
import os

# Page configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="Apapacho | Psicología",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium aesthetics
st.markdown("""
    <style>
        :root {
            --app-bg: #FAF3E0;
            --app-text: #2F4F4F;
            --hero-bg: linear-gradient(135deg, #FDFBF7 0%, #F0E6D2 100%);
            --hero-title-gradient: -webkit-linear-gradient(#4A7C59, #2F4F4F);
            --hero-title-solid: #4A7C59;
            --hero-subtitle: #556B61;
            --card-bg: #FDFBF7;
            --card-border: #DCE3E0;
            --card-hover-border: #4A7C59;
            --card-shadow: rgba(74, 124, 89, 0.15);
            --banner-p: #f7f4ec;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --app-bg: #0E1117;
                --app-text: #FAFAFA;
                --hero-bg: linear-gradient(135deg, #1E1E1E 0%, #121212 100%);
                --hero-title-gradient: -webkit-linear-gradient(#A5D6A7, #81C784);
                --hero-title-solid: #A5D6A7;
                --hero-subtitle: #B0BEC5;
                --card-bg: #1A1A1A;
                --card-border: #333333;
                --card-hover-border: #81C784;
                --card-shadow: rgba(165, 214, 167, 0.15);
                --banner-p: #E0E0E0;
            }
        }

        /* General styling */
        .main {
            background-color: var(--app-bg);
            color: var(--app-text);
            font-family: 'Inter', sans-serif;
        }

        h1, h2, h3 {
            color: var(--app-text);
            font-weight: 700;
        }

        .page-banner {
            background: linear-gradient(135deg, #4A7C59 0%, #2F4F4F 100%);
            color: white;
            border-radius: 20px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 1.4rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }

        .page-banner h1 {
            color: white;
            margin: 0 0 0.3rem 0;
            font-size: 2rem;
        }

        .page-banner p {
            color: var(--banner-p);
            margin: 0;
            font-size: 1rem;
        }

        /* Hero Section */
        .hero {
            padding: 4rem 2rem;
            text-align: center;
            background: var(--hero-bg);
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            border: 1px solid var(--card-border);
        }

        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            color: var(--hero-title-solid);
            background: var(--hero-title-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            font-size: 1.2rem;
            color: var(--hero-subtitle);
            max-width: 600px;
            margin: 0 auto 2rem auto;
            line-height: 1.6;
        }

        /* Features Section */
        .feature-card {
            background-color: var(--card-bg);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            border: 1px solid var(--card-border);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            color: var(--app-text);
        }

        .feature-card p {
            color: var(--hero-subtitle);
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px var(--card-shadow);
            border-color: var(--card-hover-border);
        }

        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        /* Hide sidebar completely on landing page */
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Navigation Buttons
col1, col2 = st.columns([8, 1])
with col2:
    if st.button("Panel Admin ⚙️", use_container_width=True):
        st.switch_page("pages/2_Admin.py")

st.markdown("""
    <div class="page-banner">
        <h1>Apapacho</h1>
        <p>Tu espacio seguro para hablar de ansiedad, burnout, estrés y bienestar emocional.</p>
    </div>
""", unsafe_allow_html=True)

st.info("⚠️ Apapacho es un apoyo emocional inicial. No sustituye a un profesional de la salud mental ni a la atención médica de emergencia.")

# Hero Section
hero_text_col, hero_img_col = st.columns([1, 1], gap="large")

with hero_text_col:
    st.markdown("""
        <div style="padding-top: 2rem; padding-bottom: 1rem;">
            <h1 style="font-size: 4rem; color: var(--hero-title-solid); font-weight: 800; margin-bottom: 1.5rem; line-height: 1.2;">
                Tu bienestar mental es nuestra prioridad
            </h1>
            <p style="font-size: 1.25rem; color: var(--hero-subtitle); margin-bottom: 2rem; line-height: 1.6;">
                <b>Apapacho</b> es tu espacio seguro para manejar el estrés laboral y la tensión universitaria. 
                Habla con nuestra especialista clínica impulsada por Inteligencia Artificial en cualquier momento, desde cualquier lugar.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Call to Action button directly below text
    col_btn, _ = st.columns([1, 1])
    with col_btn:
        if st.button("Comenzar Terapia Ahora 🌿", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Chat.py")

with hero_img_col:
    # Adding a bit of top margin to center image vertically with text
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.image("assets/apapacho_hero.png", use_column_width="always")

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Features Section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎓</div>
            <h3>Estrés Universitario</h3>
            <p>Estrategias probadas para manejar la ansiedad por exámenes, la presión académica y la gestión del tiempo.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💼</div>
            <h3>Tensión Laboral</h3>
            <p>Aprende a establecer límites, manejar el burnout y mejorar tus relaciones interpersonales en el trabajo.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3>Privacidad Total</h3>
            <p>Tus conversaciones son confidenciales. Un espacio libre de juicios donde puedes expresarte libremente.</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 5rem; padding-top: 2rem; border-top: 1px solid #30363d; color: #8b949e;">
        <p>Apapacho no sustituye la atención médica o psiquiátrica profesional ni el apoyo de emergencia cuando lo necesitas.</p>
    </div>
""", unsafe_allow_html=True)
