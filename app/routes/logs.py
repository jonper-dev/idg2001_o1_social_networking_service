from fastapi import APIRouter
from app.utils.logger import get_logs

router = APIRouter()

@router.get("/logs")
def read_logs():
    return get_logs()
