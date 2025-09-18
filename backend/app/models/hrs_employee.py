from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base

class HrsEmployee(Base):
    __tablename__ = "hrs_employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String(20))
    is_admin = Column(Boolean, default=False)
    job_title = Column(String(100))
    product_id = Column(Integer, ForeignKey("products.id"))  # за какой продукт отвечает
