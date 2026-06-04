from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.models.item import ItemsData
from src.schemas.items import ItemCreate
from src.db import get_db

def get_items(
        db: Session,
        limit: int = 10,
        offset: int = 0
        ) -> List[ItemsData]:
    """Retrieves every item."""
    return (
        db.query(ItemsData)
        .offset(offset)
        .limit(limit)
        .all()
    )

def get_item(                                                                                                                                                                                                                                                                                                                                                                           
        item_id: int,
        db: Session
        ) -> ItemsData:
    """Retrieves a single element by id"""
    return (
        db.query(ItemsData)
        .filter(ItemsData.id == item_id)
        .first()
    )                                                                                                                                                   

def create_item(payload: ItemCreate, db: Session) -> ItemsData:
    """Create a new item."""
    new_item = ItemsData(name=payload.name, description=payload.description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item