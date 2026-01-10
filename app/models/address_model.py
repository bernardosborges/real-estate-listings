from sqlalchemy import Column, Integer, String, Numeric, DateTime, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class AddressModel(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)

    zip_code = Column(String(8), nullable=False, index=True)
    country = Column(String(50), nullable=False, default="BR")
    state = Column(String(2), nullable=False)
    city = Column(String(100), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    street = Column(String(255), nullable=False)
    number = Column(String(20), nullable=False)
    complement = Column(String(100), nullable=True)

    latitude = Column(Numeric(9,6), nullable=True)
    longitude = Column(Numeric(9,6), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    properties = relationship("PropertyModel", back_populates="address")

    __table_args__ = (
        UniqueConstraint("zip_code", "street", "number", "complement", name="uq_address_unique_location"),
        CheckConstraint("latitude BETWEEN -90 AND 90"),
        CheckConstraint("longitude BETWEEN -180 AND 180"),
        Index("ix_address_geo", "latitude", "longitude")    
    )
