from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Connecting to database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="deve6426",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Connection successful to database")
except Exception as error:
    print("Error while connecting to PostgreSQL", error)
    conn.close()


def find_post(id):
    return next(filter(lambda x: x["id"] == id, my_posts), None)


def raise_exception(status_code, detail):
    raise HTTPException(
        status_code=status_code,
        detail=detail,
    )


my_posts = [
    {"title": "This is a title 1", "content": "This is a content 1", "id": 1},
    {"title": "This is a title 2", "content": "This is a content 2", "id": 2},
]


@app.get("/")
def root():
    return {"message": "This is fast api project"}


# Getting all posts
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    return {"data": cursor.fetchall()}


# Creating new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# Getting post with ID
@app.get("/post/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = (%s)""", (id,))
    post = cursor.fetchone()
    if not post:
        raise_exception(status.HTTP_404_NOT_FOUND, f"Their is no post with id: {id}")
    return {"data": post}


# Delete post with ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise_exception(status.HTTP_404_NOT_FOUND, f"Their is no post with id: {id}")


# UPdate post with ID
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, id),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise_exception(status.HTTP_404_NOT_FOUND, f"Their is no post with id: {id}")
    return {"data": updated_post}
