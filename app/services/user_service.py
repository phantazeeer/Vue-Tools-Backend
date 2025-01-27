from datetime import datetime
from datetime import timezone

from fastapi import HTTPException

from app.db.models import User
from app.repositories import SessionsRepository
from app.repositories import UserRepository
from app.utils import create_jwt
from app.utils import verify_password
from app.utils.tokens import access_token_life_time
from app.utils.tokens import refresh_token_life_time


class UserService:
    @staticmethod
    async def register(username: str, email: str, password: str):
        user_id = await UserRepository.add_user(username=username, email=email, password=password)
        access_token = create_jwt(
            {"type": "jwt_access",
             "exp": datetime.now(timezone.utc) + access_token_life_time,
             "sub": user_id,
             },
        )
        refresh_token = create_jwt(
            {"type": "jwt_refresh",
             "exp": datetime.now(timezone.utc) + refresh_token_life_time,
             "sub": user_id,
             },
        )
        await SessionsRepository.add_token(user_id=user_id, jwt=refresh_token)
        return access_token, refresh_token

    @staticmethod
    async def login(email: str, password: str):
        user = await UserRepository.find_user_by_email(email=email)
        if isinstance(user, User):
            if verify_password(password, user.hashed_password):
                access_token = create_jwt(
                    {"type": "jwt_access",
                     "exp": datetime.now(timezone.utc) + access_token_life_time,
                     "sub": user.id,
                     },
                )
                refresh_token = create_jwt(
                    {"type": "jwt_refresh",
                     "exp": datetime.now(timezone.utc) + refresh_token_life_time,
                     "sub": user.id,
                     },
                )
                await SessionsRepository.add_token(user_id=user.id, jwt=refresh_token)
                return access_token, refresh_token
            else:
                raise HTTPException(400, "Неверный пароль")
        else:
            raise HTTPException(400, "Неверная почта пользователя")
