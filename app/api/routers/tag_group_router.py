from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import List

from app.api.deps.general_deps import get_db_session, get_authenticated_user, get_superuser
from app.core.config import settings
from app.models.user_model import UserModel
from app.schemas.tag_group_schema import TagGroupCreateSchema, TagGroupReadSchema, TagGroupUpdateSchema
from app.services.tag_group_service import TagGroupService


router = APIRouter(prefix=f"{settings.API_PREFIX}/tag-groups", tags=["TagGroups"])

# -----------------------------------------------
# ENDPOINT - CREATE
# -----------------------------------------------

@router.post(
        "/", 
        response_model=TagGroupReadSchema,
        summary="Create a tag group",
        description="Adds a new tag group to the database. Requires name, slug and if is exclusive (if only one tag can be chosen from the group)."
)
def create_tag_group_endpoint(
    payload: TagGroupCreateSchema,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    return TagGroupService.create(db, **payload.model_dump(exclude_unset=True))

# -----------------------------------------------
# ENDPOINT - READ
# -----------------------------------------------

@router.get(
        "/", 
        response_model=List[TagGroupReadSchema],
        summary="List all tag group",
        description="Retrieves a paginated list of all active tag groups in the database. You can filter or paginate results."
)
def list_tag_group_endpoint(
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return TagGroupService.list_all(db)


@router.get(
        "/{tag_group_slug}", 
        response_model=TagGroupReadSchema,
        summary="Get a tag group",
        description="Retrieves a tag group by its slug."
)
def get_tag_group_by_slug_endpoint(
    tag_group_slug: str,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return TagGroupService.get_by_slug(db, tag_group_slug)


# -----------------------------------------------
# ENDPOINT - UPDATE
# -----------------------------------------------

@router.patch(
        "/{tag_group_slug}", 
        response_model=TagGroupReadSchema,
        summary="Update a tag group",
        description="Updates a tag group to the database."
)
def update_tag_group_endpoint(
    tag_group_slug: str,
    payload: TagGroupUpdateSchema,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    return TagGroupService.update(db, current_slug=tag_group_slug, **payload.model_dump(exclude_unset=True))

@router.patch(
        "/{tag_group_slug}/restore", 
        response_model=TagGroupReadSchema,
        summary="Restore a tag group",
        description="Restores a tag group to the database."
)
def restore_tag_group_endpoint(
    tag_group_slug: str,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    return TagGroupService.restore(db, tag_group_slug)


# -----------------------------------------------
# ENDPOINT - DELETE
# -----------------------------------------------

@router.delete(
        "/{tag_group_id}", 
        response_model=TagGroupReadSchema,
        summary="Delete a tag group",
        description="Delete a tag group from the database."
)
def delete_tag_group_endpoint(
    tag_group_id: int,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_superuser)
):
    return TagGroupService.soft_delete(db, tag_group_id)