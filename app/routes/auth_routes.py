#####################################
### -- Authentication handling -- ###
#####################################

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud 
from app.models.models import LoginInput, SignupInput
from app.session import create_session, get_user_id, delete_session
import uuid
router = APIRouter()



###############
### Signup  ###
###############
@router.post("/signup")
def signup(data: SignupInput, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = crud.create_user(db, data.username, data.email, data.password)
    return {
        "message": "Signup successful",
        "user_id": new_user.id,
        "username": new_user.name
    }



###############
### Login  ####
###############

@router.post("/login")
def login(response: Response, data: LoginInput, db: Session = Depends(get_db)):
    user = crud.verify_user_credentials(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    session_id = str(uuid.uuid4())
    response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True)
    
    create_session(session_id, user.id)  # Save the session
    
    return {"message": "Login successful", "user_id": user.id, "name": user.name}

