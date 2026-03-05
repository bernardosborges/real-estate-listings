from pydantic import BaseModel, field_validator, model_validator
from decimal import Decimal
from typing import cast

from app.api.schemas.address.address_schema import AddressBaseSchema
from app.api.schemas.address.address_schema import AddressUpdateSchema, AddressUpdateResponseSchema
from app.api.exceptions.schema_exceptions import InvalidMapBounds

# from app.schemas.address_schema import AddressCreateSchema, AddressReadSchema
# from app.schemas.tag_schema import TagReadSchema
# from app.schemas.photo_schema import PhotoReadSchema, PhotoThumbnailResponseSchema


# -----------------------------------------------
# PROPERTY CREATE
# -----------------------------------------------


class PropertyCreateRequestSchema(BaseModel):
    description: str
    price: Decimal
    private_area: Decimal
    address: AddressBaseSchema

    model_config = {
        "title": "PropertyCreateRequestSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "description": "Apartamento padrão",
                "price": 250000.00,
                "private_area": 80.00,
                "address": {**cast(dict, AddressBaseSchema.model_config)["json_schema_extra"]["example"]},
            }
        },
    }

    @field_validator("price")
    def price_must_be_positive(cls, v):
        if v is None:
            raise ValueError("Price is required.")
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator("private_area")
    def private_area_must_be_positive(cls, v):
        if v is None:
            raise ValueError("Private area is required.")
        if v <= 0:
            raise ValueError("Private area must be greater than 0")
        return v


class PropertyCreateResponseSchema(BaseModel):
    public_id: str
    profile_public_id: str
    description: str
    price: Decimal
    private_area: Decimal
    address: AddressBaseSchema

    model_config = {
        "title": "PropertyCreateResponseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "public_id": "342321-32321-321-3213",
                "profile_public_id": "my_user",
                "description": "Apartamento padrão",
                "price": 250000.00,
                "private_area": 80.00,
                "address": {**cast(dict, AddressBaseSchema.model_config)["json_schema_extra"]["example"]},
            }
        },
    }


# -----------------------------------------------
# PROPERTY UPDATE
# -----------------------------------------------


class PropertyUpdateRequestSchema(BaseModel):
    description: str | None = None
    price: Decimal | None = None
    private_area: Decimal | None = None
    address: AddressUpdateSchema | None = None

    model_config = {
        "title": "PropertyUpdateRequestSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "description": "Apartamento padrão",
                "price": 250000.00,
                "private_area": 80.00,
                "address": {**cast(dict, AddressBaseSchema.model_config)["json_schema_extra"]["example"]},
            }
        },
    }

    @field_validator("price")
    def price_must_be_positive(cls, v):
        if v is None:
            raise ValueError("Price is required.")
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator("private_area")
    def private_area_must_be_positive(cls, v):
        if v is None:
            raise ValueError("Private area is required.")
        if v <= 0:
            raise ValueError("Private area must be greater than 0")
        return v


class PropertyUpdateResponseSchema(BaseModel):
    public_id: str
    profile_public_id: str
    description: str
    price: Decimal
    private_area: Decimal
    address: AddressUpdateResponseSchema

    model_config = {
        "title": "PropertyUpdateResponseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "public_id": "342321-32321-321-3213",
                "profile_public_id": "my_user",
                "description": "Apartamento padrão",
                "price": 250000.00,
                "private_area": 80.00,
                "address": {**cast(dict, AddressBaseSchema.model_config)["json_schema_extra"]["example"]},
            }
        },
    }


# -----------------------------------------------
# PROPERTY LIST BY PROFILE
# -----------------------------------------------


class PropertyListResponseSchema(BaseModel):
    public_id: str
    profile_public_id: str
    description: str
    price: Decimal
    private_area: Decimal
    address: AddressBaseSchema
    is_active: bool

    model_config = {
        "title": "PropertyListResponseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "public_id": "342321-32321-321-3213",
                "profile_public_id": "my_user",
                "description": "Apartamento padrão",
                "price": 250000.00,
                "private_area": 80.00,
                "address": {**cast(dict, AddressBaseSchema.model_config)["json_schema_extra"]["example"]},
            }
        },
    }


# -----------------------------------------------
# PROPERTY LIST FOR MAP
# -----------------------------------------------


class PropertyListForMapResponseSchema(BaseModel):
    public_id: str
    profile_public_id: str | None
    description: str
    price: Decimal
    private_area: Decimal
    address: AddressBaseSchema
    is_active: bool

    model_config = {
        "title": "PropertyListResponseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "public_id": "342321-32321-321-3213",
                "profile_public_id": "my_user",
                "description": "Apartamento padrão",
                "price": 250000.00,
                "private_area": 80.00,
                "address": {**cast(dict, AddressBaseSchema.model_config)["json_schema_extra"]["example"]},
            }
        },
    }


