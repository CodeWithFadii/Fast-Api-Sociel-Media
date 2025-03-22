from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db

router = APIRouter(tags=["Authentication"])


# Creating a new user
@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def login(credential: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credential.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email does not exist",
        )

    if not utils.verify_password(credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
        )

    return user
