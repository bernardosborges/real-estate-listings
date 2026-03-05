import uuid

from datetime import datetime
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    CheckConstraint,
    Index,
    ForeignKey,
    Boolean,
    text,
    Enum,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.domain.enums.photo_enum import (
    PhotoCategoryEnum,
    PhotoVisibilityEnum,
    PhotoProcessingStatusEnum,
)


class PhotoModel(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    public_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    property_id: Mapped[int] = mapped_column(Integer, ForeignKey("properties.id"), nullable=False, index=True)

    storage_key: Mapped[str] = mapped_column(String, nullable=True)
    file_url: Mapped[str] = mapped_column(String, nullable=True)
    thumbnail_url: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[PhotoCategoryEnum] = mapped_column(
        Enum(
            PhotoCategoryEnum,
            name="photo_category_enum",
            native_enum=False,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    visibility: Mapped[PhotoVisibilityEnum] = mapped_column(
        Enum(
            PhotoVisibilityEnum,
            name="photo_visibility_enum",
            native_enum=False,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    processing_status: Mapped[PhotoProcessingStatusEnum] = mapped_column(
        Enum(
            PhotoProcessingStatusEnum,
            name="photo_processing_status_enum",
            native_enum=False,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    width: Mapped[int] = mapped_column(Integer, nullable=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    file_size: Mapped[int] = mapped_column(Integer, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=True)

    is_cover: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    property = relationship("PropertyModel", back_populates="photos_all")

    __table_args__ = (
        CheckConstraint("position >= 0", name="ck_photos_position_positive"),
        Index(
            "ux_photos_one_cover_per_property",
            "property_id",
            unique=True,
            postgresql_where=text("is_cover = true AND deleted_at IS NULL"),
        ),
        Index(
            "ux_photos_property_position",
            "property_id",
            "position",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
        Index("ix_photos_property_order", "property_id", "position"),
        Index(
            "ux_photos_content_hash",
            "content_hash",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )
