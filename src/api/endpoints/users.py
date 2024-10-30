from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, Path, Depends

from api.auth import auth_backend, fastapi_users
from schemes import (
    UserCreate,
    UserRead,
)
from services import add_avatar
from services.exceptions import InvalidUserId, NotSelf
from core.database import get_async_session
from api.auth import current_user


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
