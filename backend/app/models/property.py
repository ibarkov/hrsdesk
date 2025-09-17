from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    address = Column(Text)
    timezone = Column(String(50))
