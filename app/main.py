from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

# Initialize FastAPI app
app = FastAPI()

# Create tables in the database
models.Base.metadata.create_all(bind=engine)


# Custom error handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field_path = " → ".join(str(loc) for loc in error["loc"])
        errors.append({"field": field_path, "message": error["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "errors": errors},
    )


@app.get("/")
def root():
    return {"message": "This is a FastAPI project"}


# Getting all posts
@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Creating a new post
@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreate
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Getting a post by ID
@app.get("/post/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no post with id: {id}",
        )
    return post


# Delete post by ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no post with id: {id}",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}


# Update post by ID
@app.put("/posts/{id}", response_model=schemas.PostUpdate)
def update_post(
    id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no post with id: {id}",
        )
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


# Creating a new user
@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user.email)
    if user_query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email already exists",
        )
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Getting a user by ID
@app.post(
    "/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user.email)
    if user_query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email already exists",
        )
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
