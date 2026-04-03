# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# # Database Configuration
# DB_PATH = os.path.join(BASE_DIR, "attendance.db")

# # Face Recognition Configuration
# CONFIDENCE_THRESHOLD = 0.6

# # Server Configuration
# PORT = 5000
# HOST = "0.0.0.0"
# DEBUG = True


import os

# Database Configuration
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://attendanceiq_db_2_user:hnRNAuEIAVPIH3TrNLuYsBQFYno42wpj@dpg-d77vvknkijhs73a8n81g-a.oregon-postgres.render.com/attendanceiq_db_2"
    # "postgresql://attendanceiq_db_2_user:hnRNAuEIAVPIH3TrNLuYsBQFYno42wpj@dpg-d77vknkijhs73a8n81g-a/attendanceiq_db_2"
)

# Face Recognition Configuration
CONFIDENCE_THRESHOLD = 0.6

# Server Configuration
PORT = 5000
HOST = "0.0.0.0"
DEBUG = False