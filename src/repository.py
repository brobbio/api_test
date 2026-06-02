"""Database persistence utilities for items data."""

import logging
from typing import Any, Dict
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models import ItemsData

def insert_item(
    session: Session,
    name: str,
    description: str
) -> None:
    """Upsert daily coin data"""
    stmt = insert(ItemsData).values(
        name=name,
        description=description,
    )
    session.execute(stmt)

def save_db(
    session: Session,
    name: str,
    description: str,
) -> None:
    """Persist item data to db"""

    insert_item(session, name, description)
    session.commit()