from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud

router = APIRouter(prefix="/users", tags=["users"])

#########################
### -- GET-methods -- ###
#########################
### Getting all users.
@router.get("/")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

### Getting a specific user by their ID.
@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



###########################
### -- Other methods -- ###
###########################
### Creating a new user. A new user-ID will be assigned.
@router.post("/")
def add_user(name: str, email: str, db: Session = Depends(get_db)):
    return crud.create_user(db, name, email)

### Updating a user.
@router.put("/{user_id}")
def update_user(user_id: int, name: str, email: str, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, name, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
