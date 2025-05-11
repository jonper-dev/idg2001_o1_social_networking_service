from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db import get_db
from app import crud
from app.dependencies.auth import get_optional_user_id
from app.models.models import Post, PostOutput, UserCreate, UserUpdate, UserPatch
## Note that directories are separated by a dot (.) and not a slash (/).

router = APIRouter()

#########################
### -- GET-methods -- ###
#########################
## Getting all users.
@router.get("/")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

## Getting a specific user by their ID.
@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

## Getting all posts by a specific user.
@router.get("/{user_id}/posts", response_model=List[PostOutput])
def get_user_posts(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_optional_user_id)
):
    posts = (
        db.query(Post)
        .options(joinedload(Post.author), joinedload(Post.likes))
        .filter(Post.user_id == user_id)
        .all()
    )

    return [
        PostOutput(
            id=post.id,
            content=post.content,
            timestamp=post.created_at,
            user_id=post.user_id,
            username=post.author.name,
            likes=len(post.likes),
            is_liked_by_user=any(user.id == current_user_id for user in post.likes) if current_user_id else False
        )
        for post in posts
    ]



###########################
### -- Other methods -- ###
###########################
## Creating a new user. A new user-ID will be assigned.
@router.post("/")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.name, user.email, user.password)

## Updating a user.
@router.put("/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, user_update.name, user_update.email, user_update.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

## Partial update of a user. Only the fields that are provided will be updated.
@router.patch("/{user_id}")
def patch_user(user_id: int, updates: UserPatch, db: Session = Depends(get_db)):
    updated_user = crud.partial_update_user(db, user_id, updates.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return updated_user

## Delete user
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)
