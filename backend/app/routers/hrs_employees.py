from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from app.core.database import get_db
from app.models.hrs_employee import HrsEmployee
from app.schemas.hrs_employee import HrsEmployeeCreate, HrsEmployeeUpdate, HrsEmployeeOut

router = APIRouter(prefix="/api/hrs_employees", tags=["hrs_employees"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/", response_model=List[HrsEmployeeOut])
def list_hrs_employees(db: Session = Depends(get_db)):
    return db.query(HrsEmployee).all()

@router.get("/{employee_id}", response_model=HrsEmployeeOut)
def get_hrs_employee(employee_id: int, db: Session = Depends(get_db)):
    obj = db.query(HrsEmployee).get(employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="HRS employee not found")
    return obj


@router.post("/", response_model=HrsEmployeeOut, status_code=status.HTTP_201_CREATED)
def create_hrs_employee(payload: HrsEmployeeCreate, db: Session = Depends(get_db)):
    exists = db.query(HrsEmployee).filter(HrsEmployee.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = pwd_context.hash(payload.password)
    obj = HrsEmployee(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password_hash=hashed_password,
        phone=payload.phone,
        is_admin=payload.is_admin,
        job_title=payload.job_title,
        product_id=payload.product_id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{employee_id}", response_model=HrsEmployeeOut)
def update_hrs_employee(employee_id: int, payload: HrsEmployeeUpdate, db: Session = Depends(get_db)):
    obj = db.query(HrsEmployee).get(employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hrs_employee(employee_id: int, db: Session = Depends(get_db)):
    obj = db.query(HrsEmployee).get(employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(obj)
    db.commit()
    return None
