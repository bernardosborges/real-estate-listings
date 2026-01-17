from sqlalchemy.orm import Session
from typing import List

from app.repositories.property_tag_repository import PropertyTagRepository
from app.repositories.tag_repository import TagRepository
from app.models.property_tag_model import PropertyTagModel
from app.models.property_model import PropertyModel
from app.models.tag_model import TagModel
from app.repositories.property_repository import PropertyRepository
from app.core.exceptions.domain_exception import PropertyNotFound, TagNotFound, TagGroupNotFound, PropertyTagNotFound
from app.services.tag_service import TagService
from app.services.tag_group_service import TagGroupService

class PropertyTagService:

# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

    @staticmethod
    def add_tags_to_property(db: Session, property_id: int, tags_slug: List[str]) -> dict:
        PropertyTagService.validate_property_exists(db, property_id)
        
        db_tags_info = []
        created_slugs = []
        for tag_slug in tags_slug:
            db_tag = TagRepository.get_by_slug(db, tag_slug)
            if not db_tag:
                raise TagNotFound(f"Tag {tag_slug} not found")
            
            if db_tag.group and db_tag.group.is_exclusive:
                PropertyTagRepository.hard_delete_exclusive_group(db, property_id, db_tag.group_id)

            existing = PropertyTagRepository.get_by_property_and_tag(db, property_id, db_tag.id)
            if existing:
                continue

            db_tags_info.append({"tag_id": db_tag.id, "group_id": db_tag.group_id})
            created_slugs.append(tag_slug)

        if db_tags_info:
            db_property_tags = PropertyTagRepository.create(db, property_id, db_tags_info)
            for db_property_tag in db_property_tags:
                db.refresh(db_property_tag)

        db.commit()

        return PropertyTagService.list_tags_for_property(db, property_id)

    ###### SHORT VERSION

    # @staticmethod
    # def add_tags_to_property(db: Session, property_id: int, tags_slug: List[str]) -> dict:
    #     PropertyTagService.validate_property_exists(db, property_id)

    #     tags_to_create = PropertyTagService.prepare_property_tags(db, property_id, tags_slug)

    #     if tags_to_create:
    #         PropertyTagService.create_property_tags(db, property_id, tags_slug)

    #     db.commit()
    #     return PropertyTagService.list_tags_for_property(db, property_id)


    # def prepare_property_tags(db: Session, property_id: int, tags_slug: List[str]) -> List[dict]:
    #     db_tags_info = []
    #     for tag_slug in tags_slug:
    #         db_tag = PropertyTagService.get_tag_or_fail(db, tag_slug)
    #         PropertyTagService.apply_exclusive_rule(db, property_id, db_tag)

    #         if PropertyTagService.property_tag_exists(db, property_id, db_tag.id):
    #             continue

    #         db_tags_info.append({"tag_id": db_tag.id, "group_id": db_tag.group_id})

    # def get_tag_or_fail(db, tag_slug):
    #         db_tag = TagRepository.get_by_slug(db, tag_slug)
    #         if not db_tag:
    #             raise TagNotFound(f"Tag {tag_slug} not found")
            
    # def apply_exclusive_rule(db: Session, property_id: int, tag):
    #         if tag.group and tag.group.is_exclusive:
    #             PropertyTagRepository.hard_delete_exclusive_group(db, property_id, tag.group_id)

    # def property_tag_exists(db: Session, property_id: int, tag_id: int) -> bool:
    #     return PropertyTagRepository.get_by_property_and_tag(db, property_id, tag_id) is not None
    
    # def create_property_tags(db: Session, property_id: int, tags_info: List[dict]):
    #     db_property_tags = PropertyTagRepository.create(db, property_id, tags_info)
    #     for db_property_tag in db_property_tags:
    #             db.refresh(db_property_tag)

# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------        
        
    @staticmethod
    def list_tags_for_property(db: Session, property_id: int) -> dict:
        PropertyTagService.validate_property_exists(db, property_id) 

        db_property_tags = PropertyTagRepository.list_all_by_property(db, property_id)

        tags = []
        for db_property_tag in db_property_tags:
            db_tag = TagService.get_by_id(db, db_property_tag.tag_id)
            db_group = TagGroupService.get_by_id(db, db_tag.group_id)
            tags.append({"tag_slug": db_tag.slug, "tag_name": db_tag.name, "group_slug": db_tag.group_slug, "group_name": db_group.name})

        return {"property_id": property_id, "tags": tags}


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------     

    @staticmethod
    def update(
        db: Session,
        property_id: int,
        tag_id: int,
        group_id: int,
        is_active: bool | None = None
    ) -> PropertyTagModel:
        
        db_property_tag = PropertyTagRepository.get_by_property_and_tag(db, property_id, tag_id)
        if not db_property_tag:
            raise PropertyTagNotFound()

        update_data = {}

        if is_active is not None:
            update_data["is_active"] = is_active

        updated_property_tag = PropertyTagRepository.update(db, property_id, tag_id, **update_data)
        db.commit()
        db.refresh(updated_property_tag)

        return updated_property_tag
    

    @staticmethod
    def restore(db: Session, property_id: int, tags_slug: List[str]) -> dict:
        PropertyTagService.validate_property_exists(db, property_id)
        
        db_restored_tags = []
        for tag_slug in tags_slug:
            db_tag = TagService.get_by_slug(db, tag_slug)

            if not db_tag or db_tag.deleted_at is not None:
                #continue
                #poderia dar raise
                raise TagNotFound("AQUIIII")

            if not db_tag.group or db_tag.group.deleted_at is not None:
                #continue
                #poderia dar raise
                raise TagGroupNotFound("OU AQUIIIII")

            db_property_tag = PropertyTagRepository.get_by_property_and_tag(db, property_id, db_tag.id, include_deleted=True)
            if db_property_tag is not None:
                db_restored_tag = PropertyTagRepository.restore(db, property_id, db_tag.id)
                db_restored_tags.append(db_restored_tag)
        
        db.commit()
        for restored_tag in db_restored_tags:
            db.refresh(restored_tag)

        return PropertyTagService.list_tags_for_property(db, property_id)


# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

    @staticmethod
    def remove_tags_from_property(db: Session, property_id: int, tags_slug: List[str]) -> dict:
        db_property = PropertyTagService.validate_property_exists(db, property_id)

        for tag_slug in tags_slug:
            db_tag = TagService.get_by_slug(db, tag_slug)
            db_property_tag = PropertyTagRepository.get_by_property_and_tag(db, property_id, db_tag.id)
            if db_property_tag is not None:
                PropertyTagRepository.hard_delete(db, property_id, db_tag.id)

        db.commit()
        db.refresh(db_property)

        return PropertyTagService.list_tags_for_property(db, property_id)
    
    @staticmethod
    def soft_delete(db: Session, property_id: int, tag_id: int) -> PropertyTagModel:
        db_property_tag = PropertyTagRepository.soft_delete(db, property_id=property_id, tag_id=tag_id)

        db.commit()
        db.refresh(db_property_tag)

        return db_property_tag
    

# -----------------------------------------------
# UTILS
# -----------------------------------------------

    @staticmethod
    def validate_property_exists(db: Session, property_id) -> PropertyModel:
        db_property = PropertyRepository.get_property(db, property_id)
        if not db_property:
            raise PropertyNotFound(f"Property {property_id} not found")
        return db_property