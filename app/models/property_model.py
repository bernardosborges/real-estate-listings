from sqlalchemy import Column, Integer, String, Numeric, Float
from sqlalchemy.ext.declarative import declarative_base
from app.core.database import Base

class PropertyModel(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    price = Column(Numeric(12,2), nullable=False)
    private_area = Column(Numeric(10,2), nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Numeric(9,6), nullable=True)
    longitude = Column(Numeric(9,6), nullable=True)