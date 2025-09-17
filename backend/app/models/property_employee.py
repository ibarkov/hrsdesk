from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class PropertyEmployee(Base):
    __tablename__ = "property_employees"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String(20))
    role_in_property = Column(String(50))  # должность (например, IT Manager)

    # связь: сотрудник принадлежит отелю
    property = relationship("Property", backref="employees")
