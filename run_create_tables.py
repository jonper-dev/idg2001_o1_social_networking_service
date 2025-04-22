## Root-script for running create_tables.py.
## Avoids any pathing issues if one runs this from the root.
from app.setup.create_tables import create_tables

if __name__ == "__main__":
    create_tables()
