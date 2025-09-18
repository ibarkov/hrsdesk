from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(30), default="OPEN")   # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    priority = Column(String(20), nullable=False) # P1, P2, P3, P4, R&D

    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    created_by_employee_id = Column(Integer, ForeignKey("property_employees.id", ondelete="SET NULL"))
    assigned_to_employee_id = Column(Integer, ForeignKey("hrs_employees.id", ondelete="SET NULL"))

    support_level_id = Column(Integer, ForeignKey("support_levels.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    resolution_summary = Column(Text, nullable=True)

    # связи (для удобства при join)
    property = relationship("Property")
    product = relationship("Product")
