from sqlalchemy import text
from database import engine, DATABASE_URL

print("DATABASE_URL present:", "yes" if DATABASE_URL and DATABASE_URL != "sqlite:///./database.db" else "no")
print("Using database backend:", "POSTGRES" if DATABASE_URL.startswith("postgres") else "SQLITE")
print("DATABASE_URL:", DATABASE_URL if DATABASE_URL.startswith("sqlite") else "[postgres connection string hidden]")

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("SELECT 1 =>", result.scalar())
except Exception as e:
    print("Connection test failed:", repr(e))
