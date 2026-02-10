from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import List

from app.api.deps.general_deps import get_db_session, get_authenticated_user, get_superuser
from app.core.config import settings
from app.models.user_model import UserModel
from app.schemas.property_tag_schema import PropertyTagCreateSchema, PropertyTagReadSchema, PropertyTagUpdateSchema, PropertyTagDeleteSchema
from app.services.property_tag_service import PropertyTagService


router = APIRouter(prefix=f"{settings.API_PREFIX}/property-tags", tags=["PropertyTags"])

# -----------------------------------------------
# ENDPOINT - CREATE
# -----------------------------------------------

@router.post(
        "/", 
        response_model=PropertyTagReadSchema,
        summary="Add a tag to a property",
        description="Adds a tag to a property in the database. Requires property id, tag id and group id."
)
def create_property_tag_endpoint(
    payload: PropertyTagCreateSchema,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    return PropertyTagService.add_tags_to_property(db, **payload.model_dump(exclude_unset=True))


# -----------------------------------------------
# ENDPOINT - READ
# -----------------------------------------------

@router.get(
        "/{property_id}", 
        response_model=PropertyTagReadSchema,
        summary="List all tags added to a property",
        description="Retrieves a list of tags added to a specific property."
)
def list_tags_for_property_endpoint(
    property_id: int,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return PropertyTagService.list_tags_for_property(db, property_id)


# -----------------------------------------------
# ENDPOINT - UPDATE
# -----------------------------------------------

@router.patch(
        "/{property_id}", 
        response_model=PropertyTagReadSchema,
        summary="Update a tag added to a property",
        description="Updates a tag added to a property to the database."
)
def update_tag_endpoint(
    property_id: int,
    payload: PropertyTagUpdateSchema,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    if property_id != payload.property_id:
        raise 
    return PropertyTagService.update(db, **payload.model_dump(exclude_unset=True))


@router.patch(
        "/{property_id}/restore", 
        response_model=PropertyTagReadSchema,
        summary="Restore a property tag",
        description="Restores a property tag to the database."
)
def restore_property_tag_group_endpoint(
    property_id: int,
    payload: PropertyTagUpdateSchema,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    return PropertyTagService.restore(db, property_id, **payload.model_dump(exclude_unset=True))


# -----------------------------------------------
# ENDPOINT - DELETE
# -----------------------------------------------

@router.delete(
        "/{property_id}", 
        response_model=PropertyTagReadSchema,
        summary="Delete a tag added to a property",
        description="Delete a tag added to a property from the database."
)
def delete_property_tag_endpoint(
    property_id: int,
    payload: PropertyTagDeleteSchema,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    return PropertyTagService.remove_tags_from_property(db, **payload.model_dump(exclude_unset=True))