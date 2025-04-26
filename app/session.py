# Temporary in-memory session store (only for development/testing)
session_store = {}

def create_session(session_id: str, user_id: int):
    session_store[session_id] = user_id

def get_user_id(session_id: str):
    return session_store.get(session_id)

def delete_session(session_id: str):
    session_store.pop(session_id, None)