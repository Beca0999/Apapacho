import os
import hashlib
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
_db_initialized = False

print("DATABASE_URL set:" , "no" if DATABASE_URL.startswith("sqlite") else "yes")
if DATABASE_URL.startswith("sqlite"):
    print("Database backend: SQLITE (fallback or local development)")
else:
    print("Database backend: POSTGRES via DATABASE_URL")

DEFAULT_PASSWORD_HASH = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String(20), nullable=False, default="patient")
    password = Column(String, nullable=False, default=DEFAULT_PASSWORD_HASH)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    persona = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    global _db_initialized
    if _db_initialized:
        return

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Use only the primary key column to avoid selecting missing schema columns in older SQLite tables.
        if db.query(Agent.id).count() == 0:
            default_agent = Agent(
                name='Lyna',
                persona='Eres una psicóloga clínica altamente empática y profesional, especializada en estrés laboral y universitario. Tu objetivo es ayudar al usuario a manejar la tensión, ofrecer técnicas de relajación, validar sus emociones y guiarlo hacia un estado de mayor calma y claridad mental. No diagnosticas ni recetas medicamentos. Si detectas que el usuario está en crisis severa, recomiendas buscar ayuda profesional presencial o líneas de emergencia.',
                status='active'
            )
            db.add(default_agent)
            db.commit()
    finally:
        db.close()
    _db_initialized = True


def _ensure_db_initialized():
    if not _db_initialized:
        init_db()


# --- Users CRUD ---

def create_user(name, email, password, role='patient'):
    _ensure_db_initialized()
    db = SessionLocal()
    hashed_pw = hash_password(password)
    user = User(name=name, email=email, password=hashed_pw, role=role)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return True
    except IntegrityError:
        db.rollback()
        return False
    finally:
        db.close()


def verify_user(email, password):
    _ensure_db_initialized()
    db = SessionLocal()
    hashed_pw = hash_password(password)
    user = db.query(User).filter(User.email == email, User.password == hashed_pw).first()
    db.close()
    if user:
        return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
    return None


def get_user_by_id(user_id):
    _ensure_db_initialized()
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user:
        return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
    return None


def get_all_users():
    _ensure_db_initialized()
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]


def delete_user(user_id):
    _ensure_db_initialized()
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()


# --- Agents CRUD ---

def create_agent(name, persona, status='active'):
    _ensure_db_initialized()
    db = SessionLocal()
    agent = Agent(name=name, persona=persona, status=status)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    db.close()


def get_all_agents():
    _ensure_db_initialized()
    db = SessionLocal()
    agents = db.query(Agent).all()
    db.close()
    return [{"id": a.id, "name": a.name, "persona": a.persona, "status": a.status} for a in agents]


def get_active_agent():
    _ensure_db_initialized()
    db = SessionLocal()
    agent = db.query(Agent).filter(Agent.status == 'active').first()
    db.close()
    if agent:
        return {"id": agent.id, "name": agent.name, "persona": agent.persona, "status": agent.status}
    return None


def update_agent_status(agent_id, status):
    _ensure_db_initialized()
    db = SessionLocal()
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if agent:
        agent.status = status
        db.commit()
    db.close()


def delete_agent(agent_id):
    _ensure_db_initialized()
    db = SessionLocal()
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if agent:
        db.delete(agent)
        db.commit()
    db.close()


# --- Journal CRUD ---

def add_journal_entry(user_id, content):
    _ensure_db_initialized()
    db = SessionLocal()
    entry = JournalEntry(user_id=user_id, content=content)
    db.add(entry)
    db.commit()
    db.close()


def get_journal_entries(user_id):
    _ensure_db_initialized()
    db = SessionLocal()
    entries = db.query(JournalEntry).filter(JournalEntry.user_id == user_id).order_by(JournalEntry.timestamp.desc()).all()
    db.close()
    return [{"id": e.id, "content": e.content, "timestamp": e.timestamp} for e in entries]


# The database is initialized explicitly by the application or by migration scripts.
# This prevents Alembic from importing this module and creating tables before migrations run.
