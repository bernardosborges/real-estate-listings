import re

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import validates, relationship
from app.core.database import Base
from nanoid import generate

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"

def generate_handle():
    return f"{generate(alphabet, size=8).lower()}"

class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False, default=generate_handle)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    name = Column(String(100), nullable=True)
    bio = Column(String(500), nullable=True)
    work_phone = Column(String(20), nullable=True)
    work_city = Column(String(100), nullable=True)
    license_number = Column(String(50), nullable=True)

    profile_picture_url = Column(String(255), nullable=True)
    background_image_url = Column(String(255), nullable=True)

    preferences = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    user = relationship("UserModel", back_populates="user_profile", uselist=False)

    @validates('public_id')
    def validate_public_id(self, key, value):
        pattern = r'^[a-z0-9_.]{4,30}$'
        if not re.match(pattern, value):
            raise ValueError(
                "Public id must be 4-30 characteres and have only lowercase, numbers, - and ."
            )
        return value