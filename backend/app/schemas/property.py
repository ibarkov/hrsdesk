from pydantic import BaseModel, Field
from typing import Optional

class PropertyBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=100)
    address: Optional[str] = None
    timezone: Optional[str] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    timezone: Optional[str] = None

class PropertyOut(PropertyBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
