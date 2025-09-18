from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from app.core.database import get_db
from app.models.property_employee import PropertyEmployee
from app.schemas.property_employee import (
    PropertyEmployeeCreate,
    PropertyEmployeeUpdate,
    PropertyEmployeeOut,
)

router = APIRouter(prefix="/api/property_employees", tags=["property_employees"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/", response_model=List[PropertyEmployeeOut])
def list_property_employees(db: Session = Depends(get_db)):
    return db.query(PropertyEmployee).all()

@router.get("/{employee_id}", response_model=PropertyEmployeeOut)
def get_property_employee(employee_id: int, db: Session = Depends(get_db)):
    obj = db.query(PropertyEmployee).get(employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Property employee not found")
    return obj


@router.post("/", response_model=PropertyEmployeeOut, status_code=status.HTTP_201_CREATED)
def create_property_employee(payload: PropertyEmployeeCreate, db: Session = Depends(get_db)):
    exists = db.query(PropertyEmployee).filter(PropertyEmployee.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = pwd_context.hash(payload.password)
    obj = PropertyEmployee(
        property_id=1,  # временно фиксируем, позже сделаем выбор
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password_hash=hashed_password,
        phone=payload.phone,
        role_in_property=payload.role_in_property,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{employee_id}", response_model=PropertyEmployeeOut)
def update_property_employee(employee_id: int, payload: PropertyEmployeeUpdate, db: Session = Depends(get_db)):
    obj = db.query(PropertyEmployee).get(employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_employee(employee_id: int, db: Session = Depends(get_db)):
    obj = db.query(PropertyEmployee).get(employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(obj)
    db.commit()
    return None
