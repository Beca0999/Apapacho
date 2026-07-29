import streamlit as st
from backend.database import SessionLocal
from backend import crud
from backend.ai_service import PsychologyAgent

st.set_page_config(page_title="Chatbot - Psicóloga IA", page_icon="💬")

st.title("💬 Sesión con tu Psicóloga IA")

# Obtener los agentes de la base de datos
db = SessionLocal()
agents = crud.get_agents(db)
db.close()

if not agents:
    st.warning("No hay agentes configurados. Por favor ve a 'Admin CRUD' y crea un agente.")
    st.stop()

# Selección de agente
agent_names = {agent.id: agent.name for agent in agents}
selected_agent_id = st.selectbox("Selecciona tu psicóloga", options=list(agent_names.keys()), format_func=lambda x: agent_names[x])

# Inicializar historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicializar o actualizar el agente de IA
if "ai_agent" not in st.session_state or st.session_state.get("current_agent_id") != selected_agent_id:
    selected_agent = next((a for a in agents if a.id == selected_agent_id), None)
    if selected_agent:
        try:
            st.session_state.ai_agent = PsychologyAgent(system_prompt=selected_agent.system_prompt)
            st.session_state.current_agent_id = selected_agent.id
            # Reiniciar historial si cambiamos de agente
            st.session_state.messages = [
                {"role": "assistant", "content": f"Hola, soy {selected_agent.name}. Estoy aquí para escucharte de manera confidencial. ¿Cómo te sientes hoy respecto a tus responsabilidades?"}
            ]
        except ValueError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"Error al inicializar la IA: {e}")
            st.stop()

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtener respuesta del agente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = st.session_state.ai_agent.send_message(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Ocurrió un error de conexión: {e}")
