from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db import get_db
from app.routes import users, posts ## Importing our route modules
## Note that directories are separated by a dot (.) and not a slash (/).

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Only allow your frontend during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Server is running"}

## Including the routers from other files.
app.include_router(users.router)
app.include_router(posts.router)
