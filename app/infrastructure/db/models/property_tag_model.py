from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class PropertyTagModel(Base):
    __tablename__ = "property_tags"

    property_id = Column(
        Integer,
        ForeignKey("properties.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    tag_id = Column(
        Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    group_id = Column(Integer, ForeignKey("tag_groups.id"), nullable=False, index=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    property = relationship("PropertyModel", back_populates="property_tags")
    tag = relationship("TagModel", back_populates="property_tags")
    group = relationship("TagGroupModel")
