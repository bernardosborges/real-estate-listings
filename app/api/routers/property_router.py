from decimal import Decimal
from fastapi import APIRouter, Depends, Query, status


from app.core.config import settings
from app.api.deps.oauth2 import get_current_user, get_current_user_optional
from app.api.deps.property_deps import (
    get_create_property_usecase,
    get_list_properties_by_profile_usecase,
    get_list_properties_for_map_usecase,
    get_update_property_usecase,
    get_deactivate_property_usecase,
    get_activate_property_usecase,
    get_restore_property_usecase,
    get_soft_delete_property_usecase
)
from app.domain.entities.user import User
# from app.schemas.property_schema import PropertyCreateSchema, PropertyReadSchema, PropertyUpdateSchema
# from app.services.property_service import PropertyService
# from app.infrastructure.storage.s3_service import S3Service


from app.application.usecases.property.create_property import CreatePropertyUseCase
from app.application.usecases.property.update_property import UpdatePropertyUseCase
from app.application.usecases.property.list_properties_by_profile import ListPropertiesByProfileUseCase
from app.application.usecases.property.list_properties_for_map import ListPropertiesForMapUseCase
from app.application.usecases.property.deactivate_property import DeactivatePropertyUseCase
from app.application.usecases.property.activate_property import ActivatePropertyUseCase
from app.application.usecases.property.soft_delete_property import SoftDeletePropertyUseCase
from app.application.usecases.property.restore_property import RestorePropertyUseCase
from app.application.dto.property.create_property_input import CreatePropertyInput
from app.application.dto.property.update_property_input import UpdatePropertyInput
from app.application.dto.property.list_for_map_property_input import ListForMapPropertyInput
from app.application.dto.address.address_input import AddressInput
from app.application.dto.address.update_address_input import UpdateAddressInput
from app.api.schemas.property.property_filters_schema import PropertyFiltersSchema
from app.api.schemas.property.property_schema import (
    PropertyCreateRequestSchema,
    PropertyCreateResponseSchema,
    PropertyUpdateRequestSchema,
    PropertyUpdateResponseSchema,
    PropertyListResponseSchema,
    PropertyListForMapRequestSchema,
    PropertyListForMapResponseSchema
)

router = APIRouter(prefix=f"{settings.API_PREFIX}/properties", tags=["Properties"])


# -----------------------------------------------
# ENDPOINT - CREATE PROPERTY
# -----------------------------------------------

@router.post(
        "/", 
        response_model=PropertyCreateResponseSchema,
        summary="Create a new property",
        description=(
            "Adds a new property to the database. "
            "Requires description, price, private area, address, latitude and longitude."
        )
)
def create_property_endpoint(
    payload: PropertyCreateRequestSchema,
    usecase: CreatePropertyUseCase = Depends(get_create_property_usecase),
    current_user: User = Depends(get_current_user)
):

    address_dto = AddressInput(
        zip_code = payload.address.zip_code,
        country = payload.address.country,
        state = payload.address.state,
        city = payload.address.city,
        neighborhood = payload.address.neighborhood,
        street = payload.address.street,
        number = payload.address.number,
        complement = payload.address.complement,
        latitude = payload.address.latitude,
        longitude = payload.address.longitude,
        confidence = payload.address.confidence,
        provider = payload.address.provider
    )

    usecase_input = CreatePropertyInput(
        description = payload.description,
        price = payload.price,
        private_area = payload.private_area,
        address = address_dto
    )

    result = usecase.execute(usecase_input, current_user)

    return PropertyCreateResponseSchema(
            public_id = result.public_id,
            profile_public_id = result.profile_public_id,
            description = result.description,
            price = result.price,
            private_area = result.private_area,
            address = result.address
        )

# -----------------------------------------------
# ENDPOINT - LIST PROPERTIES BY PROFILE
# -----------------------------------------------

@router.get(
        "/profile/{profile_public_id}",
        response_model=list[PropertyListResponseSchema],
        summary="List all properties from a profile with filters",
        description=(
            "Retrieves a paginated list of all active properties created by a specific profile in the database. "
            "You can filter or paginate results."
        )
)
def list_properties_by_profile_endpoint(
    profile_public_id: str,
    usecase: ListPropertiesByProfileUseCase = Depends(get_list_properties_by_profile_usecase),
    current_user: User | None = Depends(get_current_user_optional),
    filters: PropertyFiltersSchema = Depends()
):

    results = usecase.execute(
        profile_public_id = profile_public_id,
        current_user = current_user,
        limit = filters.limit,
        offset = filters.offset,
        price_min = filters.price_min,
        price_max = filters.price_max
    )

    return [
        PropertyListResponseSchema(
            public_id = result.public_id,
            profile_public_id = result.profile_public_id,
            description = result.description,
            price = result.price,
            private_area = result.private_area,
            address = result.address,
            is_active = result.is_active
        )
        for result in results
    ]


# -----------------------------------------------
# ENDPOINT - LIST PROPERTIES FOR MAP AREA
# -----------------------------------------------

