from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud

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
