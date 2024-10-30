from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


class SqlAlchemyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_db(self, user_id):
        query = select(User).filter(User.id == int(user_id))
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
