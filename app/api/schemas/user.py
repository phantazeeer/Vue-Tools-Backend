from pydantic import BaseModel, EmailStr


class UserCreateResponse(BaseModel):
    jwt_refresh: str
    jwt_access: str


class UserCreateParameters(BaseModel):
    name: EmailStr
    email: str
    password: str


class UserLogInParameters(BaseModel):
    email: EmailStr
    password: str


class UserLogInResponse(BaseModel):
    jwt_refresh: str
    jwt_access: str
