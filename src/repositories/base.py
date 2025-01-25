from sqlalchemy import select

from database import async_session_maker


class BaseRepository:
    model = None

    def __init__(self, session: async_session_maker):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
