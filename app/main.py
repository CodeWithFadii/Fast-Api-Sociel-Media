from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from . import models
from .routers import post, user,auth
from .database import engine

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "This is a FastAPI project"}
