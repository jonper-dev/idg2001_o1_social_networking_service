from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud

router = APIRouter(prefix="/posts", tags=["posts"])

#########################
### -- GET-methods -- ###
#########################
### Getting all posts (and comment-posts).
@router.get("/")
def get_all_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

### Getting a specific post by its ID.
@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post



###########################
### -- Other methods -- ###
###########################
### Creating a new post (or comment-post). A new post-ID will be assigned.
@router.post("/")
def create_post(title: str, content: str, user_id: int, db: Session = Depends(get_db)):
    return crud.create_post(db, title, content, user_id)

### Updating a post.
@router.put("/{post_id}")
def update_post(post_id: int, title: str, content: str, db: Session = Depends(get_db)):
    post = crud.update_post(db, post_id, title, content)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return post
