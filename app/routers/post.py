from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


# Getting all posts
@router.get("/", response_model=list[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    user_data: schemas.User = Depends(oauth2.get_current_user),
    limit: int = Query(10, ge=1, le=100),  # Users can set limit (1-100), default 10
    skip: int = Query(0, ge=0),  # Users can set skip (default 0)
):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts


# Creating a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_data: schemas.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(user_id=user_data.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Getting a post by ID
@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    user_data: schemas.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no post with id: {id}",
        )
    return post


# Delete post by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    user_data: schemas.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no post with id: {id}",
        )
    if post.user_id != user_data.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}


# Update post by ID
@router.put("/{id}", response_model=schemas.PostUpdate)
def update_post(
    id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    user_data: schemas.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no post with id: {id}",
        )
    if post.user_id != user_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
