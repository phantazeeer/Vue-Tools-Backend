from app.db.database import async_session_maker as as_fabric
from app.db.models.sessions import Session


class SessionsRepository:

    @staticmethod
    async def add_token(user_id: int, jwt: str, useragent: str | None = None):
        async with as_fabric() as session:
            token = Session(user_id=user_id, useragent=useragent, jwt_refresh=jwt)
            session.add(token)
            await session.commit()
