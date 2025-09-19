from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOut
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


# 🔑 Проверка прав доступа
def check_ticket_permissions(ticket: Ticket, current_user: dict):
    role = current_user["role"]

    if role == "admin":
        return True

    if role == "hrs":
        # HRS-сотрудник может видеть тикеты по своим продуктам (упростим: пока все)
        return True

    if role == "property":
        # сотрудник отеля видит только тикеты своего отеля
        if ticket.property_id != current_user.get("property_id"):
            raise HTTPException(status_code=403, detail="Not allowed to access this ticket")
        return True

    raise HTTPException(status_code=403, detail="Access denied")


@router.get("/", response_model=List[TicketOut])
def list_tickets(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    role = current_user["role"]

    if role in {"admin", "hrs"}:
        return db.query(Ticket).all()
    elif role == "property":
        return db.query(Ticket).filter(Ticket.property_id == current_user.get("property_id")).all()
    else:
        raise HTTPException(status_code=403, detail="Access denied")


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    obj = db.query(Ticket).get(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")
    check_ticket_permissions(obj, current_user)
    return obj


@router.post("/", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "property":
        raise HTTPException(status_code=403, detail="Only property employees can create tickets")

    obj = Ticket(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        property_id=current_user.get("property_id"),
        product_id=payload.product_id,
        created_by_employee_id=payload.created_by_employee_id,
        status="OPEN"
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    obj = db.query(Ticket).get(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")

    check_ticket_permissions(obj, current_user)

    # 🔑 Проверка допустимых статусов
    allowed_statuses_hrs = {"OPEN", "IN_PROGRESS", "PENDING", "ON_HOLD", "SOLVED", "CLOSED"}
    allowed_statuses_property = {"OPEN", "PENDING", "SOLVED", "CLOSED"}

    if payload.status:
        if current_user["role"] == "hrs" and payload.status not in allowed_statuses_hrs:
            raise HTTPException(status_code=400, detail=f"Invalid status for HRS: {payload.status}")
        if current_user["role"] == "property" and payload.status not in allowed_statuses_property:
            raise HTTPException(status_code=400, detail=f"Invalid status for Property Employee: {payload.status}")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete tickets")

    obj = db.query(Ticket).get(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(obj)
    db.commit()
    return None
