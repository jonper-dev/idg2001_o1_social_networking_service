from threading import Lock, Timer
from sqlalchemy.orm import Session
from app.models.models import likes_table

class LikeBatcher:
    def __init__(self, db: Session, flush_interval: int = 5):
        self.db = db
        self.flush_interval = flush_interval
        self.likes = []
        self.lock = Lock()
        self.timer = Timer(self.flush_interval, self.flush_likes)
        self.timer.start()

    def add_like(self, user_id: int, post_id: int):
        with self.lock:
            self.likes.append({"user_id": user_id, "post_id": post_id})

    def flush_likes(self):
        with self.lock:
            if self.likes:
                print(f"Flushing likes: {self.likes}")  # Add this line for debugging
                self.db.execute(likes_table.insert(), self.likes)
                self.db.commit()
                self.likes = []
        # Restart the timer
        self.timer = Timer(self.flush_interval, self.flush_likes)
        self.timer.start()

    def stop(self):
        self.timer.cancel()