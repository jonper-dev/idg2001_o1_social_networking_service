from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud
from app.models.models import UserCreate, UserUpdate, UserPatch
### Note that directories are separated by a dot (.) and not a slash (/).

router = APIRouter(prefix="/users", tags=["users"])

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
        raise HTTPException(status_code=404, detail="User not found")
    return user



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
