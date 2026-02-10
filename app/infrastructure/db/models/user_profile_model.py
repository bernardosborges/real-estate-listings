import re

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import validates, relationship

from app.core.database import Base
from app.domain.constants.user_profile_constants import (
    PROFILE_NAME_MAX_LENGHT,
    PROFILE_BIO_MAX_LENGHT,
    PROFILE_WORK_PHONE_MAX_LENGHT,
    PROFILE_WORK_CITY_MAX_LENGHT,
    PROFILE_LICENSE_NUMBER_MAX_LENGHT
)

class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    name = Column(String(PROFILE_NAME_MAX_LENGHT), nullable=True)
    bio = Column(String(PROFILE_BIO_MAX_LENGHT), nullable=True)
    work_phone = Column(String(PROFILE_WORK_PHONE_MAX_LENGHT), nullable=True)
    work_city = Column(String(PROFILE_WORK_CITY_MAX_LENGHT), nullable=True)
    license_number = Column(String(PROFILE_LICENSE_NUMBER_MAX_LENGHT), nullable=True)

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
        if not re.fullmatch(pattern, value):
            raise ValueError(
                "Public id must be 4-30 characteres and have only lowercase, numbers, - and ."
            )
        return value