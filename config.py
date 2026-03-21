import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database Configuration
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

# Face Recognition Configuration
CONFIDENCE_THRESHOLD = 0.6

# Server Configuration
PORT = 5000
HOST = "0.0.0.0"
DEBUG = True
