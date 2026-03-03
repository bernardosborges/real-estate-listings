from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from app.models.tag_group_model import TagGroupModel


class TagGroupRepository:

    # -----------------------------------------------
    # CRUD - CREATE
    # -----------------------------------------------

    @staticmethod
    def create(db: Session, obj: TagGroupModel) -> TagGroupModel:
        db.add(obj)
        return obj

    # -----------------------------------------------
    # CRUD - READ
    # -----------------------------------------------

    @staticmethod
    def get_by_id(
        db: Session, id: int, include_deleted: bool = False
    ) -> TagGroupModel | None:
        query = db.query(TagGroupModel).filter(TagGroupModel.id == id)

        if not include_deleted:
            query = query.filter(TagGroupModel.deleted_at.is_(None))
        return query.first()

    @staticmethod
    def get_by_slug(
        db: Session, slug: str, include_deleted: bool = False
    ) -> TagGroupModel | None:
        query = db.query(TagGroupModel).filter(TagGroupModel.slug == slug)

        if not include_deleted:
            query = query.filter(TagGroupModel.deleted_at.is_(None))
        return query.first()

    @staticmethod
    def list_all(db: Session, include_deleted: bool = False) -> List[TagGroupModel]:
        query = db.query(TagGroupModel)

        if not include_deleted:
            query = query.filter(TagGroupModel.deleted_at.is_(None))
        return query.order_by(TagGroupModel.id).all()

    # -----------------------------------------------
    # CRUD - UPDATE
    # -----------------------------------------------

    @staticmethod
    def update(db: Session, id: int, **kwargs) -> TagGroupModel | None:
        db_tag_group = TagGroupRepository.get_by_id(db, id)
        if not db_tag_group:
            return None

        for key, value in kwargs.items():
            setattr(db_tag_group, key, value)
        return db_tag_group

    @staticmethod
    def restore(db: Session, id: int) -> TagGroupModel | None:
        db_tag_group = TagGroupRepository.get_by_id(db, id, include_deleted=True)
        if not db_tag_group:
            return None

        db_tag_group.deleted_at = None
        db_tag_group.is_active = True

        return db_tag_group

    # -----------------------------------------------
    # CRUD - DELETE
    # -----------------------------------------------

    @staticmethod
    def soft_delete(db: Session, id: int) -> TagGroupModel | None:
        db_tag_group = TagGroupRepository.get_by_id(db, id)
        if not db_tag_group:
            return None

        db_tag_group.deleted_at = datetime.now(timezone.utc)
        db_tag_group.is_active = False

        return db_tag_group
