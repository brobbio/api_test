"""DB initialization utilities"""
import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

DEFAULT_DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/items"

def get_engine() -> Engine:
    """Create and return a SQLAlchemy engine."""
    return create_engine(os.getenv("DB_URL", DEFAULT_DB_URL), pool_pre_ping=True)

engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()