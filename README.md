# Offline Facial Recognition Attendance System

A Flask-based backend for an offline facial recognition attendance system running on a Raspberry Pi. The Pi acts as a WiFi hotspot and provides this local web server.

## Features
- **Offline Capable:** Runs locally on a Raspberry Pi
- **Facial Recognition:** Uses `face_recognition` library to detect and identify students automatically
- **SQLite Database:** Stores students, sessions, admins, and attendance logs
- **Flask API:** Clean modular API using Blueprints
- **Google Sheets Sync:** Placeholder logic to optionally push data to Google Sheets

## Requirements
- Python 3.7+
- Raspberry Pi with Camera Module or USB Camera

## Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: `face_recognition` and `dlib` can take some time to compile on a Raspberry Pi. See standard guides for installing `dlib` on Raspberry Pi if needed.*

3. Initialize the database:
   ```bash
   python database.py
   ```

## Running the Server

Start the application:
```bash
python app.py
```
The server will run at `http://0.0.0.0:5000` (configurable in `config.py`).

## API Endpoints List

All API endpoints return JSON responses. Currently, they are placeholders returning standard success messages.

### Auth
- `POST /api/auth/login` - Admin login

### Students
- `GET /api/students/` - List all enrolled students
- `POST /api/students/enroll` - Enroll a new student

### Sessions
- `POST /api/sessions/start` - Start a new attendance session
- `POST /api/sessions/end` - End the current session

### Attendance
- `POST /api/attendance/mark` - Mark attendance for a student
- `GET /api/attendance/export` - Export attendance data
