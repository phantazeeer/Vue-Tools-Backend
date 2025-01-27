from pydantic import BaseModel


class UserCreateResponse(BaseModel):
    jwt_refresh: str
    jwt_access: str


class UserCreateParameters(BaseModel):
    name: str
    email: str
    password: str


class UserLogInParameters(BaseModel):
    email: str
    password: str


class UserLogInResponse(BaseModel):
    jwt_refresh: str
    jwt_access: str
