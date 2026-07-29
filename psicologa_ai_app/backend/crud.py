from sqlalchemy.orm import Session
from . import models

# === User CRUD ===
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, username: str, email: str):
    db_user = models.User(username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# === Agent CRUD ===
def get_agent(db: Session, agent_id: int):
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()

def get_agents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Agent).offset(skip).limit(limit).all()

def create_agent(db: Session, name: str, description: str, system_prompt: str):
    db_agent = models.Agent(name=name, description=description, system_prompt=system_prompt)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def update_agent(db: Session, agent_id: int, name: str, description: str, system_prompt: str):
    db_agent = get_agent(db, agent_id)
    if db_agent:
        db_agent.name = name
        db_agent.description = description
        db_agent.system_prompt = system_prompt
        db.commit()
        db.refresh(db_agent)
    return db_agent

def delete_agent(db: Session, agent_id: int):
    db_agent = get_agent(db, agent_id)
    if db_agent:
        db.delete(db_agent)
        db.commit()
    return db_agent
