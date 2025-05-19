from fastapi import APIRouter, Cookie, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db import get_db
from app import crud
from app.dependencies.auth import get_current_user_id, get_optional_user_id
from app.models.models import Post
from app.schemas.schemas import PostCreate, PostUpdate, PostPatch, PostOutput
from app.session import session_store
## Note that directories are separated by a dot (.) and not a slash (/).

router = APIRouter()

#########################
### -- GET-methods -- ###
#########################
## Getting all posts (and comment-posts), also used for showing posts.
@router.get("/", response_model=List[PostOutput])
def get_posts(
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(get_optional_user_id)
):
    posts = db.query(Post).options(joinedload(Post.likes),
                                   joinedload(Post.reply_to).joinedload(Post.author)).all()

    return [
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
    try:
        return crud.create_post(db, post_data, user_id=user_id)
    except Exception as e:
        print("Error creating post:", e)
        raise HTTPException(status_code=500, detail="Could not create post.")

## Updating a post.
@router.put("/{post_id}")
def update_post(
    post_id: int, 
    updated: PostUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
    ): 

    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    ## Verify ownership using helper function 
    verify_ownership(post, user_id)
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
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    
    verify_ownership(post, user_id)

    crud.delete_post(db, post_id)
    return {"message": "Post deleted."}

##########################
### Like / Unlike Post ###
##########################

## Like post
@router.post("/{post_id}/like")
def like_post(
    post_id: int, 
    db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user_id)
    ):

    return crud.toggle_like(db, user_id, post_id)

# @router.post("/like/{post_id}")
# def like_post(post_id: int, request: Request, db: Session = Depends(get_db)):
#     user_id = check_user_authenticated(request)  # Use the helper function

#     post = crud.get_post(db, post_id)
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")

#     if crud.is_post_liked_by_user(db, post_id, user_id):
#         raise HTTPException(status_code=400, detail="Already liked this post")

#     crud.like_post(db, user_id, post_id)

#     return JSONResponse(content={"message": "Post liked successfully"}, status_code=200)

## Unlike Post
@router.post("/{post_id}/unlike")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    user_id = Depends(get_current_user_id)
):

    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    if not crud.is_post_liked_by_user(db, post_id, user_id):
        raise HTTPException(status_code=400, detail="Post not liked.")

    crud.unlike_post(db, user_id, post_id)

    return JSONResponse(content={"message": "Post unliked successfully."})

