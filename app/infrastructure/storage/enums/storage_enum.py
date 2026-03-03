from enum import Enum


class StorageObjectTypeEnum(str, Enum):
    ORIGINAL = "original"
    THUMB = "thumb"
    MEDIUM = "medium"
