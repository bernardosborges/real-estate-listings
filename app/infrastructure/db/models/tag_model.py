from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean,  UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class TagModel(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), nullable=False, index=True)
    
    is_active = Column(Boolean, default=True, nullable=False)

    group_id = Column(Integer, ForeignKey("tag_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    group = relationship("TagGroupModel", back_populates="tags")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    property_tags = relationship("PropertyTagModel", back_populates="tag", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("group_id", "slug", name="uq_tag_group_slug"),
    )

    @property
    def group_slug(self) -> str:
        return self.group.slug