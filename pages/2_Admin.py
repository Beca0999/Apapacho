import streamlit as st
import pandas as pd
from database import (
    init_db,
    get_all_users, create_user, delete_user,
    get_all_agents, create_agent, delete_agent, update_agent_status
)

# Ensure database schema exists before the admin page loads.
init_db()

st.set_page_config(page_title="Admin - Apapacho", page_icon="⚙️", layout="wide")

st.markdown("""
    <style>
        :root {
            --app-bg: #FAF3E0;
            --app-text: #2F4F4F;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --app-bg: #0E1117;
                --app-text: #FAFAFA;
            }
        }

        .stApp {
            background-color: var(--app-bg);
            color: var(--app-text);
        }
    </style>
""", unsafe_allow_html=True)

col_img, col_text = st.columns([1, 4])
with col_img:
    st.image("assets/apapacho_admin.png", use_column_width=True)
with col_text:
    st.title("⚙️ Panel de Administración")
    st.markdown("Gestiona los usuarios y los perfiles de los agentes de Inteligencia Artificial de Apapacho.")

tab1, tab2 = st.tabs(["👥 Usuarios", "🤖 Agentes IA"])

# --- USERS TAB ---
with tab1:
    st.header("Gestión de Usuarios")
    
    # Create User Form
    with st.expander("➕ Añadir Nuevo Usuario"):
        with st.form("new_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nombre completo")
            with col2:
                email = st.text_input("Correo electrónico")
            
            password = st.text_input("Contraseña provisional (ej. 123456)", type="password")
            role = st.selectbox("Rol", ["patient", "therapist", "admin"]) 
            
            submit = st.form_submit_button("Crear Usuario")
            if submit:
                if name and email and password:
                    success = create_user(name, email, password, role)
                    if success:
                        st.success(f"Usuario {name} creado correctamente.")
                        st.rerun()
                    else:
                        st.error("Error: El correo electrónico ya existe.")
                else:
                    st.warning("Por favor, completa nombre, correo y contraseña.")
                    
    # Display Users
    st.subheader("Lista de Usuarios")
    users = get_all_users()
    if users:
        df_users = pd.DataFrame(users)
        st.dataframe(df_users, use_container_width=True, hide_index=True)
        
        # Delete User
        with st.form("delete_user_form"):
            st.write("Eliminar usuario")
            user_to_delete = st.selectbox("Selecciona el ID a eliminar", [u['id'] for u in users])
            if st.form_submit_button("Eliminar"):
                delete_user(user_to_delete)
                st.success("Usuario eliminado.")
                st.rerun()
    else:
        st.info("No hay usuarios registrados en la base de datos.")


# --- AGENTS TAB ---
with tab2:
    st.header("Gestión de Agentes")
    
    # Create Agent Form
    with st.expander("➕ Añadir Nuevo Agente"):
        with st.form("new_agent_form"):
            agent_name = st.text_input("Nombre del Agente (ej. Dra. Sofía)")
            agent_persona = st.text_area("Prompt / Persona (Instrucciones para Gemini)", height=150)
            
            submit_agent = st.form_submit_button("Crear Agente")
            if submit_agent:
                if agent_name and agent_persona:
                    create_agent(agent_name, agent_persona)
                    st.success(f"Agente {agent_name} creado.")
                    st.rerun()
                else:
                    st.warning("Completa todos los campos.")
                    
    # Display Agents
    st.subheader("Lista de Agentes")
    agents = get_all_agents()
    if agents:
        df_agents = pd.DataFrame(agents)
        st.dataframe(df_agents, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            # Change active agent
            with st.form("activate_agent_form"):
                st.write("Cambiar estado de Agente")
                agent_to_update = st.selectbox("ID del agente", [a['id'] for a in agents])
                new_status = st.selectbox("Nuevo estado", ["active", "inactive"])
                if st.form_submit_button("Actualizar Estado"):
                    # First, deactivate all if making one active (simple rule for one active agent)
                    if new_status == "active":
                        for a in agents:
                            if a['status'] == 'active':
                                update_agent_status(a['id'], 'inactive')
                    update_agent_status(agent_to_update, new_status)
                    st.success("Estado actualizado.")
                    st.rerun()
        with col2:
            # Delete agent
            with st.form("delete_agent_form"):
                st.write("Eliminar Agente")
                agent_to_delete = st.selectbox("ID a eliminar", [a['id'] for a in agents])
                if st.form_submit_button("Eliminar"):
                    delete_agent(agent_to_delete)
                    st.success("Agente eliminado.")
                    st.rerun()
    else:
        st.info("No hay agentes registrados.")

st.markdown("---")
if st.button("← Volver al Inicio"):
    st.switch_page("app.py")
