from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    priority: str

    property_id: int
    product_id: int

class TicketCreate(TicketBase):
    created_by_employee_id: int

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to_employee_id: Optional[int] = None
    support_level_id: Optional[int] = None
    resolution_summary: Optional[str] = None

class TicketOut(TicketBase):
    id: int
    status: str
    created_by_employee_id: Optional[int]
    assigned_to_employee_id: Optional[int]
    support_level_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    resolution_summary: Optional[str]

    class Config:
        from_attributes = True
        orm_mode = True
