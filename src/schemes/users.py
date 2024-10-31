from datetime import datetime
from enum import Enum, IntEnum
from fastapi_users import schemas


class Gendre(IntEnum):
    MALE = 1
    FEMALE = 2


class OrderBy(str, Enum):
    DESCENDING = "descending"
    ASCENDING = "ascending"


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    sex: Gendre
    url_avatar: str
    registered_at: datetime
    lattitude: float
    longitude: float


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    sex: Gendre
    url_avatar: str