class PropertyListForMapRequestSchema(BaseModel):
    lat_north: Decimal
    lat_south: Decimal
    lng_east: Decimal
    lng_west: Decimal
    profile_public_id: str | None = None

    model_config = {
        "title": "PropertyListForMapRequestSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "lat_north": "-50.344561",
                "lat_south": "-50.344872",
                "lng_east": "-30.487564",
                "lng_west": "-30.487932",
                "profile_public_id": "test_user",
            }
        },
    }

    @model_validator(mode="after")
    def validate_map_bounds(self):
        if self.lat_north <= self.lat_south:
            raise InvalidMapBounds()
        if self.lng_east <= self.lng_west:
            raise InvalidMapBounds()

        return self


# # -----------------------------------------------
# # BASE
# # -----------------------------------------------

# class PropertyBaseSchema(BaseModel):
#     description: str
#     price: Decimal
#     private_area: Decimal

#     model_config = {
#         "title": "PropertyBaseSchema",
#         "from_attributes": True,
#         "json_schema_extra": {
#             "example": {
#                 "description": "Apartamento padrão",
#                 "price": 250000.00,
#                 "private_area": 80.00,
#             }
#         }
#     }

#     @field_validator('price')
#     def price_must_be_positive(cls, v):
#         if v <= 0:
#             raise ValueError("Price must be greater than 0")
#         return v

#     @field_validator('private_area')
#     def private_area_must_be_positive(cls, v):
#         if v <= 0:
#             raise ValueError("Private area must be greater than 0")
#         return v


# # -----------------------------------------------
# # CREATE
# # -----------------------------------------------

# class PropertyCreateSchema(PropertyBaseSchema):
#     """
#     Schema used to create a new property.
#     Inherits all fields from PropertyBaseSchema
#     """

#     address: AddressCreateSchema

#     model_config = {
#         **PropertyBaseSchema.model_config,
#         "title": "PropertyCreateSchema"
#     }

# # -----------------------------------------------
# # READ
# # -----------------------------------------------

# class PropertyReadSchema(PropertyBaseSchema):
#     public_id: str
#     address: AddressReadSchema
#     tags: list[TagReadSchema] = []
#     photos_enriched: list[PhotoThumbnailResponseSchema] = []

#     model_config = {
#         **PropertyBaseSchema.model_config,
#         "title": "PropertyReadSchema",
#         "json_schema_extra": {
#             "example": {
#                 "public_id": 1,
#                 **PropertyBaseSchema.model_config["json_schema_extra"]["example"],
#                 "address": {
#                     "zip_code": "90000000",
#                     "country": "BR",
#                     "state": "RS",
#                     "city": "Porto Alegre",
#                     "neighborhood": "Centro",
#                     "street": "Rua das Flores",
#                     "number": "80",
#                     "complement": "Apto 301",
#                     "latitude": -30.0346,
#                     "longitude": -51.2177
#                 },
#                 "is_active": True
#             }
#         }
#     }


# class PropertyReadEditSchema(PropertyBaseSchema):
#     public_id: str
#     is_active: bool
#     address: AddressReadSchema
#     tags: list[TagReadSchema] = []
#     photos: list[PhotoReadSchema] = []

#     model_config = {
#         **PropertyBaseSchema.model_config,
#         "title": "PropertyReadSchema",
#         "json_schema_extra": {
#             "example": {
#                 "public_id": 1,
#                 **PropertyBaseSchema.model_config["json_schema_extra"]["example"],
#                 "address": {
#                     "zip_code": "90000000",
#                     "country": "BR",
#                     "state": "RS",
#                     "city": "Porto Alegre",
#                     "neighborhood": "Centro",
#                     "street": "Rua das Flores",
#                     "number": "80",
#                     "complement": "Apto 301",
#                     "latitude": -30.0346,
#                     "longitude": -51.2177
#                 },
#                 "is_active": True
#             }
#         }
#     }

# # -----------------------------------------------
# # UPDATE
# # -----------------------------------------------

# class PropertyUpdateSchema(BaseModel):
#     description: str | None = None
#     price: Decimal | None = None
#     private_area: Decimal | None = None
#     is_active: bool | None = None

#     address: AddressCreateSchema | None = None

#     # -------- VALIDATORS --------
#     @field_validator('price')
#     def price_must_be_positive(cls, v):
#         if v is not None and v <= 0:
#             raise ValueError("Price must be greater than 0")
#         return v

#     @field_validator('private_area')
#     def private_area_must_be_positive(cls, v):
#         if v is not None and v <= 0:
#             raise ValueError("Private area must be greater than 0")
#         return v
