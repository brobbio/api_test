from pydantic import BaseModel
from typing import Optional

#Requests type classes
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

 
class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None