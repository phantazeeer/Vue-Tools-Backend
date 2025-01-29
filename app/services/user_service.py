from fastapi import HTTPException

from app.db import User
from app.repositories import SessionsRepository
from app.repositories import UserRepository
from app.utils import create_token, get_jwt_payload
from app.utils import verify_password


class UserService:
    @staticmethod
    async def register(username: str, email: str, password: str):
        user_id = await UserRepository.add_user(username=username, email=email, password=password)
        access_token = create_token("access", user_id)
        refresh_token = create_token("refresh", user_id)
        await SessionsRepository.add_token(user_id=user_id, jwt=refresh_token)
        return access_token, refresh_token

    @staticmethod
    async def login(email: str, password: str):
        user = await UserRepository.find_user_by_email(email=email)
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
        token = get_jwt_payload(token)
        if isinstance(token, dict):
            user = await UserRepository.find_user_by_id(int(token["sub"]))
            return user
        else:
            raise HTTPException(400, "Не валидный токен")
