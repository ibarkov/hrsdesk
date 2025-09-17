from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=100)
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True  # pydantic v2; для v1: orm_mode = True
        orm_mode = True         # сохраняем совместимость
