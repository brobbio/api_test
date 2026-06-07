"""DB initialization utilities"""
import os
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DEFAULT_DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/items"

Base = declarative_base()
_engine = None

def get_engine() -> Engine:
    """Create and return a SQLAlchemy engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(os.getenv("DB_URL", DEFAULT_DB_URL), pool_pre_ping=True)
    return _engine


def get_db():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()