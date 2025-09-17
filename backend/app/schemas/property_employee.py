from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class PropertyEmployeeBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    role_in_property: Optional[str] = None

class PropertyEmployeeCreate(PropertyEmployeeBase):
    password: str = Field(..., min_length=6)

class PropertyEmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role_in_property: Optional[str] = None

class PropertyEmployeeOut(PropertyEmployeeBase):
    id: int
    property_id: int

    class Config:
        from_attributes = True
        orm_mode = True
