from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone
from typing import List

from app.models.tag_model import TagModel


class TagRepository:

    # -----------------------------------------------
    # CRUD - CREATE
    # -----------------------------------------------

    @staticmethod
    def create(db: Session, obj: TagModel) -> TagModel:
        db.add(obj)
        return obj

    # -----------------------------------------------
    # CRUD - READ
    # -----------------------------------------------

    @staticmethod
    def get_by_id(db: Session, id: int, include_deleted: bool = False) -> TagModel | None:
        query = db.query(TagModel).options(joinedload(TagModel.group)).filter(TagModel.id == id)

        if not include_deleted:
            query = query.filter(TagModel.deleted_at.is_(None))
        return query.first()

    @staticmethod
    def get_by_slug(db: Session, slug: str, include_deleted: bool = False) -> TagModel | None:
        query = db.query(TagModel).options(joinedload(TagModel.group)).filter(TagModel.slug == slug)

        if not include_deleted:
            query = query.filter(TagModel.deleted_at.is_(None))
        return query.first()

    @staticmethod
    def list_by_group(db: Session, group_id: int, include_deleted: bool = False) -> List[TagModel]:
        query = db.query(TagModel).filter(TagModel.group_id == group_id)

        if not include_deleted:
            query = query.filter(TagModel.deleted_at.is_(None))
        return query.order_by(TagModel.id).all()

    @staticmethod
    def list_all(db: Session, include_deleted: bool = False) -> List[TagModel]:
        query = db.query(TagModel)

        if not include_deleted:
            query = query.filter(TagModel.deleted_at.is_(None))
        return query.order_by(TagModel.id).all()

    # -----------------------------------------------
    # CRUD - UPDATE
    # -----------------------------------------------

    @staticmethod
    def update(db: Session, id: int, **kwargs) -> TagModel | None:
        db_tag = TagRepository.get_by_id(db, id)
        if not db_tag:
            return None

        for key, value in kwargs.items():
            setattr(db_tag, key, value)
        return db_tag

    @staticmethod
    def restore(db: Session, id: int) -> TagModel | None:
        db_tag = TagRepository.get_by_id(db, id, include_deleted=True)
        if not db_tag:
            return None

        db_tag.deleted_at = None
        db_tag.is_active = True

        return db_tag

    # -----------------------------------------------
    # CRUD - DELETE
    # -----------------------------------------------

    @staticmethod
    def soft_delete(db: Session, id: int) -> TagModel | None:
        db_tag = TagRepository.get_by_id(db, id)
        if not db_tag:
            return None

        db_tag.deleted_at = datetime.now(timezone.utc)
        db_tag.is_active = False

        return db_tag
