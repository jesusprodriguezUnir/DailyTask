from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    color: str = "#9E9E9E"

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True
