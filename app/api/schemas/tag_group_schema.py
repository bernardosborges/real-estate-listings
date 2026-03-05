from pydantic import BaseModel, field_validator
from typing import cast
import re
import unicodedata

# -----------------------------------------------
# BASE
# -----------------------------------------------


class TagGroupBaseSchema(BaseModel):
    name: str
    slug: str
    is_exclusive: bool = False

    model_config = {
        "title": "TagGroupBaseSchema",
        "from_attributes": True,
        "json_schema_extra": {"example": {"name": "Dormitórios", "slug": "bedrooms", "is_exclusive": True}},
    }

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        if len(v) > 100:
            raise ValueError("Name too long")
        return v

    @field_validator("slug", mode="before")
    def normalize_slug(cls, v: str) -> str:
        if not v:
            raise ValueError("Slug cannot be empty")
        v = v.lower()
        v = v.strip()
        v = unicodedata.normalize("NFKD", v).encode("ascii", "ignore").decode("ascii")
        v = re.sub(r"\s+", "-", v)
        v = re.sub(r"[^a-z0-9\-]", "", v)
        v = re.sub(r"-{2,}", "-", v)
        return v


# -----------------------------------------------
# CREATE
# -----------------------------------------------


class TagGroupCreateSchema(TagGroupBaseSchema):

    model_config = {**TagGroupBaseSchema.model_config, "title": "TagGroupCreate"}


# -----------------------------------------------
# READ
# -----------------------------------------------


class TagGroupReadSchema(TagGroupBaseSchema):
    id: int

    model_config = {
        **TagGroupBaseSchema.model_config,
        "title": "TagGroupRead",
        "json_schema_extra": {
            "example": {"id": 1, **cast(dict, TagGroupBaseSchema.model_config)["json_schema_extra"]["example"]}
        },
    }


# -----------------------------------------------
# UPDATE
# -----------------------------------------------


class TagGroupUpdateSchema(BaseModel):
    name: str | None = None
    new_slug: str | None = None
    is_exclusive: bool | None = None

    model_config = {
        "title": "TagGroupUpdateSchema",
        "from_attributes": True,
        "json_schema_extra": {"example": {"name": "Dormitórios", "new_slug": "bedrooms", "is_exclusive": True}},
    }

    @field_validator("name")
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty")
            if len(v) > 100:
                raise ValueError("Name too long")
        return v

    @field_validator("new_slug", mode="before")
    def normalize_slug(cls, v: str | None) -> str | None:
        if v is not None:
            if not v:
                raise ValueError("Slug cannot be empty")
            v = v.lower()
            v = v.strip()
            v = unicodedata.normalize("NFKD", v).encode("ascii", "ignore").decode("ascii")
            v = re.sub(r"\s+", "-", v)
            v = re.sub(r"[^a-z0-9\-]", "", v)
            v = re.sub(r"-{2,}", "-", v)
        return v
