from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

from app.domain.constants.property_constants import (
    PROPERTY_DESCRIPTION_MAX_LENGHT,
    PROPERTY_PUBLIC_ID_SIZE,
)


class PropertyModel(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    public_id = Column(
        String(PROPERTY_PUBLIC_ID_SIZE), unique=True, nullable=False, index=True
    )

    # user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    profile_id = Column(
        Integer,
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    address_id = Column(
        Integer,
        ForeignKey(
            "addresses.id", name="fk_properties_address_id", ondelete="RESTRICT"
        ),
        nullable=False,
        index=True,
    )

    description = Column(String(PROPERTY_DESCRIPTION_MAX_LENGHT), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    private_area = Column(Numeric(10, 2), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    profile = relationship("UserProfileModel", backref="properties")
    # user = relationship("UserModel", backref="properties")
    address = relationship("AddressModel", back_populates="properties")
    photos = relationship(
        "PhotoModel",
        back_populates="property",
        cascade="all, delete-orphan",
        lazy="selectin",
        primaryjoin="and_(PropertyModel.id == PhotoModel.property_id, PhotoModel.deleted_at.is_(None), PhotoModel.visibility == 'public', PhotoModel.is_active == True, PhotoModel.processing_status == 'ready')",
        order_by="PhotoModel.position",
    )
    photos_all = relationship(
        "PhotoModel",
        back_populates="property",
        cascade="all, delete-orphan",
        lazy="selectin",
        primaryjoin="and_(PropertyModel.id == PhotoModel.property_id, PhotoModel.deleted_at.is_(None), PhotoModel.processing_status == 'ready')",
        order_by="PhotoModel.position",
        viewonly=True,
        overlaps="photos",
    )
    property_tags = relationship(
        "PropertyTagModel", back_populates="property", cascade="all, delete-orphan"
    )
    tags = relationship(
        "TagModel", secondary="property_tags", viewonly=True, lazy="selectin"
    )
