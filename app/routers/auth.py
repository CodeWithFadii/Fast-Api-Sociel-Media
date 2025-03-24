from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(tags=["Authentication"])


# Creating a new user
@router.post(
    "/login", response_model=schemas.Token
)
def login(credential: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        user = (
            db.query(models.User).filter(models.User.email == credential.email).first()
        )

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
        access_token = oauth2.create_access_token({"user_id": user.id})

        return {"access_token": access_token, "token_type": "bearer"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
