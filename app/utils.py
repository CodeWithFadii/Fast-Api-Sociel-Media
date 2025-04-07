from passlib.context import CryptContext

from app import schemas
from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"



def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def add_likes_to_post(post: schemas.Post, likes_count: int):
    return schemas.Post(
        id=post.id,
        title=post.title,
        content=post.content,
        published=post.published,
        created_at=post.created_at,
        user_id=post.user_id,
        user_data=schemas.UserData(id=post.user_data.id, email=post.user_data.email),
        likes_count=likes_count,
    )
