#####################################
### -- Authentication handling -- ###
#####################################
from fastapi import APIRouter, Depends, Response, Cookie, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud 
from app.models.models import LoginInput, SignupInput
from app.session import create_session, get_user_id, delete_session, session_store
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])

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
def login(data: LoginInput, response: Response, db: Session = Depends(get_db)):
    user = crud.verify_user_credentials(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    session_id = str(uuid.uuid4())      ## Create a new session ID.
    create_session(session_id, user.id) ## Save the session.

    response.set_cookie(key="session_id", value=session_id, httponly=True)
    
    return {"message": "Login successful", "user_id": user.id, "name": user.name}

################
### Logout  ####
################
@router.post("/logout")
def logout_user(
    response: Response,
    session_id: str = Cookie(None)
):
    if session_id:
        delete_session(session_id)
        response.delete_cookie("session_id")
        return {"message": "Logged out successfully."}
    else:
        raise HTTPException(status_code=401, detail="Not logged in.")
