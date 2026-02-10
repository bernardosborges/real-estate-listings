from pydantic import BaseModel, field_validator
from typing import List
import re
import unicodedata

# -----------------------------------------------
# BASE
# -----------------------------------------------

class PropertyTagBaseSchema(BaseModel):
    property_id: int
    tag_slug: str

    model_config = {
        "title": "PropertyTagBaseSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "property_id": 10,
                "tag_slug": "1-dorm-0-suite",
            }
        }
    }

# -----------------------------------------------
# CREATE
# -----------------------------------------------

class PropertyTagCreateSchema(BaseModel):
    property_id: int
    tags_slug: List[str]


    model_config = {
        "title": "PropertyTagCreateSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "property_id": 10,
                "tags_slug": ["1-dorm-0-suite"],
            }
        }
    }


# -----------------------------------------------
# READ
# -----------------------------------------------

class PropertyTagReadSchema(BaseModel):
    property_id: int
    tags: List[dict]

    model_config = {
        "title": "PropertyTagReadSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "property_id": 10,
                "tags": [{"tag_slug": "1-dorm-0-suite", "tag_name": "1 dormitório (sem suite)", "group_slug": "bedrooms", "group_name": "Dormitórios"}],
            }
        }
    }

# -----------------------------------------------
# UPDATE
# -----------------------------------------------

class PropertyTagUpdateSchema(BaseModel):
    tags_slug: List[str]
    
    model_config = {
        "title": "PropertyTagUpdateSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "tags": ["1-dorm-0-suite"]
            }
        }
    }


# -----------------------------------------------
# DELETE
# -----------------------------------------------

class PropertyTagDeleteSchema(BaseModel):
    property_id: int
    tags_slug: List[str]
    
    model_config = {
        "title": "PropertyTagReadSchema",
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "property_id": 10,
                "tags_slug": ["1-dorm-0-suite"]
            }
        }
    }