from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import List

from app.core.database import get_db
from app.core.config import settings
from app.core.oauth2 import superuser_required, get_current_user
from app.models.user_model import UserModel
from app.schemas.tag_schema import TagCreateSchema, TagReadSchema, TagUpdateSchema
from app.services.tag_service import TagService


router = APIRouter(prefix=f"{settings.API_PREFIX}/tags", tags=["Tags"])

# -----------------------------------------------
# ENDPOINT - CREATE
# -----------------------------------------------

@router.post(
        "/", 
        response_model=TagReadSchema,
        summary="Create a tag",
        description="Adds a new tag to the database. Requires name, slug and group id."
)
def create_tag_endpoint(
    payload: TagCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(superuser_required)
):
    return TagService.create(db, **payload.model_dump(exclude_unset=True))


# -----------------------------------------------
# ENDPOINT - READ
# -----------------------------------------------

@router.get(
        "/", 
        response_model=List[TagReadSchema],
        summary="List all tags of a tag group",
        description="Retrieves a paginated list of all active tags in the database. You can filter or paginate results."
)
def list_tag_endpoint(
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
):
    return TagService.list_all(db)


@router.get(
        "/{tag_slug}", 
        response_model=TagReadSchema,
        summary="Get a tag group",
        description="Retrieves a tag by its slug."
)
def get_tag_by_slug_endpoint(
    tag_slug: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(get_current_user)
):
    return TagService.get_by_slug(db, tag_slug)


# -----------------------------------------------
# ENDPOINT - UPDATE
# -----------------------------------------------

@router.patch(
        "/{tag_slug}", 
        response_model=TagReadSchema,
        summary="Update a tag",
        description="Updates a tag to the database."
)
def update_tag_endpoint(
    tag_slug: str,
    payload: TagUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(superuser_required)
):
    return TagService.update(db, tag_slug, **payload.model_dump(exclude_unset=True))

@router.patch(
        "/{tag_slug}/restore", 
        response_model=TagReadSchema,
        summary="Restore a tag",
        description="Restores a tag to the database."
)
def restore_tag_endpoint(
    tag_slug: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(superuser_required)
):
    return TagService.restore(db, tag_slug)


# -----------------------------------------------
# ENDPOINT - DELETE
# -----------------------------------------------

@router.delete(
        "/{tag_id}", 
        response_model=TagReadSchema,
        summary="Delete a tag",
        description="Delete a tag from the database."
)
def delete_tag_endpoint(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Security(superuser_required)
):
    return TagService.soft_delete(db, tag_id)