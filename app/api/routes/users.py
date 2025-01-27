from fastapi import APIRouter

from app.api.schemas import UserCreateParameters
from app.api.schemas import UserCreateResponse
from app.api.schemas import UserLogInParameters
from app.api.schemas import UserLogInResponse
from app.services.user_service import UserService

router = APIRouter(tags=["work with users"], prefix="/api")


@router.post("/register")
async def register(user: UserCreateParameters) -> UserCreateResponse:
    """Регистрация пользователя"""
    access_token, refresh_token = await UserService.register(
        username=user.name, password=user.password, email=user.email,
    )
    response = UserCreateResponse(jwt_refresh=refresh_token, jwt_access=access_token)
    return response


@router.post("/login")
async def login(user: UserLogInParameters) -> UserLogInResponse:
    resp = await UserService.login(user.email, user.password)
    if isinstance(resp, tuple):
        resp = UserLogInResponse(jwt_access=resp[0], jwt_refresh=resp[1])
        return resp
