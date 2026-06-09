"""SQLAlchemy ORM table classes declaration"""

from sqlalchemy import Column, Integer, Text, Date, Float, JSON, UniqueConstraint, String
from sqlalchemy.orm import declarative_base
from src.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

    role = Column(String)  # "maintainer" or "clerk"