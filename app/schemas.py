from datetime import datetime
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


# User schema ------------------


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass
