from fastapi import APIRouter
from app.api.schemas import UserCreate, UserResponse

router = APIRouter(tags=["work with users"], prefix="/api")


@router.post("/register")
async def register(user: UserCreate) -> UserResponse:
    """Регистрация пользователя"""
    pass


@router.get("/users")
async def get_users() -> UserResponse:
    pass