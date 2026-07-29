from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database

app = FastAPI(
    title="Apapacho API",
    description="API pública para consultar datos de la aplicación Apapacho.",
    version="1.0.0"
)

# Modelo Pydantic para el POST de usuarios
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "patient"

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Apapacho. Usa /docs para ver la documentación interactiva."}

@app.get("/api/v1/users")
def get_users():
    """
    Recupera todos los usuarios de la base de datos.
    Por seguridad, este endpoint filtra las contraseñas cifradas y no las incluye en la respuesta.
    """
    users = database.get_all_users()
    # Los usuarios ya se devuelven desde get_all_users() sin contraseña (id, name, email, role).
    return {"status": "success", "data": users}

@app.get("/api/v1/agents")
def get_agents():
    """
    Recupera todos los agentes de inteligencia artificial registrados.
    """
    agents = database.get_all_agents()
    return {"status": "success", "data": agents}

@app.post("/api/v1/users", status_code=201)
def create_new_user(user: UserCreate):
    """
    Crea un nuevo usuario en la base de datos.
    Este es un ejemplo de endpoint POST, donde en un futuro se implementarán los tokens de seguridad.
    """
    success = database.create_user(user.name, user.email, user.password, user.role)
    if success:
        return {"status": "success", "message": f"Usuario {user.name} creado exitosamente."}
    else:
        raise HTTPException(status_code=400, detail="El correo electrónico ya existe en la base de datos.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
