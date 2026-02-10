from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from app.models.property_tag_model import PropertyTagModel


class PropertyTagRepository:

# -----------------------------------------------
# CRUD - CREATE
# -----------------------------------------------

    @staticmethod
    def create(db: Session, property_id: int, tags_info: List[dict]) -> List[PropertyTagModel]:
        property_tags = []
        for tag_info in tags_info:
            db_property_tag = PropertyTagModel(property_id=property_id, tag_id=tag_info["tag_id"], group_id=tag_info["group_id"])
            db.add(db_property_tag)
            property_tags.append(db_property_tag)

        return property_tags


# -----------------------------------------------
# CRUD - READ
# -----------------------------------------------

    @staticmethod
    def get_by_property_and_tag(db: Session, property_id: int, tag_id: int, include_deleted: bool = False) -> PropertyTagModel | None:
        query = db.query(PropertyTagModel).filter(PropertyTagModel.property_id == property_id, PropertyTagModel.tag_id == tag_id)

        if not include_deleted:
            query = query.filter(PropertyTagModel.deleted_at.is_(None))
        return query.first()
    
    @staticmethod
    def list_all_by_property(db: Session, property_id: int, include_deleted: bool = False) -> List[PropertyTagModel]:
        query = db.query(PropertyTagModel).filter(PropertyTagModel.property_id == property_id)

        if not include_deleted:
            query = query.filter(PropertyTagModel.deleted_at.is_(None))
        return query.order_by(PropertyTagModel.tag_id).all()
    
    @staticmethod
    def list_all_by_tag(db: Session, tag_id: int, include_deleted: bool = False) -> List[PropertyTagModel]:
        query = db.query(PropertyTagModel).filter(PropertyTagModel.tag_id == tag_id)

        if not include_deleted:
            query = query.filter(PropertyTagModel.deleted_at.is_(None))
        return query.order_by(PropertyTagModel.tag_id).all()
    


# -----------------------------------------------
# CRUD - UPDATE
# -----------------------------------------------

    @staticmethod
    def update(db: Session, property_id: int, tag_id: int, **kwargs) -> PropertyTagModel | None:
        db_property_tag = PropertyTagRepository.get_by_property_and_tag(db, property_id, tag_id)
        if not db_property_tag:
            return None

        for key, value in kwargs.items():
            setattr(db_property_tag, key, value)
        return db_property_tag
    
    @staticmethod
    def restore(db: Session, property_id: int, tag_id: int) -> PropertyTagModel | None:
        db_property_tag = PropertyTagRepository.get_by_property_and_tag(db, property_id=property_id, tag_id=tag_id, include_deleted=True)
        if not db_property_tag:
            return None

        db_property_tag.deleted_at = None

        return db_property_tag

# -----------------------------------------------
# CRUD - DELETE
# -----------------------------------------------

    @staticmethod
    def soft_delete(db: Session, property_id: int, tag_id: int) -> PropertyTagModel | None:
        return PropertyTagRepository.delete(db, property_id, tag_id, hard=False)
    
    @staticmethod
    def hard_delete(db: Session, property_id: int, tag_id: int) -> PropertyTagModel | None:
        return PropertyTagRepository.delete(db, property_id, tag_id, hard=True)

    @staticmethod
    def delete(db: Session, property_id: int, tag_id: int, hard: bool = True) -> PropertyTagModel | None:
        db_property_tag = PropertyTagRepository.get_by_property_and_tag(db, property_id, tag_id)
        if not db_property_tag:
            return None
        
        if hard:
            db.delete(db_property_tag)
        else:
            db_property_tag.deleted_at = datetime.now(timezone.utc)

        return db_property_tag
    
    @staticmethod
    def hard_delete_exclusive_group(db: Session, property_id: int, group_id: int) -> int:
        query = db.query(PropertyTagModel).filter(PropertyTagModel.property_id == property_id, PropertyTagModel.group_id == group_id).delete(synchronize_session=False)
        return query