from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class HrsEmployeeBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    is_admin: bool = False
    job_title: Optional[str] = None
    product_id: Optional[int] = None

class HrsEmployeeCreate(HrsEmployeeBase):
    password: str = Field(..., min_length=6)

class HrsEmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_admin: Optional[bool] = None
    job_title: Optional[str] = None
    product_id: Optional[int] = None

class HrsEmployeeOut(HrsEmployeeBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
