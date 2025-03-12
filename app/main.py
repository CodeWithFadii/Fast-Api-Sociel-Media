from typing import Optional
from fastapi import Body, FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    return next(filter(lambda x: x["id"] == id, my_posts), None)


my_posts = [
    {"title": "This is a title 1", "content": "This is a content 1", "id": 1},
    {"title": "This is a title 2", "content": "This is a content 2", "id": 2},
]


@app.get("/")
def root():
    return {"message": "This is fast api project"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(1, 10000)
    my_posts.append(post_dict)
    return {"data": post}


@app.get("/post/{id}")
def get_post(id: int):
    post = find_post(id=id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Their is not post with id: {id}",
        )
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id=id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Their is not post with id: {id}",
        )
    my_posts.remove(post) @ app.delete(
        "/posts/{id}", status_code=status.HTTP_204_NO_CONTENT
    )


@app.put("/posts/{id}")
def update_post(id: int, post_data: Post):
    post = find_post(id=id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Their is not post with id: {id}",
        )
    post.update(post_data)
    return {"message": "Post updated successfully"}
