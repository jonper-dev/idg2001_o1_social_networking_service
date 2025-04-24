from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import crud
from app.models.models import PostCreate, PostUpdate, PostPatch, PostOutput

router = APIRouter(prefix="/posts", tags=["posts"])

#########################
### -- GET-methods -- ###
#########################
## Getting all posts (and comment-posts), also used for showing posts.
@router.get("/", response_model=List[PostOutput])
def read_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return [
        PostOut(
            id=post.id,
            content=post.content,
            timestamp=post.created_at,
            user_id=post.user_id,
            username=post.user.name ## From the table-join.
        )
        for post in posts
    ]

## Getting a specific post by its ID.
@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return post



###########################
### -- Other methods -- ###
###########################
## Creating a new post (or comment-post). A new post-ID will be assigned.
@router.post("/")
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_post(db, post_data)
    except Exception as e:
        print("Error creating post:", e)
        raise HTTPException(status_code=500, detail="Could not create post.")

## Updating a post.
@router.put("/{post_id}")
def update_post(post_id: int, updated: PostUpdate, db: Session = Depends(get_db)):
    post = crud.update_post(db, post_id, updated.content)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return post


## Partial update of a post. Only the fields that are provided will be updated.
@router.patch("/{post_id}")
def patch_post(post_id: int, updates: PostPatch, db: Session = Depends(get_db)):
    updated_post = crud.partial_update_post(db, post_id, updates.dict(exclude_unset=True))
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return updated_post

## Delete post
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_post(db, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found.")
    return {"message": "Post deleted."}
