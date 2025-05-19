from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Union
from app.models.models import Post
from app.schemas.schemas import PostOutput, UserPublic
from app.dependencies.auth import get_optional_user_id
from app.db import get_db
from app import crud

router = APIRouter()

## Search posts by content
@router.get("", response_model=Union[List[PostOutput], List[UserPublic]])
def search(
    query: str = Query(..., min_length=1),
    type: str = Query("posts"),  # Default to lowercase 'posts' for consistency
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(get_optional_user_id)
):
    if type.lower() == "posts":  # Normalize the type to lowercase
        posts = db.query(Post).options(joinedload(Post.likes), joinedload(Post.author))\
            .filter(Post.content.ilike(f"%{query}%")).all()

        return [
            PostOutput(
                id=post.id,
                content=post.content,
                timestamp=post.created_at,
                user_id=post.user_id,
                username=post.author.name if post.author else "Anonymous",
                likes=len(post.likes),
                is_liked_by_user=any(liker.id == user_id for liker in post.likes) if user_id else False
            )
            for post in posts
        ]
    
    elif type.lower() == "accounts":
        users = crud.search_accounts(db, query)
        return [UserPublic.model_validate(user) for user in users]

    elif type.lower() == "hashtags":
        hashtags = crud.search_hashtags(db, query)
        return [hashtag.name for hashtag in hashtags]

    else:
        raise HTTPException(status_code=400, detail="Invalid search type.")
