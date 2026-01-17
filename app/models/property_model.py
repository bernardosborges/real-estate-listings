from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class PropertyModel(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    address_id = Column(Integer, ForeignKey("addresses.id", name="fk_properties_address_id", ondelete="RESTRICT"), nullable=False, index=True) 

    description = Column(String(500), nullable=False)
    price = Column(Numeric(12,2), nullable=False)
    private_area = Column(Numeric(10,2), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    user = relationship("UserModel", backref="properties")
    address = relationship("AddressModel", back_populates="properties")
    photos = relationship("PhotoModel", back_populates="property", cascade="all, delete-orphan")