from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemas import UserCreateParameters
from app.api.schemas import UserCreateResponse
from app.api.schemas import UserLogInParameters
from app.api.schemas import UserLogInResponse
from app.api.schemas.user import UserGetMeResponse
from app.services.user_service import UserService
from app.utils import get_jwt_payload
from app.utils.unitofwork import IUnitOfWork, UnitOfWork, uowfabric
from app.repositories.user_repo import UserRepository

router = APIRouter(tags=["work with users"], prefix="/api")

async def get_user_service() -> UserService:
    uow = uowfabric(UserRepository)
    return UserService(uow)


@router.post("/register")
async def register(user: UserCreateParameters, user_service: UserService = Depends(get_user_service)) -> UserCreateResponse:
    """Регистрация пользователя"""
    access_token, refresh_token = await user_service.register(
        username=user.name, password=user.password, email=user.email,
    )
    response = UserCreateResponse(refresh_token=refresh_token, access_token=access_token, token_type="bearer")
    return response


@router.post("/login")
async def login(user: UserLogInParameters) -> UserLogInResponse:
    resp = await UserService.login(user.email, user.password)
    if isinstance(resp, tuple):
        resp = UserLogInResponse(access_token=resp[0], token_type="bearer", refresh_token=resp[1])
        return resp


@router.post("/docs/login")
async def docs_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    resp = await UserService.login(form_data.username, form_data.password)
    if isinstance(resp, tuple):
        resp = UserLogInResponse(access_token=resp[0], token_type="bearer", refresh_token=resp[1])
        return resp


@router.get("/me")
async def me(jwt_access: Annotated[str, Depends(get_jwt_payload)]) -> UserGetMeResponse:
    resp = await UserService.get_me(jwt_access)
    return UserGetMeResponse(user_id=resp.id,
                             name=resp.username,
                             email=resp.email,
                             is_active=resp.is_active,
                             )
