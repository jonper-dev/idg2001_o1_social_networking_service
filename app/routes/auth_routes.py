#####################################
### -- Authentication handling -- ###
#####################################
## User creation, user registration, ... ?

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud 

router = APIRouter()

########################
### Signup endpoint  ###
########################
@router.post("/signup/")
def signup(
     username: str = Form(...), 
     email: str = Form(...), 
     password: str = Form(...), 
     db: Session = Depends(get_db)
):
    
    existing_user = crud.get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = crud.create_user(db, name, email, password)
    return {"message": "Signup successful", "user": new_user}

@router.get("/login/")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user": user}
