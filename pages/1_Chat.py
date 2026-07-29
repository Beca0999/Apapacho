import streamlit as st
from agent import get_chat_session, send_message
import os
from dotenv import load_dotenv
from database import verify_user, create_user, get_journal_entries, add_journal_entry, get_user_by_id
import extra_streamlit_components as stx

st.set_page_config(page_title="Chat - Apapacho", page_icon="💬", layout="centered")

# Basic styling
st.markdown("""
    <style>
        :root {
            --bg-color: #FAF3E0;
            --text-main: #20312C;
            --chat-bg: #FFFFFF;
            --border-color: #DCE3E0;
            --card-bg: #FFFDF8;
            --activity-bg: #F8F1E3;
            --activity-border: #E7D9BC;
            --h3-color: #2F4F4F;
            --h4-color: #4A7C59;
            --banner-p: #f8f3ea;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg-color: #0E1117;
                --text-main: #FAFAFA;
                --chat-bg: #1E1E1E;
                --border-color: #333333;
                --card-bg: #1A1A1A;
                --activity-bg: #252525;
                --activity-border: #444444;
                --h3-color: #A5D6A7;
                --h4-color: #81C784;
                --banner-p: #E0E0E0;
            }
        }

        .stApp {
            background-color: var(--bg-color);
            color: var(--text-main);
        }
        .stChatMessage {
            background-color: var(--chat-bg);
            border-radius: 10px;
            border: 1px solid var(--border-color);
            padding: 10px;
            color: var(--text-main);
        }
        .stChatMessage [data-testid="stMarkdownContainer"] p,
        .stChatMessage [data-testid="stMarkdownContainer"] li {
            color: var(--text-main) !important;
        }
        .banner {
            background: linear-gradient(135deg, #4A7C59 0%, #2F4F4F 100%);
            color: white;
            border-radius: 18px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 22px rgba(0,0,0,0.12);
            width: 100%;
            box-sizing: border-box;
        }
        .banner h1 {
            color: white;
            font-size: 1.6rem;
            margin: 0 0 0.25rem 0;
        }
        .banner p {
            color: var(--banner-p);
            margin: 0;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        .resource-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 0.9rem 1rem;
            margin-top: 0.75rem;
            color: var(--text-main);
        }
        .resource-card h3 {
            margin-top: 0;
            color: var(--h3-color);
        }
        .activity-card {
            background: var(--activity-bg);
            border-radius: 12px;
            padding: 0.8rem;
            border: 1px solid var(--activity-border);
            height: 100%;
            color: var(--text-main);
            margin-bottom: 0.6rem;
        }
        .activity-card h4 {
            margin-bottom: 0.3rem;
            color: var(--h4-color);
        }
        .chat-panel {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 0.7rem;
            overflow-wrap: anywhere;
        }
        @media (max-width: 768px) {
            .banner {
                padding: 0.9rem 1rem;
            }
            .banner h1 {
                font-size: 1.3rem;
            }
            .banner p {
                font-size: 0.9rem;
            }
            .st-emotion-cache-1y4p8pa {
                padding: 0.4rem !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Cookie Manager for sessions
cookie_manager = stx.CookieManager()

# Login System
if not st.session_state.get('logged_in', False):
    cookie_user_id = cookie_manager.get("apapacho_user_id")
    if cookie_user_id:
        # Prevent re-running endlessly if cookie is being processed
        # stx.CookieManager requires a small delay on first load, so we check carefully
        user = get_user_by_id(int(cookie_user_id))
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            st.rerun()
    st.markdown("""
        <div class="banner">
            <h1>Acceso a Apapacho</h1>
            <p>Inicia sesión o regístrate para hablar con Lyna.</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab_login, tab_register = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse"])
    
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Ingresar")
            if submitted:
                user = verify_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user
                    cookie_manager.set("apapacho_user_id", str(user["id"]), max_age=86400*30)
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
                    
    with tab_register:
        with st.form("register_form"):
            reg_name = st.text_input("Nombre completo")
            reg_email = st.text_input("Correo electrónico")
            reg_pass = st.text_input("Contraseña", type="password")
            reg_submitted = st.form_submit_button("Crear cuenta")
            if reg_submitted:
                if reg_name and reg_email and reg_pass:
                    if create_user(reg_name, reg_email, reg_pass):
                        st.success("¡Registro exitoso! Ahora puedes iniciar sesión.")
                    else:
                        st.error("El correo ya está registrado.")
                else:
                    st.warning("Completa todos los campos.")
    
    st.markdown("---")
    if st.button("← Volver al Inicio"):
        st.switch_page("app.py")
    st.stop()

# --- Chat Interface (Only runs if logged in) ---
st.markdown("""
    <div class="banner">
        <h1>Apapacho</h1>
        <p>Tu apoyo emocional guiado por IA para ansiedad, burnout y estrés.</p>
    </div>
""", unsafe_allow_html=True)

col_img, col_text = st.columns([1, 4], gap="small")
with col_img:
    st.image("assets/apapacho_chat.png", use_container_width=True)
with col_text:
    st.title("🌿 Sesión con Lyna")
    st.caption("Habla con calma, toma tu tiempo y cuida tu bienestar.")

st.info("⚠️ Apapacho es un apoyo emocional inicial. No sustituye a un profesional de salud mental ni a la atención médica de emergencia. Si sientes riesgo inmediato, busca ayuda profesional o una línea de emergencia.")

with st.sidebar:
    st.markdown(f"**👤 Hola, {st.session_state.current_user['name']}**")
    if st.button("Cerrar Sesión"):
        cookie_manager.delete("apapacho_user_id")
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    st.markdown("---")
    
    st.markdown("<div class='chat-panel'>", unsafe_allow_html=True)
    st.subheader("🧭 Recursos de apoyo")
    emergency_number = os.getenv("APAPACHO_EMERGENCY_NUMBER", "911")
    support_number = os.getenv("APAPACHO_SUPPORT_NUMBER", "800 911 2000")
    st.markdown(f"""
        <div class="resource-card">
            <h3>Especialistas y números</h3>
            <p><strong>Emergencias:</strong> {emergency_number}</p>
            <p><strong>Apoyo psicológico o telefónico:</strong> {support_number}</p>
            <p><strong>Psicólogo/a clínico/a:</strong> agenda una valoración en tu clínica o seguro.</p>
            <p><strong>Psiquiatra:</strong> consulta en tu centro de salud si la ansiedad o el burnout afectan tu rendimiento o tu sueño.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Actividades rápidas")
    st.markdown("""
        <div class="activity-card">
            <h4>🫁 Respiración 4-4-6</h4>
            <p>Inhala 4 segundos, retén 4 y exhala 6. Repite 5 veces para bajar la tensión.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="activity-card">
            <h4>🚶‍♀️ Paseo breve</h4>
            <p>Da un paseo de 10 minutos sin celular para despejar la mente y recuperar calma.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="activity-card">
            <h4>📓 Diario Emocional</h4>
            <p>Registra cómo te sientes hoy para llevar un historial.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("journal_form"):
        journal_text = st.text_area("¿Cómo te sientes?", height=80, label_visibility="collapsed", placeholder="Hoy me siento...")
        journal_submit = st.form_submit_button("Guardar en mi diario")
        if journal_submit and journal_text.strip():
            add_journal_entry(st.session_state.current_user["id"], journal_text.strip())
            st.success("¡Registro guardado!")
    
    entries = get_journal_entries(st.session_state.current_user["id"])
    if entries:
        st.markdown(f"<small>Tienes {len(entries)} entradas guardadas.</small>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Check API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "tu_api_key_aqui":
    st.error("⚠️ La clave de API de Gemini no está configurada. Por favor, actualiza el archivo `.env`.")
    st.stop()

# Initialize session state for chat history
if "chat_session" not in st.session_state:
    session, error = get_chat_session()
    if error:
        st.error(f"Error al inicializar el agente: {error}")
        st.stop()
    st.session_state.chat_session = session

    # Add initial greeting
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "model", "content": "Hola. Soy Lyna. Este chat es un apoyo emocional inicial y no sustituye a un profesional de salud mental ni a la atención de emergencia. Si te sientes muy abrumado, puedo ayudarte con respiraciones, pausas, técnicas para ansiedad o burnout y sugerirte apoyo profesional. ¿Cómo te sientes hoy?"}
        ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get model response
    with st.chat_message("model"):
        with st.spinner("Lyna está escribiendo..."):
            response_text = send_message(st.session_state.chat_session, prompt)
            st.markdown(response_text)

    # Add model response to state
    st.session_state.messages.append({"role": "model", "content": response_text})

if st.button("← Volver al Inicio"):
    st.switch_page("app.py")
