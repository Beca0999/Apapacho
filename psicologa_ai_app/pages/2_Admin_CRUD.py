import streamlit as st
from backend.database import SessionLocal
from backend import crud

st.set_page_config(page_title="Admin CRUD", page_icon="⚙️", layout="wide")

st.title("⚙️ Panel de Administración - CRUD")

db = SessionLocal()

tab1, tab2 = st.tabs(["👥 Gestión de Usuarios", "🧠 Gestión de Agentes IA"])

# --- TAB 1: Usuarios ---
with tab1:
    st.header("Usuarios del Sistema")
    
    with st.expander("➕ Crear Nuevo Usuario"):
        with st.form("create_user_form"):
            new_username = st.text_input("Nombre de Usuario")
            new_email = st.text_input("Correo Electrónico")
            submit_user = st.form_submit_button("Guardar Usuario")
            if submit_user:
                if new_username and new_email:
                    crud.create_user(db, username=new_username, email=new_email)
                    st.success(f"Usuario {new_username} creado exitosamente!")
                    st.rerun()
                else:
                    st.error("Por favor completa todos los campos.")
    
    st.subheader("Lista de Usuarios")
    users = crud.get_users(db)
    if users:
        for u in users:
            col_id, col_name, col_email, col_action = st.columns([1, 3, 3, 2])
            col_id.write(u.id)
            col_name.write(u.username)
            col_email.write(u.email)
            if col_action.button("Eliminar", key=f"del_user_{u.id}", type="primary"):
                crud.delete_user(db, u.id)
                st.rerun()
    else:
        st.info("No hay usuarios registrados.")

# --- TAB 2: Agentes ---
with tab2:
    st.header("Agentes IA (Perfiles de Psicólogos)")
    
    with st.expander("➕ Crear Nuevo Agente", expanded=True):
        st.info("El prompt del sistema le indica a Gemini cómo debe comportarse. Por ejemplo: 'Eres una psicóloga clínica empática especialista en estrés universitario. Usa tono cálido y profesional.'")
        with st.form("create_agent_form"):
            new_agent_name = st.text_input("Nombre del Agente")
            new_agent_desc = st.text_input("Descripción breve")
            new_agent_prompt = st.text_area("Prompt del Sistema (Instrucciones para Gemini)")
            submit_agent = st.form_submit_button("Guardar Agente")
            if submit_agent:
                if new_agent_name and new_agent_prompt:
                    crud.create_agent(db, name=new_agent_name, description=new_agent_desc, system_prompt=new_agent_prompt)
                    st.success(f"Agente {new_agent_name} creado exitosamente!")
                    st.rerun()
                else:
                    st.error("El nombre y el prompt son obligatorios.")

    st.subheader("Lista de Agentes")
    agents = crud.get_agents(db)
    if agents:
        for a in agents:
            with st.container(border=True):
                col_info, col_actions = st.columns([4, 1])
                with col_info:
                    st.write(f"**{a.name}** - {a.description}")
                    st.caption(f"Prompt: {a.system_prompt[:100]}...")
                with col_actions:
                    if st.button("Eliminar", key=f"del_agent_{a.id}", type="primary"):
                        crud.delete_agent(db, a.id)
                        st.rerun()
    else:
        st.info("No hay agentes registrados.")

db.close()
