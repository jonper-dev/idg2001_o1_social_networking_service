from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import crud
from app.models.models import Post, PostCreate, PostUpdate, PostPatch, PostOutput, likes, post_hashtags

# Temporary in-memory session store (only for development/testing)
session_store = {}

router = APIRouter(prefix="/posts", tags=["posts"])

#########################
### -- GET-methods -- ###
#########################
## Getting all posts (and comment-posts), also used for showing posts.
@router.get("/", response_model=List[PostOutput])
def get_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return [
        PostOutput(
            id=post.id,
            content=post.content,
            timestamp=post.created_at,
            user_id=post.user_id,
            username=post.author.name ## From the table-join.
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
def partial_update_post(post_id: int, post_update: PostPatch, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    ## Find a proper way to check for currently logged in user later.
    # if post.user_id != current_user["id"]:
    #     raise HTTPException(status_code=403, detail="Not authorized to edit this post.")
    
    post.content = post_update.content
    db.commit()
    db.refresh(post)
    return post

## Delete post
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_post(db, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found.")
    return {"message": "Post deleted."}

###############
### Like Post ###
###############
@router.post("/like/{post_id}")
def like_post(post_id: int, db: Session = Depends(get_db), response: Response = Depends()):
    # Get the session ID from the cookie
    session_id = response.cookies.get("session_id")
    if not session_id or session_id not in session_store:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_id = session_store[session_id]  # Get the user ID from session store

    # Check if the post already exists
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if the user has already liked the post
    if crud.is_post_liked_by_user(db, post_id, user_id):
        raise HTTPException(status_code=400, detail="Already liked this post")

    # Like the post by inserting into the likes table
    crud.like_post(db, user_id, post_id)

    return JSONResponse(content={"message": "Post liked successfully"}, status_code=200)

###############
### Unlike Post ###
###############
@router.post("/unlike/{post_id}")
def unlike_post(post_id: int, db: Session = Depends(get_db), response: Response = Depends()):
    # Get the session ID from the cookie
    session_id = response.cookies.get("session_id")
    if not session_id or session_id not in session_store:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_id = session_store[session_id]  # Get the user ID from session store

    # Check if the post exists
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if the user has liked the post
    if not crud.is_post_liked_by_user(db, post_id, user_id):
        raise HTTPException(status_code=400, detail="Post not liked yet")

    # Unlike the post by removing from the likes table
    crud.unlike_post(db, user_id, post_id)

    return JSONResponse(content={"message": "Post unliked successfully"}, status_code=200)

## Search posts by content
@router.get("/search")
def search_posts(query: str, db: Session = Depends(get_db)):
    results = db.query(Post).filter(Post.content.ilike(f"%{query}%")).order_by(Post.created_at.desc()).all()
    return results