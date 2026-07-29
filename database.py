import sqlite3
import os
import hashlib

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'patient',
            password TEXT NOT NULL DEFAULT '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92' -- '123456' hashed
        )
    ''')
    
    # Check if password column exists (for migrating existing DB)
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    if "password" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN password TEXT NOT NULL DEFAULT '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'")
    
    # Agents table
    c.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            persona TEXT NOT NULL,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    # Insert default agent if empty
    c.execute('SELECT COUNT(*) FROM agents')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO agents (name, persona, status) 
            VALUES (?, ?, ?)
        ''', ('Lyna', 'Eres una psicóloga clínica altamente empática y profesional, especializada en estrés laboral y universitario. Tu objetivo es ayudar al usuario a manejar la tensión, ofrecer técnicas de relajación, validar sus emociones y guiarlo hacia un estado de mayor calma y claridad mental. No diagnosticas ni recetas medicamentos. Si detectas que el usuario está en crisis severa, recomiendas buscar ayuda profesional presencial o líneas de emergencia.', 'active'))
    
    # Journal entries table
    c.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Users CRUD ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(name, email, password, role='patient'):
    conn = get_connection()
    c = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        c.execute('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)', (name, email, hashed_pw, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    hashed_pw = hash_password(password)
    c.execute('SELECT id, name, email, role FROM users WHERE email = ? AND password = ?', (email, hashed_pw))
    user = c.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "name": user[1], "email": user[2], "role": user[3]}
    return None

def get_user_by_id(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, email, role FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "name": user[1], "email": user[2], "role": user[3]}
    return None

def get_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, email, role FROM users')
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2], "role": r[3]} for r in rows]

def delete_user(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

# --- Agents CRUD ---
def create_agent(name, persona, status='active'):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO agents (name, persona, status) VALUES (?, ?, ?)', (name, persona, status))
    conn.commit()
    conn.close()

def get_all_agents():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM agents')
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "persona": r[2], "status": r[3]} for r in rows]

def get_active_agent():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM agents WHERE status = "active" LIMIT 1')
    r = c.fetchone()
    conn.close()
    if r:
        return {"id": r[0], "name": r[1], "persona": r[2], "status": r[3]}
    return None

def update_agent_status(agent_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE agents SET status = ? WHERE id = ?', (status, agent_id))
    conn.commit()
    conn.close()

def delete_agent(agent_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM agents WHERE id = ?', (agent_id,))
    conn.commit()
    conn.close()

# --- Journal CRUD ---
def add_journal_entry(user_id, content):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO journal_entries (user_id, content) VALUES (?, ?)', (user_id, content))
    conn.commit()
    conn.close()

def get_journal_entries(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, content, timestamp FROM journal_entries WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "content": r[1], "timestamp": r[2]} for r in rows]

# Initialize DB when this module is loaded
init_db()
