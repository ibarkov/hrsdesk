from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class DutyRoster(Base):
    __tablename__ = "duty_roster"

    id = Column(Integer, primary_key=True, index=True)
    duty_date = Column(Date, nullable=False)  # дата дежурства
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    level = Column(String(10), nullable=False)  # L1, L2, L3
    hrs_employee_id = Column(Integer, ForeignKey("hrs_employees.id", ondelete="CASCADE"))

    product = relationship("Product")
    employee = relationship("HrsEmployee")
