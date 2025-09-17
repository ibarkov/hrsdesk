from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyOut

router = APIRouter(prefix="/api/properties", tags=["properties"])

@router.get("/", response_model=List[PropertyOut])
def list_properties(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Property).offset(skip).limit(limit).all()

@router.get("/{property_id}", response_model=PropertyOut)
def get_property(property_id: int, db: Session = Depends(get_db)):
    obj = db.query(Property).get(property_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return obj

@router.post("/", response_model=PropertyOut, status_code=status.HTTP_201_CREATED)
def create_property(payload: PropertyCreate, db: Session = Depends(get_db)):
    exists = db.query(Property).filter(Property.code == payload.code).first()
    if exists:
        raise HTTPException(status_code=409, detail="Property code already exists")
    obj = Property(
        code=payload.code,
        name=payload.name,
        address=payload.address,
        timezone=payload.timezone
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{property_id}", response_model=PropertyOut)
def update_property(property_id: int, payload: PropertyUpdate, db: Session = Depends(get_db)):
    obj = db.query(Property).get(property_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Property not found")
    if payload.name is not None:
        obj.name = payload.name
    if payload.address is not None:
        obj.address = payload.address
    if payload.timezone is not None:
        obj.timezone = payload.timezone
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    obj = db.query(Property).get(property_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(obj)
    db.commit()
    return None
