"""SQLAlchemy ORM table classes declaration"""

from sqlalchemy import Column, Integer, Text, Date, Float, JSON, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ItemsData(Base):
    """Items data model"""
    __tablename__ = "items_data"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    