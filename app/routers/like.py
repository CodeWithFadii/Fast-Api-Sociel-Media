from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from ..oauth2 import get_current_user

router = APIRouter(prefix="/like", tags=["Likes"])


@router.post("/")
def like_unlike_post(
    like: schemas.LikeCreate,
    db: Session = Depends(database.get_db),
    user_data: int = Depends(get_current_user),
):
    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user already liked the post
    existing_like = (
        db.query(models.Like)
        .filter(
            models.Like.user_id == user_data.id, models.Like.post_id == like.post_id
        )
        .first()
    )

    if existing_like:
        # If already liked, remove the like (unlike)
        db.delete(existing_like)
        db.commit()
        return {"message": "Like removed"}

    # Otherwise, create a new like
    new_like = models.Like(user_id=user_data.id, post_id=like.post_id)
    db.add(new_like)
    db.commit()
    return {"message": "Post liked"}
