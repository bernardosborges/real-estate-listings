from sqlalchemy import Column, Integer, String, Numeric, DateTime, UniqueConstraint, CheckConstraint, Index, ForeignKey, Boolean, text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.enums.photo_enum import PhotoCategoryEnum, PhotoVisibilityEnum, PhotoProcessingStatusEnum


class PhotoModel(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False, index=True)

    file_url = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    category = Column(Enum(PhotoCategoryEnum, name="photo_category_enum", native_enum=False, values_callable=lambda enum_cls: [e.value for e in enum_cls]), nullable=False)
    visibility = Column(Enum(PhotoVisibilityEnum, name="photo_visibility_enum", native_enum=False, values_callable=lambda enum_cls: [e.value for e in enum_cls]), nullable=False)
    processing_status = Column(Enum(PhotoProcessingStatusEnum, name="photo_processing_status_enum", native_enum=False, values_callable=lambda enum_cls: [e.value for e in enum_cls]), nullable=False)
    position = Column(Integer, nullable=False)

    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)
    content_hash = Column(String(64), nullable=True)

    is_cover = Column(Boolean, nullable=False, server_default=text("false"))
    is_active = Column(Boolean, nullable=False, server_default=text("true"))

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    property = relationship("PropertyModel", back_populates="photos")

    __table_args__ = (
        CheckConstraint(
            "position >= 0",
            name="ck_photos_position_positive"
        ),
        Index(
            "ux_photos_one_cover_per_property",
            "property_id",
            unique=True,
            postgresql_where=text("is_cover = true AND deleted_at IS NULL")
        ),
        Index(
            "ux_photos_property_position",
            "property_id",
            "position",
            unique=True,
            postgresql_where=text("deleted_at IS NULL")
        ),
        Index(
            "ix_photos_property_order",
            "property_id",
            "position"
        ),
        Index(
            "ux_photos_content_hash",
            "content_hash",
            unique=True,
            postgresql_where=text("deleted_at IS NULL")
        ),
    )