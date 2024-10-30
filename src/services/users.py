import shutil
import tempfile
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from PIL import Image

from core.config import settings
from crud import SqlAlchemyRepository
from services import exceptions
from models import User


async def get_user(
    session: AsyncSession, user_id: int, current_user: User
) -> User:
    repo = SqlAlchemyRepository(session)
    user = await repo.get_user_db(user_id)
    if user is None:
        raise exceptions.InvalidUserId(user_id)
    if user.id != current_user.id:
        raise exceptions.NotSelf(current_user)

    return user


async def add_avatar(
    session: AsyncSession, user_id: int, current_user: User, avatar
) -> User:
    user = await get_user(session, user_id, current_user)
    with open(settings.STORAGE_LOCATION + avatar.filename, "wb+") as avtr_img:
        shutil.copyfileobj(avatar.file, avtr_img)
    user.url_avatar = str(settings.STORAGE_LOCATION + avatar.filename)
    await session.commit()
    treat_image(user.url_avatar)
    return user


def treat_image(avatar):
    small_gif = (
        b"\x47\x49\x46\x38\x39\x61\x02\x00"
        b"\x01\x00\x80\x00\x00\x00\x00\x00"
        b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
        b"\x00\x00\x00\x2C\x00\x00\x00\x00"
        b"\x02\x00\x01\x00\x00\x02\x02\x0C"
        b"\x0A\x00\x3B"
    )
    temp = tempfile.TemporaryFile()
    temp.write(small_gif)
    im1 = Image.open(avatar)
    im2 = Image.open(temp)
    im1.paste(im2)
    im1.save(avatar, quality=95)

    im1.close()
    im2.close()


async def get_users(
    session: AsyncSession,
    last_name: str,
    first_name: str,
    gendre: int,
    order_by: str,
) -> List[User]:
    repo = SqlAlchemyRepository(session)
    return await repo.get_users_db(last_name, first_name, gendre, order_by)
