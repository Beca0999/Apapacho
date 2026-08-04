import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Permitir configurar la URL de la BD desde la variable de entorno (útil para Render/prod)
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./psicologa.db")

# Para SQLite necesitamos pasar `check_same_thread` en entornos multi-hilo
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

engine = create_engine(DB_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Crear las tablas según los modelos si no existen (inicialización automática)
Base.metadata.create_all(bind=engine)

def get_db():
    """Generador para obtener una sesión de la base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
