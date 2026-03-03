from sqlalchemy.orm import Session
from typing import List

from app.core.exceptions.domain_exception import TagGroupAlreadyExists, TagGroupNotFound
from app.repositories.tag_group_repository import TagGroupModel
from app.repositories.tag_group_repository import TagGroupRepository
from app.repositories.tag_repository import TagRepository
from app.services.tag_service import TagService


class TagGroupService:

    # -----------------------------------------------
    # CRUD - CREATE
    # -----------------------------------------------

    @staticmethod
    def create(
        db: Session, name: str, slug: str, is_exclusive: bool = False
    ) -> TagGroupModel:
        existing = TagGroupRepository.get_by_slug(db, slug, include_deleted=True)

        if existing:
            raise TagGroupAlreadyExists(f"TagGroup with slug '{slug}' already exists")

        tag_group = TagGroupModel(
            name=name, slug=slug, is_exclusive=is_exclusive, is_active=True
        )

        TagGroupRepository.create(db, tag_group)
        db.commit()
        db.refresh(tag_group)

        return tag_group

    # -----------------------------------------------
    # CRUD - READ
    # -----------------------------------------------

    @staticmethod
    def get_by_id(db: Session, id: int) -> TagGroupModel:
        db_tag_group = TagGroupRepository.get_by_id(db, id)
        if not db_tag_group:
            raise TagGroupNotFound(id)
        return db_tag_group

    @staticmethod
    def get_by_slug(db: Session, slug: str) -> TagGroupModel:
        db_tag_group = TagGroupRepository.get_by_slug(db, slug)
        if not db_tag_group:
            raise TagGroupNotFound(slug)
        return db_tag_group

    @staticmethod
    def list_all(db: Session) -> List[TagGroupModel]:
        return TagGroupRepository.list_all(db)

    # -----------------------------------------------
    # CRUD - UPDATE
    # -----------------------------------------------

    @staticmethod
    def update(
        db: Session,
        current_slug: str,
        name: str | None = None,
        new_slug: str | None = None,
        is_exclusive: bool | None = None,
    ) -> TagGroupModel:

        db_tag_group = TagGroupRepository.get_by_slug(db, current_slug)
        if not db_tag_group:
            raise TagGroupNotFound(current_slug)

        if new_slug is not None and new_slug != current_slug:
            existing = TagGroupRepository.get_by_slug(
                db, new_slug, include_deleted=True
            )
            if existing:
                raise TagGroupAlreadyExists(
                    f"TagGroup with slug '{new_slug}' already exists"
                )

        update_data = {}

        if name is not None:
            update_data["name"] = name
        if new_slug is not None:
            update_data["slug"] = new_slug
        if is_exclusive is not None:
            update_data["is_exclusive"] = is_exclusive

        updated_tag_group = TagGroupRepository.update(
            db, db_tag_group.id, **update_data
        )
        db.commit()
        db.refresh(updated_tag_group)

        return updated_tag_group

    @staticmethod
    def restore(db: Session, slug: str) -> TagGroupModel:
        db_tag_group = TagGroupRepository.get_by_slug(db, slug, include_deleted=True)
        if not db_tag_group:
            raise TagGroupNotFound(slug=slug)

        if db_tag_group.deleted_at is None:
            return db_tag_group

        restored_tag_group = TagGroupRepository.restore(db, db_tag_group.id)
        db.commit()
        db.refresh(restored_tag_group)

        return restored_tag_group

    # -----------------------------------------------
    # CRUD - DELETE
    # -----------------------------------------------

    @staticmethod
    def soft_delete(db: Session, id: int) -> TagGroupModel:
        db_tag_group = TagGroupRepository.soft_delete(db, id)
        if not db_tag_group:
            raise TagGroupNotFound(id)

        for tag in db_tag_group.tags:
            TagService.soft_delete(db, tag.id)

        db.commit()
        db.refresh(db_tag_group)

        return db_tag_group
