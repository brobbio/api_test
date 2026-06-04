from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.db import get_db
from src.schemas.items import ItemCreate, ItemResponse
from src.services import items as item_service

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=List[ItemResponse])
def list_items(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return item_service.get_items(db, limit, offset)

@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    return item_service.create_item(payload, db)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = item_service.get_item(item_id, db)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item