# Documentación de la API de Apapacho

Bienvenido a la documentación de la API REST de Apapacho. Esta API permite a aplicaciones externas (o frontends) consultar información sobre los usuarios y los agentes de la base de datos de manera estandarizada mediante formato JSON.

Actualmente la API se encuentra en su fase inicial ("Modo Público"), por lo que **no requiere tokens de autenticación** para los métodos GET (consultas).

## ¿Cómo iniciar el servidor API?
La API está construida con **FastAPI**. Para iniciar el servidor de manera local, ejecuta el siguiente comando en la terminal:
```bash
venv/bin/python api.py
```
El servidor se levantará por defecto en: `http://localhost:8000`

## Endpoints Disponibles

### 1. Obtener todos los Usuarios
- **URL:** `/api/v1/users`
- **Método:** `GET`
- **Descripción:** Devuelve una lista con todos los usuarios registrados en el sistema. *Por seguridad, la contraseña cifrada se oculta automáticamente en la respuesta.*
- **Ejemplo de Respuesta (JSON):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "test",
      "email": "test@example.com",
      "role": "patient"
    }
  ]
}
```

### 2. Obtener todos los Agentes
- **URL:** `/api/v1/agents`
- **Método:** `GET`
- **Descripción:** Devuelve una lista con todos los agentes de Inteligencia Artificial (Ej. Lyna) configurados en el sistema y su estado actual.
- **Ejemplo de Respuesta (JSON):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Lyna",
      "persona": "Eres una psicóloga clínica...",
      "status": "active"
    }
  ]
}
```

### 3. Crear un Nuevo Usuario (Futuro Uso de Tokens)
- **URL:** `/api/v1/users`
- **Método:** `POST`
- **Descripción:** Recibe un objeto JSON para registrar un nuevo usuario en la base de datos.
- **Nota Importante:** Actualmente funciona en modo público (para pruebas), pero conforme la API escale, este endpoint exigirá enviar un **Token de Seguridad** en los Headers de la petición (`Authorization: Bearer <TOKEN>`) tal como se ha planificado. **Los tokens de seguridad y contraseñas nunca deben enviarse mediante el método GET.**
- **Ejemplo de Petición (Body JSON):**
```json
{
  "name": "Juan Perez",
  "email": "juan@example.com",
  "password": "mi_password_seguro",
  "role": "patient"
}
```

## Documentación Interactiva (Swagger UI)
Al usar FastAPI, obtienes documentación interactiva generada automáticamente. Con el servidor corriendo, simplemente entra en tu navegador a:
- [http://localhost:8000/docs](http://localhost:8000/docs)

Allí podrás probar todos los endpoints visualmente sin necesidad de usar Postman o herramientas externas.
