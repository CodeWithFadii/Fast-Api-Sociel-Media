from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# User schema ------------------


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserLogin(UserBase):
    pass


class UserData(BaseModel):
    id: int
    email: EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


# JWT Token schema------------------


class TokenData(BaseModel):
    id: Optional[int] = None


class Token(BaseModel):
    access_token: str
    token_type: str


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
    user_id: int
    user_data: UserData
    

class PostOut(BaseModel):
    Post: Post
    likes_count: int
    
    




# Vote schema ----------------


class LikeBase(BaseModel):
    post_id: int


class LikeCreate(LikeBase):
    pass
