# app/utils/logger.py

from fastapi import Request
from typing import List
from threading import Lock
from datetime import datetime, timezone


# Store API calls and DB access count
api_calls: List[dict] = []
db_access_count = 0
log_lock = Lock()

def log_api_call(method: str, path: str, status_code: int = None):
    with log_lock:
         api_calls.append({
            "method": method,
            "path": path,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat()
        })

def log_db_access():
    global db_access_count
    with log_lock:
        db_access_count += 1

def get_logs():
    with log_lock:
        return {
            "api_calls": api_calls.copy(),
            "db_accesses": db_access_count
        }
