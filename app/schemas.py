from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# Post schema ----------------


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user_id : int


# User schema ------------------


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserLogin(UserBase):
    pass


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class TokenData(BaseModel):
    id: Optional[int] = None


class Token(BaseModel):
    access_token: str
    token_type: str
