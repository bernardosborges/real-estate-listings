from pydantic import BaseModel, field_validator
from typing import cast
import re
import unicodedata

# -----------------------------------------------
# BASE
# -----------------------------------------------


class TagBaseSchema(BaseModel):
    name: str
    slug: str

    model_config = {
        "title": "TagBaseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {"name": "1 Dormitório (1 Suíte)", "slug": "1-dorm-1-suite", "group_slug": "dormitorios"}
        },
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


class TagCreateSchema(TagBaseSchema):

    group_slug: str

    model_config = {
        **TagBaseSchema.model_config,
        "title": "TagCreateSchema",
    }

    @field_validator("group_slug")
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Group slug cannot be empty")
        return v


# -----------------------------------------------
# READ
# -----------------------------------------------


class TagReadSchema(TagBaseSchema):
    group_slug: str

    model_config = {
        **TagBaseSchema.model_config,
        "title": "TagReadSchema",
        "json_schema_extra": {
            "example": {"id": 1, **cast(dict, TagBaseSchema.model_config)["json_schema_extra"]["example"]}
        },
    }


# -----------------------------------------------
# UPDATE
# -----------------------------------------------


class TagUpdateSchema(BaseModel):
    name: str | None = None
    new_slug: str | None = None
    group_slug: str | None = None

    model_config = {
        "title": "TagUpdateSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {"name": "2 dormitórios (1 suite)", "new_slug": "2-dorm-1-suite", "group_slug": "bedrooms"}
        },
    }
