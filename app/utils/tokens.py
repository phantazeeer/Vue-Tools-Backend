from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.core import settings

secured = OAuth2PasswordBearer(tokenUrl='/api/docs/login')


# Authentification
def create_jwt(payload: dict) -> str:
    """
    This function generates a jwt

    REQUIRED FIELDS:
    iss — (issuer) издатель токена,
    sub — (subject) "тема", назначение токена,описываемый объект,
    aud — (audience) аудитория, получатели токена,
    exp — (expire time) срок действия токена,
    nbf — (not before) срок, до которого токен не действителен,
    iat — (issued at) время создания токена,
    jti — (JWT id) идентификатор токена
    """
    for param in payload.copy().keys():
        if not payload[param]:
            payload.pop(param)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ENCRYPT_ALG)


def get_jwt_payload(token: Annotated[str, Depends(secured)]) -> dict | str:
    """
    This function decodes token
    if token invalid :return: name of error
    else :return: payload(json)
    :param token: str
    """
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ENCRYPT_ALG])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Bearer token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid bearer token")


def create_token(type: str, user_id: int) -> str:
    if type == "access":
        return create_jwt(
            {"type": "access_token",
             "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_LT),
             "sub": str(user_id),
             },
        )
    if type == "refresh":
        return create_jwt(
            {"type": "jwt_refresh",
             "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_LT),
             "sub": str(user_id),
             },
        )
