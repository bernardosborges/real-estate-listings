from sqlalchemy.orm import Session
from typing import List

from app.core.exceptions.domain_exception import (
    TagAlreadyExists,
    TagNotFound,
    TagGroupNotFound,
)
from app.models.tag_model import TagModel
from app.repositories.tag_repository import TagRepository
from app.repositories.tag_group_repository import TagGroupRepository
from app.repositories.property_tag_repository import PropertyTagRepository


class TagService:

    # -----------------------------------------------
    # CRUD - CREATE
    # -----------------------------------------------

    @staticmethod
    def create(db: Session, name: str, slug: str, group_slug: str) -> TagModel:
        existing = TagRepository.get_by_slug(db, slug, include_deleted=True)
        if existing:
            raise TagAlreadyExists(f"Tag with slug '{slug}' already exists")

        existing_group = TagGroupRepository.get_by_slug(db, group_slug)
        if not existing_group:
            raise TagGroupNotFound(group_slug)

        tag = TagModel(name=name, slug=slug, group_id=existing_group.id, is_active=True)

        TagRepository.create(db, tag)
        db.commit()
        db.refresh(tag)

        return tag

    # -----------------------------------------------
    # CRUD - READ
    # -----------------------------------------------

    @staticmethod
    def get_by_id(db: Session, id: int) -> TagModel:
        db_tag = TagRepository.get_by_id(db, id)
        if not db_tag:
            raise TagNotFound(id)
        return db_tag

    @staticmethod
    def get_by_slug(db: Session, slug: str, include_delete: bool = False) -> TagModel:
        db_tag = TagRepository.get_by_slug(db, slug, include_delete)
        if not db_tag:
            raise TagNotFound(slug)
        return db_tag

    @staticmethod
    def list_all(db: Session) -> List[TagModel]:
        return TagRepository.list_all(db)

    # -----------------------------------------------
    # CRUD - UPDATE
    # -----------------------------------------------

    @staticmethod
    def update(
        db: Session,
        current_slug: str,
        name: str | None = None,
        new_slug: str | None = None,
        group_slug: str | None = None,
    ) -> TagModel:

        db_tag = TagRepository.get_by_slug(db, current_slug)
        if not db_tag:
            raise TagNotFound(current_slug)

        if new_slug is not None and new_slug != current_slug:
            existing = TagRepository.get_by_slug(db, new_slug, include_deleted=True)
            if existing:
                raise TagAlreadyExists(f"TagGroup with slug '{new_slug}' already exists")

        update_data = {}

        if name is not None:
            update_data["name"] = name
        if new_slug is not None:
            update_data["slug"] = new_slug
        if group_slug is not None:
            existing_group = TagGroupRepository.get_by_slug(db, group_slug)
            if not existing_group:
                raise TagGroupNotFound(group_slug)
            update_data["group_id"] = existing_group.id

        updated_tag = TagRepository.update(db, db_tag.id, **update_data)
        db.commit()
        db.refresh(updated_tag)

        return updated_tag

    @staticmethod
    def restore(db: Session, slug: str) -> TagModel:
        db_tag = TagRepository.get_by_slug(db, slug, include_deleted=True)
        if not db_tag:
            raise TagNotFound(slug=slug)

        if db_tag.deleted_at is None:
            return db_tag

        db_group = TagGroupRepository.get_by_slug(db, db_tag.group_slug, include_deleted=True)
        if not db_group or db_group.deleted_at is not None:
            raise TagGroupNotFound(slug=db_tag.group_slug)

        restored_tag = TagRepository.restore(db, db_tag.id)
        db.commit()
        db.refresh(restored_tag)

        return restored_tag

    # -----------------------------------------------
    # CRUD - DELETE
    # -----------------------------------------------

    @staticmethod
    def soft_delete(db: Session, id: int) -> TagModel:
        db_tag = TagRepository.soft_delete(db, id)
        if not db_tag:
            raise TagNotFound(id)

        db_property_tags = PropertyTagRepository.list_all_by_tag(db, id)
        from app.services.property_tag_service import PropertyTagService

        for property in db_property_tags:
            PropertyTagService.soft_delete(db, property.property_id, property.tag_id)

        db.commit()
        db.refresh(db_tag)

        return db_tag
