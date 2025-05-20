from fastapi import APIRouter, Cookie, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db import get_db, SessionLocal
from app import crud
from app.dependencies.auth import get_current_user_id, get_optional_user_id
from app.models.models import Post
from app.schemas.schemas import PostCreate, PostUpdate, PostPatch, PostOutput
from app.session import session_store
from app.utils.redis_cache import get_cache, set_cache, delete_cache
from app.utils.like_batcher import LikeBatcher
import json
## Note that directories are separated by a dot (.) and not a slash (/).

router = APIRouter()

# Initialize the LikeBatcher (you may want to use dependency injection for the DB session)
like_batcher = None

@router.on_event("startup")
def initialize_batcher():
    global like_batcher
    db = SessionLocal()  # Create a database session
    like_batcher = LikeBatcher(db=db, flush_interval=5)  # Use the correct flush interval

@router.on_event("shutdown")
def stop_batcher():
    global like_batcher
    if like_batcher:
        like_batcher.stop()
        like_batcher.db.close()  # Close the database session

#########################
### -- GET-methods -- ###
#########################
## Getting all posts (and comment-posts), also used for showing posts.
@router.get("/", response_model=List[PostOutput])
def get_posts(
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(get_optional_user_id)
):
    cache_key = "all_posts"
    cached_posts = get_cache(cache_key)

    if cached_posts:
        return json.loads(cached_posts)

    posts = db.query(Post).options(
        joinedload(Post.likes),
        joinedload(Post.reply_to).joinedload(Post.author)
    ).all()

    post_outputs = [
        PostOutput(
            id=post.id,
            content=post.content,
            timestamp=post.created_at,
            user_id=post.user_id,
            username=post.author.name,
            likes=len(post.likes),
            is_liked_by_user=any(liker.id == user_id for liker in post.likes) if user_id else False,
            reply_to_username=post.reply_to.author.name if post.reply_to else None
        )
        for post in posts
    ]

    set_cache(cache_key, json.dumps([post.dict() for post in post_outputs], default=str))
    return post_outputs

## Getting a specific post by its ID.
@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return post




############################
### Authenticated routes ###
############################

## Helper function for verifying posts
def verify_ownership(post, user_id):
    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized.")

## Creating a new post (or comment-post). A new post-ID will be assigned.
@router.post("/")
def create_post(
    post_data: PostCreate, 
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    delete_cache("all_posts")
    return crud.create_post(db, post_data, user_id=user_id)

## Updating a post.
@router.put("/{post_id}")
def update_post(
    post_id: int, 
    updated: PostUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    delete_cache("all_posts")
    return crud.update_post(db, post_id, updated.content)

## Partial update of a post. Only the fields that are provided will be updated.
@router.patch("/{post_id}")
def partial_update_post(
    post_id: int, 
    post_update: PostPatch,  
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
    ):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    verify_ownership(post, user_id)

    if post_update.content:
        post.content = post_update.content

    db.commit()
    db.refresh(post)
    return post

## Delete post
@router.delete("/{post_id}")
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    delete_cache("all_posts")
    return crud.delete_post(db, post_id)

##########################
### Like / Unlike Post ###
##########################

## Like post
@router.post("/{post_id}/like")
def like_post(post_id: int, user_id: int = Depends(get_current_user_id)):
    global like_batcher
    if not like_batcher:
        raise HTTPException(status_code=500, detail="LikeBatcher is not initialized.")
    like_batcher.add_like(user_id, post_id)
    return {"message": "Like added to batch"}