@router.get(
        "/map",
        response_model=list[PropertyListForMapResponseSchema],
        summary="List properties in map viewport",
        description=(
            "Retrieves a paginated list of all active properties in a viewport. "
            "You can filter or paginate results."
        )
)
def list_properties_for_map_endpoint(
    payload: PropertyListForMapRequestSchema,
    usecase: ListPropertiesForMapUseCase = Depends(get_list_properties_for_map_usecase),
    current_user: User | None = Depends(get_current_user_optional),
    filters: PropertyFiltersSchema = Depends()
):

    usecase_input = ListForMapPropertyInput(
        lat_north = payload.lat_north,
        lat_south = payload.lat_south,
        lng_east = payload.lng_east,
        lng_west = payload.lng_west,
        profile_public_id = payload.profile_public_id
    )

    results = usecase.execute(
        data = usecase_input,
        current_user = current_user,
        limit = filters.limit,
        offset = filters.offset,
        price_min = filters.price_min,
        price_max = filters.price_max
    )

    return [
        PropertyListForMapResponseSchema(
            public_id = result.public_id,
            profile_public_id = result.profile_public_id,
            description = result.description,
            price = result.price,
            private_area = result.private_area,
            address = result.address,
            is_active = result.is_active
        )
        for result in results
    ]


# -----------------------------------------------
# ENDPOINT - PROPERTY UPDATE
# -----------------------------------------------

@router.patch(
        "/{property_public_id}",
        response_model=PropertyUpdateResponseSchema,
        summary="Update a property",
        description="Updates a property to the database.",
        status_code=status.HTTP_200_OK
)
def update_property_endpoint(
    property_public_id: str,
    payload: PropertyUpdateRequestSchema,
    usecase: UpdatePropertyUseCase = Depends(get_update_property_usecase),
    current_user: User = Depends(get_current_user)
):

    address_dto = None
    if payload.address:
        address_dto = UpdateAddressInput(
            number = payload.address.number,
            complement = payload.address.complement,
            latitude = payload.address.latitude,
            longitude = payload.address.longitude,
            confidence = payload.address.confidence,
            provider = payload.address.provider
        )

    usecase_input = UpdatePropertyInput(
        description = payload.description,
        price = payload.price,
        private_area = payload.private_area,
        address = address_dto
    )

    result = usecase.execute(property_public_id=property_public_id, data=usecase_input, current_user=current_user)

    return PropertyUpdateResponseSchema(
            public_id = result.public_id,
            profile_public_id = result.profile_public_id,
            description = result.description,
            price = result.price,
            private_area = result.private_area,
            address = result.address
        )


# -----------------------------------------------
# ENDPOINT - PROPERTY DEACTIVATE
# -----------------------------------------------

@router.patch(
        "/{property_public_id}/deactivate",
        summary="Deactivate a property",
        description="Deactivate a from the database.",
        status_code=status.HTTP_204_NO_CONTENT
)
def deactivate_property_endpoint(
    property_public_id: str,
    usecase: DeactivatePropertyUseCase = Depends(get_deactivate_property_usecase),
    current_user: User = Depends(get_current_user)
):
    usecase.execute(property_public_id=property_public_id, current_user=current_user)


# -----------------------------------------------
# ENDPOINT - PROPERTY ACTIVATE
# -----------------------------------------------

@router.patch(
        "/{property_public_id}/activate",
        summary="Activate a property",
        description="Activate a property from the database.",
        status_code=status.HTTP_204_NO_CONTENT
)
def activate_property_endpoint(
    property_public_id: str,
    usecase: ActivatePropertyUseCase = Depends(get_activate_property_usecase),
    current_user: User = Depends(get_current_user)
):
    usecase.execute(property_public_id=property_public_id, current_user=current_user)
    return

# -----------------------------------------------
# ENDPOINT - PROPERTY RESTORE
# -----------------------------------------------

@router.patch(
        "/{property_public_id}/restore",
        summary="Restore a property",
        description="Restore a soft deleted property from the database.",
        status_code=status.HTTP_204_NO_CONTENT
)
def restore_property_endpoint(
    property_public_id: str,
    usecase: RestorePropertyUseCase = Depends(get_restore_property_usecase),
    current_user: User = Depends(get_current_user)
):
    usecase.execute(property_public_id=property_public_id, current_user=current_user)
    return



# -----------------------------------------------
# ENDPOINT - PROPERTY SOFT DELETE
# -----------------------------------------------

@router.delete(
        "/{property_public_id}",
        summary="Delete a property",
        description="Delete a property from the database.",
        status_code=status.HTTP_204_NO_CONTENT
)
def delete_property_endpoint(
    property_public_id: str,
    usecase: SoftDeletePropertyUseCase = Depends(get_soft_delete_property_usecase),
    current_user: User = Depends(get_current_user)
):
    usecase.execute(property_public_id=property_public_id, current_user=current_user)
    return



