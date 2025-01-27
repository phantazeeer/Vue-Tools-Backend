from sqlalchemy import select

from app.db.database import async_session_maker as as_fabric
from app.db.models import User
from app.utils import get_password_hash


class UserRepository:

    @staticmethod
    async def add_user(username: str, email: str, password: str) -> int:
        async with as_fabric() as session:
            user = User(
                username=username,
                email=email,
                hashed_password=get_password_hash(password),
            )
            session.add(user)
            await session.commit()
            query = select(User).filter(User.username == username)
            result = await session.execute(query)
            user_id = result.scalars().first().id
        return user_id

    @staticmethod
    def update_user():
        pass

    @staticmethod
    def delete_user():
        pass

    @staticmethod
    async def find_user_by_email(email: str) -> User:
        async with as_fabric() as session:
            query = select(User).filter(User.email == email)
            result = await session.execute(query)
        return result.scalars().first()
