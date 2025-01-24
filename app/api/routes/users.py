from fastapi import APIRouter

router = APIRouter(tags=["work with users"])

@router.get("/users")
async def get_users():
    """Возвращает данные пользователя"""
    return None