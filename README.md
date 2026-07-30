# 🌿 Apapacho - Tu Compañera de Bienestar Mental

**Apapacho** es una aplicación web interactiva que sirve como un espacio seguro para hablar de ansiedad, burnout, estrés y bienestar emocional. La aplicación cuenta con "Lyna", una especialista clínica impulsada por Inteligencia Artificial diseñada para escuchar activamente, validar emociones y proporcionar recursos rápidos para el manejo del estrés universitario y laboral.

## ✨ Características Principales

*   **Chat Guiado por IA (Lyna):** Integración nativa con la API de Google Gemini (`gemini-3.1-flash-lite`) para ofrecer asistencia psicológica conversacional, dotada de empatía y profesionalismo.
*   **Diario Emocional:** Un espacio privado donde los usuarios pueden registrar diariamente sus emociones y sentimientos. El historial se guarda de manera confidencial en la base de datos local.
*   **Persistencia de Sesiones Seguras:** Gracias al uso de cookies seguras, el sistema recuerda el inicio de sesión del usuario incluso después de recargar la página o cerrar el navegador.
*   **Panel de Administración Integral:** Interfaz dedicada (`pages/2_Admin.py`) para gestionar perfiles de usuarios y parametrizar los comportamientos (personas) de los diferentes Agentes de IA.
*   **API REST (En desarrollo):** Puntos de acceso públicos (`api.py`) utilizando FastAPI para poder conectar clientes externos a la base de usuarios y agentes registrados en el futuro.
*   **Interfaz Premium y Accesible:** Una capa visual cuidada construida sobre Streamlit con inyecciones de CSS puro para garantizar una experiencia tranquila, incluyendo soporte para *Modo Oscuro*.

---

## 🛠️ Stack Tecnológico

*   **Frontend y Motor Web:** [Streamlit](https://streamlit.io/)
*   **Inteligencia Artificial:** SDK GenAI de Google (`google-genai`)
*   **Base de Datos:** SQLite3 (Persistencia local en `database.db`)
*   **Autenticación y Sesiones:** `extra-streamlit-components` para manejo de cookies.
*   **API Auxiliar:** FastAPI + Uvicorn
*   **Variables de Entorno:** `python-dotenv`

---

## 🚀 Requisitos e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd apapacho
   ```

2. **Crear y activar un entorno virtual (Recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # venv\Scripts\activate   # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno (`.env`):**
   Crea un archivo llamado `.env` en la raíz del proyecto. Este archivo no se sube a GitHub por seguridad.
   ```env
   GEMINI_API_KEY=tu_clave_secreta_aqui
   GEMINI_MODEL=gemini-3.1-flash-lite
   APAPACHO_EMERGENCY_NUMBER="911"
   APAPACHO_SUPPORT_NUMBER="800 911 2000"
   ```

5. **Iniciar la Aplicación Web:**
   ```bash
   streamlit run app.py
   ```
   *La aplicación estará disponible localmente en `http://localhost:8501`*

---

## ☁️ Despliegue en Render

Para publicar tu aplicación en [Render](https://render.com/), el repositorio ya incluye un archivo `render.yaml` (Blueprint) que automatiza casi todo el proceso:

1. **Sube tu código a GitHub** (asegúrate de hacer push a tu repositorio).
2. Entra a tu cuenta de **Render** y ve a **Blueprints > New Blueprint Instance**.
3. Conecta tu cuenta de GitHub y selecciona el repositorio de `apapacho`.
4. Render detectará el archivo `render.yaml`. Durante la configuración, te pedirá que ingreses de forma segura el valor de `GEMINI_API_KEY`.
5. Haz clic en **Apply** y Render instalará todo automáticamente.

> **⚠️ Nota importante sobre la Base de Datos (SQLite):**
> En el plan gratuito de Render, el disco duro es *efímero*. Esto significa que cada vez que la app entre en reposo o se reinicie, tu base de datos (`database.db`) **se borrará y perderás los usuarios registrados y los diarios**. Para producción a largo plazo, deberás cambiar SQLite por una base de datos en la nube gratuita (como PostgreSQL, que también ofrece Render de forma gratuita) o contratar un "Persistent Disk" en Render.

---

## 📁 Estructura del Proyecto

```text
apapacho/
│
├── app.py                   # Página principal (Landing Page y ruteo).
├── agent.py                 # Lógica de conexión y configuración del SDK de Gemini (Google GenAI).
├── database.py              # Scripts SQL para creación y CRUD (Usuarios, Agentes, Diario).
├── api.py                   # Endpoints de FastAPI para integraciones futuras.
├── requirements.txt         # Listado de dependencias del proyecto.
├── .env                     # (No incluido) Credenciales seguras.
├── .gitignore               # Configuración para ignorar archivos confidenciales/locales.
│
├── pages/                   # Múltiples páginas de la interfaz Streamlit.
│   ├── 1_Chat.py            # Interfaz del chat interactivo con Lyna y el Diario Emocional.
│   └── 2_Admin.py           # Panel para creación y eliminación de usuarios y agentes.
│
└── assets/                  # Directorio para imágenes y recursos estáticos.
```

---

## ⚠️ Descargo de Responsabilidad Médica
Apapacho es una herramienta de **apoyo emocional inicial y contención**. **En ningún momento** sustituye a un profesional de la salud mental, una terapia psicológica convencional o atención psiquiátrica de emergencia. Si el usuario se encuentra en riesgo inminente, la plataforma lo exhortará a buscar los canales médicos adecuados (como líneas de emergencia y centros de salud físicos).
