from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# Creating a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user.email)
    if user_query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email already exists",
        )
    # Hashing password
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Getting a user by ID
@router.get("/{id}", response_model=schemas.User)
def create_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with id: {id}",
        )
    user = user_query.first()
    return user
