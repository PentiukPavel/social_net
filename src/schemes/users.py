from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    sex: str
    url_avatar: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    sex: str
    url_avatar: str
