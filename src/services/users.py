import shutil
import tempfile
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from PIL import Image
from geopy.distance import great_circle as GC

from core.config import settings
from core.limits import Limit
from crud import SqlAlchemyRepository
from models import User
from services import exceptions
from utils.emails import send_invitation_by_email


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
    current_user: Optional[User],
    last_name: Optional[str],
    first_name: Optional[str],
    gendre: Optional[str],
    order_by: str,
    distance: Optional[float],
) -> List[User]:
    repo = SqlAlchemyRepository(session)
    users = await repo.get_users_db(last_name, first_name, gendre, order_by)
    if not distance:
        return users
    for i in range(len(users)):
        if not is_in_range(current_user, users[i], distance):
            del users[i]
    return users


async def make_invitation(
    user_id: int,
    session: AsyncSession,
    current_user: User,
) -> str:
    repo = SqlAlchemyRepository(session)
    user = await repo.get_user_db(user_id)
    if user == current_user:
        raise exceptions.NotInviteYourSelf(current_user)
    if (
        await repo.count_user_invitations(current_user)
        > Limit.MAX_INVITATIONS_PER_DAY.value
    ):
        raise exceptions.InvitationsLimitExceeded(current_user)
    favorites = await repo.get_user_invitations(current_user)
    if user in favorites:
        raise exceptions.AlreadyInvitated(current_user)

    repo.create_an_invitation(current_user, user)
    send_invitation_by_email(
        user.email,
        f"{current_user.first_name} {current_user.last_name}",
        current_user.email,
    )
    return user.email


def is_in_range(user_1: User, user_2: User, distance: float) -> bool:
    user_1_coordinates = (user_1.lattitude, user_1.longitude)
    user_2_coordinates = (user_2.lattitude, user_2.longitude)
    return GC(user_1_coordinates, user_2_coordinates).km <= distance
