from fastapi import Cookie, HTTPException
from typing import Optional
from app.session import get_user_id as lookup_user_id

#####################################
### -- Helper-logic for routes -- ###
#####################################
## Finding current user if applicable for posts
def get_current_user_id(session_id: str = Cookie(None)) -> int:
    if not session_id:
        raise HTTPException(status_code=401, detail="Not logged in.")
    user_id = lookup_user_id(session_id)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    return user_id

## Finding current user without requiring login.
def get_optional_user_id(session_id: str = Cookie(None)) -> Optional[int]:
    if not session_id:
        return None
    return lookup_user_id(session_id)
