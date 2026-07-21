from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings
from sqlalchemy import text

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

with engine.connect() as conn:
    print(conn.execute(text("SELECT current_database();")).scalar())
    print(conn.execute(text("SELECT current_schema();")).scalar())

print("DATABASE:", settings.database_url)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
