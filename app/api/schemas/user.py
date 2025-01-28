from pydantic import BaseModel, EmailStr


class UserCreateResponse(BaseModel):
    jwt_refresh: str
    jwt_access: str


class UserCreateParameters(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogInParameters(BaseModel):
    email: EmailStr
    password: str


class UserLogInResponse(BaseModel):
    jwt_refresh: str
    jwt_access: str


class UserGetMeResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    is_active: bool
