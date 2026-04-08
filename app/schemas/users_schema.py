from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr


class CreateUser(UserBase):
    password: str = Field(min_length=6, max_length=72)


class LoginUser(BaseModel):
    email: EmailStr
    password: str


# ver se tem alguma forma de reaproveitar a base do Create. Criar uma classe genérica?
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6, max_length=72)


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class CreateUserResponse(UserResponse):
    created_at: datetime


class UpdateUserResponse(UserResponse):
    updated_at: datetime
