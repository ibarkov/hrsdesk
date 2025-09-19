from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.database import get_db
from app.models.duty_roster import DutyRoster
from app.schemas.duty_roster import DutyRosterCreate, DutyRosterOut
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/duty_roster", tags=["duty_roster"])


@router.get("/", response_model=List[DutyRosterOut])
def list_duty_roster(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view duty roster")
    return db.query(DutyRoster).all()


@router.post("/", response_model=DutyRosterOut, status_code=status.HTTP_201_CREATED)
def create_duty_roster(payload: DutyRosterCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can assign duty roster")

    obj = DutyRoster(
        duty_date=payload.duty_date,
        product_id=payload.product_id,
        level=payload.level,
        hrs_employee_id=payload.hrs_employee_id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/today/{product_id}/{level}", response_model=DutyRosterOut)
def get_today_duty(product_id: int, level: str, db: Session = Depends(get_db)):
    today = date.today()
    obj = (
        db.query(DutyRoster)
        .filter(DutyRoster.product_id == product_id, DutyRoster.level == level, DutyRoster.duty_date == today)
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="No duty found for today")
    return obj
