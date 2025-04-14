from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import get_db
from models.models import User

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running"}

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users