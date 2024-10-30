from http import HTTPStatus
from typing import Annotated, List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Path,
    Query,
    UploadFile,
)

from api.auth import auth_backend, fastapi_users, current_user
from core.database import get_async_session
from schemes import (
    Gendre,
    OrderBy,
    UserCreate,
    UserRead,
)
from services import add_avatar, get_users
from services.exceptions import InvalidUserId, NotSelf


v1_users_router = APIRouter(prefix="/api/clients", tags=["Users"])


v1_users_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
)


v1_users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
)


@v1_users_router.post("/{user_id}/add_image", response_model=UserRead)
async def add_avatar_endpoint(
    user_id=Annotated[int, Path(ge=0)],
    avatar: UploadFile = File(...),
    session=Depends(get_async_session),
    current_user=Depends(current_user),
):
    try:
        user = await add_avatar(session, user_id, current_user, avatar)
    except InvalidUserId:
        return HTTPException(status_code=HTTPStatus.NOT_FOUND)
    except NotSelf:
        return HTTPException(status_code=HTTPStatus.FORBIDDEN)
    return user


@v1_users_router.get("/list", response_model=List[UserRead])
async def get_users_endpoint(
    session=Depends(get_async_session),
    first_name: Optional[str] = Query(alias="Имя", default=None),
    last_name: Optional[str] = Query(alias="Фамилия", default=None),
    gendre: Optional[Gendre] = Query(alias="Пол", default=None),
    order_by: Optional[OrderBy] = Query(
        alias="Сортировка по дате созлания", default=OrderBy.DESCENDING
    ),
):
    return await get_users(session, first_name, last_name, gendre, order_by)
