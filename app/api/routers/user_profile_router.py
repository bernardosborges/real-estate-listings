from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.general_deps import get_db_session, get_authenticated_user
from app.core.config import settings
from app.models.user_model import UserModel
from app.schemas.user_profile_schema import UserProfileCreateSchema, UserProfileReadSchema, UserProfileUpdateSchema
from app.services.user_profile_service import UserProfileService
from app.core.exceptions.domain_exception import InvalidPublicId


router = APIRouter(prefix=f"{settings.API_PREFIX}/user-profiles", tags=["UserProfiles"])

# -----------------------------------------------
# ENDPOINT - CREATE
# -----------------------------------------------

@router.post(
        "/", 
        response_model=UserProfileReadSchema,
        summary="Create a user profile for a user",
        description="Create a profile for a user in the database. Requires public_id and user_id."
)
def create_user_profile_endpoint(
    payload: UserProfileCreateSchema,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return UserProfileService.create(db, current_user.id, **payload.model_dump(exclude_unset=True), current_user=current_user)


# -----------------------------------------------
# ENDPOINT - READ
# -----------------------------------------------

@router.get(
        "/me", 
        response_model=UserProfileReadSchema,
        summary="Get a profile for a user",
        description="Retrieves the profile of a user."
)
def get_my_profile_endpoint(
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return UserProfileService.get_by_user_id_or_404(db, current_user.id)


@router.get(
        "/{public_id}", 
        response_model=UserProfileReadSchema,
        summary="Get a profile for a user",
        description="Retrieves the profile of a user."
)
def get_user_profile_endpoint(
    public_id: str,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return UserProfileService.get_by_public_id_or_404(db, public_id)


# -----------------------------------------------
# ENDPOINT - UPDATE
# -----------------------------------------------

@router.patch(
        "/{public_id}", 
        response_model=UserProfileReadSchema,
        summary="Update a user profile",
        description="Updates the profile of a user to the database."
)
def update_user_profile_endpoint(
    public_id: str,
    payload: UserProfileUpdateSchema,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return UserProfileService.update(db, public_id, current_user, **payload.model_dump(exclude_unset=True, mode="json"))


@router.patch(
        "/{public_id}/restore", 
        response_model=UserProfileReadSchema,
        summary="Restore a user profile",
        description="Restores the user profile to the database."
)
def restore_user_profile_endpoint(
    public_id: str,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return UserProfileService.restore(db, public_id, current_user)


# -----------------------------------------------
# ENDPOINT - DELETE
# -----------------------------------------------

@router.delete(
        "/{public_id}", 
        response_model=UserProfileReadSchema,
        summary="Delete the user profile",
        description="Delete the user profile from the database."
)
def delete_user_profile_endpoint(
    public_id: str,
    db: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_authenticated_user)
):
    return UserProfileService.soft_delete(db, public_id, current_user)