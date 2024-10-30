import shutil
from typing import Optional

from fastapi import Depends, Request, File, UploadFile
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions,
    models,
    schemas,
)

from core.config import settings
from models import User
from api.utils import get_user_db
from core.database import get_async_session


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.AUTH_SECRET
    verification_token_secret = settings.AUTH_SECRET

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        pass

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        pass

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(
            f"Verification requested for user {user.id}."
            f"Verification token: {token}"
        )

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
        avatar: UploadFile = File(...),
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)
        session = get_async_session()
        with open(settings.STORAGE_LOCATION + avatar.filename, "wb") as image:
            shutil.copyfileobj(avatar.file, image)
        created_user.url_avatar = str(
            settings.STORAGE_LOCATION + avatar.filename
        )
        await session.commit()
        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
