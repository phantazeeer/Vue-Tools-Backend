from fastapi import HTTPException

from app.db import User
from app.repositories import SessionsRepository
from app.repositories import UserRepository
from app.utils import create_token
from app.utils import verify_password
from app.utils.unitofwork import IUnitOfWork
from app.api.schemas.user import UserGetMeResponse


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def register(self, username: str, email: str, password: str):
        async with self.uow:
            user_id = await self.uow.repo.add_user(username=username, email=email, password=password)
            access_token = create_token("access", user_id)
            refresh_token = create_token("refresh", user_id)
            await self.uow.commit()
            await SessionsRepository.add_token(user_id=user_id, jwt=refresh_token)
            return access_token, refresh_token

    @staticmethod
    async def login(email: str, password: str):
        user = await UserRepository.find_one(email=email)
        if isinstance(user, User):
            if verify_password(password, user.hashed_password):
                access_token = create_token("access", user.id)
                refresh_token = create_token("refresh", user.id)
                await SessionsRepository.add_token(user_id=user.id, jwt=refresh_token)
                return access_token, refresh_token
            else:
                raise HTTPException(400, "Неверный пароль")
        else:
            raise HTTPException(400, "Неверная почта пользователя")

    @staticmethod
    async def get_me(token: str):
        if isinstance(token, dict):
            user = await UserRepository.find_one(id=int(token["sub"]))
            return user
        else:
            raise HTTPException(400, "Не валидный токен")
        

    async def get_one_user(self, id: int) -> UserGetMeResponse:
        async with self.uow:
            user = await self.uow.users.find_one(id=id)
            user_to_return = UserGetMeResponse.model_validate(user)
            await self.uow.commit()
            return user_to_return
