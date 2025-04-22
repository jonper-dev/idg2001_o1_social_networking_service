from app.models.models import Base
from app.db import engine
## Setup-file for creating tables in the database.
## Not needed after launch, but useful for development.

from app.models.models import Base
from app.db import engine

def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created on Clever Cloud DB.")

if __name__ == "__main__":
    create_tables()
