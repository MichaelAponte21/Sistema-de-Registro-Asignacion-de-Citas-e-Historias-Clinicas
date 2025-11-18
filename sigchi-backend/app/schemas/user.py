# app/schemas/user.py
from pydantic import BaseModel, EmailStr, constr
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    role_id: int


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=72)
    role_id: int


class UserResponse(UserBase):
    id: int

    class Config:
        # Pydantic v2: reemplaza orm_mode=True
        from_attributes = True
