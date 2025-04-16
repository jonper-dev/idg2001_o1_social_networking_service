from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.routes import users, posts ### Importing our route modules

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running"}

### Including the routers from other files.
app.include_router(users.router)
app.include_router(posts.router)
