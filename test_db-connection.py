from sqlalchemy import create_engine, text
from app.config import DATABASE_URL

## Testing file for the database connection.
## This file is used to test the database connection and is not part of the main application.
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Connected to DB successfully.")
except Exception as e:
    print("❌ Failed to connect to DB:", e)
