from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.database import get_db
from app.models.ticket import Ticket
from app.models.duty_roster import DutyRoster
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOut
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


# 🔑 Проверка прав доступа
def check_ticket_permissions(ticket: Ticket, current_user: dict):
    role = current_user["role"]

    if role == "admin":
        return True

    if role == "hrs":
        user_product_id = current_user.get("product_id")
        if user_product_id is None:
            raise HTTPException(status_code=403, detail="HRS employee has no assigned product")
        if ticket.product_id != user_product_id:
            raise HTTPException(status_code=403, detail="Not allowed to access this ticket")
        return True

    if role == "property":
        if ticket.property_id != current_user.get("property_id"):
            raise HTTPException(status_code=403, detail="Not allowed to access this ticket")
        return True

    raise HTTPException(status_code=403, detail="Access denied")


@router.get("/", response_model=List[TicketOut])
def list_tickets(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    role = current_user["role"]

    if role == "admin":
        return db.query(Ticket).all()
    elif role == "hrs":
        user_product_id = current_user.get("product_id")
        if not user_product_id:
            return []
        return db.query(Ticket).filter(Ticket.product_id == user_product_id).all()
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
    role = current_user["role"]
    assigned_to_employee_id = None
    property_id = payload.property_id

    if role == "admin":
        # Админ может назначить исполнителя сразу
        assigned_to_employee_id = payload.assigned_to_employee_id
        if not property_id:
            raise HTTPException(status_code=400, detail="Admin must specify property_id")

    elif role == "hrs":
        # HRS сотрудник может создать тикет только по своему продукту
        user_product_id = current_user.get("product_id")
        if payload.product_id != user_product_id:
            raise HTTPException(status_code=403, detail="HRS can only create tickets for their product")
        # Может назначить тикет себе
        assigned_to_employee_id = current_user["sub"]

    elif role == "property":
        # Property сотрудник может создавать тикеты только для своего отеля
        property_id = current_user.get("property_id")
        if not property_id:
            raise HTTPException(status_code=403, detail="Property employee must have property_id")
        # Ищем дежурного L1
        today = date.today()
        duty = (
            db.query(DutyRoster)
            .filter(
                DutyRoster.product_id == payload.product_id,
                DutyRoster.level == "L1",
                DutyRoster.duty_date == today
            )
            .first()
        )
        assigned_to_employee_id = duty.hrs_employee_id if duty else None

    else:
        raise HTTPException(status_code=403, detail="Access denied")

    obj = Ticket(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        property_id=property_id,
        product_id=payload.product_id,
        created_by_employee_id=payload.created_by_employee_id,
        assigned_to_employee_id=assigned_to_employee_id,
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


@router.put("/{ticket_id}/take", response_model=TicketOut)
def take_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Позволяет HRS сотруднику взять тикет себе"""
    if current_user["role"] != "hrs":
        raise HTTPException(status_code=403, detail="Only HRS employees can take tickets")

    obj = db.query(Ticket).get(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")

    check_ticket_permissions(obj, current_user)

    obj.assigned_to_employee_id = current_user["sub"]
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
