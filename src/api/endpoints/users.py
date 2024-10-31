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
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import (
    auth_backend,
    fastapi_users,
    optional_current_user,
    current_user,
)
from core.choices import APIMessages
from core.database import get_async_session
from models import User
from schemes import (
    Gendre,
    OrderBy,
    UserCreate,
    UserRead,
)
from services import add_avatar, get_users, make_invitation
from services.exceptions import (
    AlreadyInvitated,
    InvalidUserId,
    InvitationsLimitExceeded,
    NotSelf,
    NotInviteYourSelf,
)


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
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
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
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(optional_current_user),
    first_name: Optional[str] = Query(alias="Имя", default=None),
    last_name: Optional[str] = Query(alias="Фамилия", default=None),
    gendre: Optional[Gendre] = Query(alias="Пол", default=None),
    order_by: Optional[OrderBy] = Query(
        alias="Сортировка по дате создания", default=OrderBy.DESCENDING
    ),
    distance: Optional[float] = Query(alias="Радиус", default=None),
):
    return await get_users(
        session,
        current_user,
        first_name,
        last_name,
        gendre,
        order_by,
        distance,
    )


@v1_users_router.post("clients/{user_id}/match")
async def make_invitation_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    try:
        email = await make_invitation(user_id, session, current_user)
        return {"status": HTTPStatus.CREATED, "email": email}
    except InvalidUserId:
        return HTTPException(status_code=HTTPStatus.NOT_FOUND)
    except NotInviteYourSelf:
        return HTTPException(
            status_code=HTTPStatus.LOCKED,
            detail=APIMessages.NOT_INVITE_YOURSELF.value,
        )
    except AlreadyInvitated:
        return HTTPException(
            status_code=HTTPStatus.LOCKED,
            detail=APIMessages.ALREADY_INVITATED.value,
        )
    except InvitationsLimitExceeded:
        return HTTPException(
            status_code=HTTPStatus.LOCKED,
            detail=APIMessages.INVITATION_LIMIT_EXCEEDED.value,
        )
