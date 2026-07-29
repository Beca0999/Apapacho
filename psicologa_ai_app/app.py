import streamlit as st
from backend.database import engine, Base

# Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

st.set_page_config(
    page_title="Apapacho - Psicóloga IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para un diseño más moderno y profesional
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #2E86C1;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5D6D7E;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">Apapacho - Tu Espacio Seguro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Psicóloga Clínica con Inteligencia Artificial Especializada en Estrés Académico y Laboral</p>', unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ¿Sientes que la universidad o el trabajo te abruman?")
    st.write("""
    **Apapacho** es una herramienta diseñada para escucharte y guiarte en momentos de alta tensión. 
    A través de un chatbot potenciado por IA y basado en principios de psicología clínica, puedes hablar 
    abiertamente sobre tus preocupaciones, estrés por exámenes, ambiente laboral o sobrecarga de tareas.
    """)
    st.write("✅ **Confidencialidad:** Tus conversaciones son privadas.")
    st.write("✅ **Disponibilidad 24/7:** Siempre que necesites un respiro, a cualquier hora.")
    st.write("✅ **Especializada:** Entrenada específicamente para el contexto de tensión de estudiantes universitarios y jóvenes profesionales.")

with col2:
    st.info("💡 **Primeros Pasos:**")
    st.write("1. Dirígete a la sección de **Admin CRUD** en el menú de la izquierda para configurar un Agente IA (si aún no hay uno).")
    st.write("2. Ve a la sección **Chatbot** para comenzar a hablar con la psicóloga.")
    
    st.write("---")
    st.write("¿Estás listo para hablar?")
    if st.button("Ir al Chatbot", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Chatbot.py")

st.divider()
st.caption("⚠️ Nota: Esta herramienta utiliza Inteligencia Artificial y está diseñada exclusivamente para apoyo emocional inicial. No reemplaza la evaluación o terapia psicológica por un profesional humano de la salud, especialmente en crisis o emergencias.")
