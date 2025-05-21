from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud

router = APIRouter()

## Search posts by content
@router.get("/")
def search(
    query: str = Query(..., min_length=1),
    type: str = Query("posts"),  # Default to searching posts
    db: Session = Depends(get_db)
):
    if type == "posts":
        results = crud.search_posts(db, query)
    elif type == "accounts":
        results = crud.search_accounts(db, query)
    elif type == "hashtags":
        results = crud.search_hashtags(db, query)
    else:
        raise HTTPException(status_code=400, detail="Invalid search type.")
    
    return results