from threading import Lock, Timer
from sqlalchemy.orm import Session
from app.models.models import likes_table

class LikeBatcher:
    def __init__(self, db: Session, flush_interval: int = 60, max_batch_size: int = 10):
        self.db = db
        self.flush_interval = flush_interval # Time-based flush (e.g., every 60 seconds)
        self.max_batch_size = max_batch_size  # Count-based flush (e.g., after 10 likes)
        self.likes = []
        self.lock = Lock()
        self.timer = Timer(self.flush_interval, self.flush_likes)
        self.timer.start()

    def add_like(self, user_id: int, post_id: int):
        with self.lock:
            self.likes.append({"user_id": user_id, "post_id": post_id})
            if len(self.likes) >= self.max_batch_size:
                self._flush_locked()

    def flush_likes(self):
        with self.lock:
            self._flush_locked()
        # Restart the timer
        self.timer = Timer(self.flush_interval, self.flush_likes)
        self.timer.start()

    def _flush_locked(self):
        if self.likes:
            print(f"Flushing likes: {self.likes}")  # Debug line
            self.db.execute(likes_table.insert(), self.likes)
            self.db.commit()
            self.likes = []

    def stop(self):
        self.timer.cancel()