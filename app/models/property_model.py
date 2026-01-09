from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class PropertyModel(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)

    description = Column(String(500), nullable=False)
    price = Column(Numeric(12,2), nullable=False)
    private_area = Column(Numeric(10,2), nullable=False)
    address = Column(String(255), nullable=False)

    latitude = Column(Numeric(9,6), nullable=True)
    longitude = Column(Numeric(9,6), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("UserModel", backref="properties")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())