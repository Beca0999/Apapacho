import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Utilizaremos una base de datos SQLite local llamada 'psicologa.db'
DB_URL = "sqlite:///./psicologa.db"

# Configuramos la conexión. 'check_same_thread' es necesario para SQLite en entornos multihilo como Streamlit
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Generador para obtener una sesión de la base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
