from database import init_db
from seed import seed_students

if __name__ == "__main__":
    print("Starting database initialization...")
    init_db()
    seed_students()
    print("Database initialization complete.")
