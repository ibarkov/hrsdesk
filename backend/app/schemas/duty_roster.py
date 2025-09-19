from pydantic import BaseModel, Field
from datetime import date

class DutyRosterBase(BaseModel):
    duty_date: date
    product_id: int
    level: str = Field(..., pattern="^L[123]$")  # только L1/L2/L3

class DutyRosterCreate(DutyRosterBase):
    hrs_employee_id: int

class DutyRosterOut(DutyRosterBase):
    id: int
    hrs_employee_id: int

    class Config:
        from_attributes = True