# # -----------------------------------------------
# # ENDPOINT - LIST PROPERTIES
# # -----------------------------------------------

# @router.get(
#         "/",
#         response_model=list[PropertyReadSchema],
#         summary="List all properties",
#         description=(
#               "Retrieves a paginated list of all active properties in the database. "
#               "You can filter or paginate results"
#         )
# )
# def list_properties_endpoint(
#     db: Session = Depends(get_db_session),
#     price_min: Decimal | None = Query(None, ge=0, description="Minimum price"),
#     price_max: Decimal | None = Query(None, ge=0, description="Maximum price"),
#     limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
#     offset: int = Query(0, ge=0, description="Number of results do skip")
# ):
#     return PropertyService.list_all(db, price_min, price_max, limit, offset)


# # -----------------------------------------------
# # ENDPOINT - LIST PROPERTIES BY USER
# # -----------------------------------------------

# @router.get(
#         "/user/{user_profile_public_id}",
#         response_model=list[PropertyReadSchema],
#         summary="List all properties from a user with filters",
#         description=(
#               "Retrieves a paginated list of all active properties created by a specific user in the database. "
#               "You can filter or paginate results."
#         )
# )
# def list_properties_by_user_endpoint(
#     user_profile_public_id: str,
#     db: Session = Depends(get_db_session),
#     price_min: Decimal | None = Query(None, ge=0, description="Minimum price"),
#     price_max: Decimal | None = Query(None, ge=0, description="Maximum price"),
#     limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
#     offset: int = Query(0, ge=0, description="Number of results do skip")
# ):
#     return PropertyService.list_by_user_profile_public_id(db, user_profile_public_id, price_min, price_max, limit, offset)

# # -----------------------------------------------
# # ENDPOINT - LIST PROPERTIES IN MAP
# # -----------------------------------------------

# @router.get(
#         "/map",
#         response_model=list[PropertyReadSchema],
#         summary="List properties in map viewport",
#         description=(
#         "Retrieves a paginated list of all active properties in a viewport. You can filter or paginate results."
#         )
# )
# def list_properties_for_map_endpoint(
#     db: Session = Depends(get_db_session),
#     min_lat: float = Query(..., ge=-90, le=90, description="Minimum latitude"),
#     max_lat: float = Query(..., ge=-90, le=90, description="Maximum latitude"),
#     min_lng: float = Query(..., ge=-180, le=180, description="Minumum longitude"),
#     max_lng: float = Query(..., ge=-180, le=180, description="Maximum longitude"),
#     price_min: Decimal | None = Query(None, ge=0, description="Minimum price"),
#     price_max: Decimal | None = Query(None, ge=0, description="Maximum price"),
#     limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
#     offset: int = Query(0, ge=0, description="Number of results do skip")
# ):
#     return PropertyService.list_for_map(db, min_lat, max_lat, min_lng, max_lng, price_min, price_max, limit, offset)


# # -----------------------------------------------
# # ENDPOINT - GET A PROPERTY
# # -----------------------------------------------

# @router.get(
#          "/{property_id}",
#         response_model=PropertyReadSchema,
#         summary="Get a property",
#         description="Retrieves a property from the database."
# )
# def get_property_endpoint(
#     property_id: str,
#     db: Session = Depends(get_db_session),
#     storage: S3Service = Depends(get_storage_service)
# ):
#     return PropertyService.get_with_details_by_public_id(db, storage, property_id)


# # -----------------------------------------------
# # ENDPOINT - UPDATE A PROPERTY
# # -----------------------------------------------

# @router.patch(
#         "/{property_id}",
#         response_model=PropertyReadSchema,
#         summary="Update a property",
#         description="Updates a property to the database."
# )
# def update_property_endpoint(
#     property_id: str,
#     property: PropertyUpdateSchema,
#     db: Session = Depends(get_db_session),
#     current_user: UserModel = Depends(get_authenticated_user)
# ):
#     return PropertyService.update(db, property_id, property, current_user)

# # -----------------------------------------------
# # ENDPOINT - RESTORE A PROPERTY
# # -----------------------------------------------

# @router.patch(
#         "/{property_id}/restore",
#         response_model=PropertyReadSchema,
#         summary="Restore a property",
#         description="Restores a property to the database."
# )
# def restore_property_endpoint(
#     property_id: str,
#     db: Session = Depends(get_db_session),
#     current_user: UserModel = Depends(get_authenticated_user)
# ):
#     return PropertyService.restore(db, property_id, current_user)


# # -----------------------------------------------
# # ENDPOINT - DELETE A PROPERTY
# # -----------------------------------------------

# @router.delete(
#         "/{property_id}",
#         response_model=PropertyReadSchema,
#         summary="Delete a property",
#         description="Delete a property from the database."
# )
# def delete_property_endpoint(
#     property_id: str,
#     db: Session = Depends(get_db_session),
#     current_user: UserModel = Depends(get_authenticated_user)
# ):
#     return PropertyService.delete(db, property_id, current_user)
