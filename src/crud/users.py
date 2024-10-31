from datetime import datetime
from typing import List, Optional

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Favorite, User
from schemes import OrderBy


class SqlAlchemyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_db(self, user_id):
        query = select(User).filter(User.id == int(user_id))
        user = await self.session.execute(query)
        return user.scalar_one_or_none()

    async def get_users_db(
        self,
        last_name: Optional[str],
        first_name: Optional[str],
        gendre: Optional[str],
        order_by: str,
    ) -> Optional[List[User]]:
        query = select(User)
        if last_name:
            query = query.filter(User.last_name.contains(last_name))
        if first_name:
            query = query.filter(User.last_name.contains(first_name))
        if gendre:
            query = query.filter(User.sex == gendre)
        if order_by:
            if order_by == OrderBy.DESCENDING:
                query = query.order_by(desc(User.registered_at))
            else:
                query = query.order_by(asc(User.registered_at))

        users = await self.session.execute(query)
        return users.scalars().all()

    async def get_user_invitations(self, user: User):
        favorites = await self.session.execute(user.favorites)
        return favorites.scalars().all()

    async def count_user_invitations(self, user: User) -> int:
        query = select(Favorite).filter(
            Favorite.subscriber_id == user.id,
            func.DATE(Favorite.registered_at) == datetime.now().date(),
        )
        invtitations = await self.session.execute(query)
        return len(invtitations.scalars().all())

    async def create_an_invitation(self, user: User, favorite: User) -> None:
        user.favorites.append(favorite)
        self.session.commit()
