import sqlite3
import os
from config import DB_PATH

def get_db_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database with tables from schema.sql."""
    # Ensure the parent directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    schema_path = os.path.join(os.path.dirname(__file__), 'models', 'schema.sql')
    
    with get_db_connection() as conn:
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
