from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOut

router = APIRouter(prefix="/api/tickets", tags=["tickets"])

@router.get("/", response_model=List[TicketOut])
def list_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    obj = db.query(Ticket).get(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return obj

@router.post("/", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    obj = Ticket(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        property_id=payload.property_id,
        product_id=payload.product_id,
        created_by_employee_id=payload.created_by_employee_id,
        status="OPEN"
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    obj = db.query(Ticket).get(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    obj = db.query(Ticket).get(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(obj)
    db.commit()
    return None
