from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
import jwt

app = FastAPI()
access_token_life_time = timedelta(hours=1)
refresh_token_life_time = timedelta(days=30)
JWT_SECRET_KEY = "secret"
ENCRYPT_ALG = "HS256"


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
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ENCRYPT_ALG)


def get_jwt_payload(token: str) -> dict | str:
    """
    This function decodes token
    if token invalid :return: name of error
    else :return: payload(json)
    :param token: str
    """
    try:
        decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=ENCRYPT_ALG)
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Bearer token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid bearer token")


def check_jwt(token: Annotated[str, Header()]):
    return get_jwt_payload(token)


@app.get("/", dependencies=[Depends(check_jwt)])
def main():
    return "hello"
