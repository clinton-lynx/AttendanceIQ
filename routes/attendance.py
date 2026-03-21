# from flask import Blueprint, jsonify
# from database import get_db_connection

# attendance_bp = Blueprint('attendance', __name__)


# @attendance_bp.route('/session/<int:session_id>', methods=['GET'])
# def get_session_attendance(session_id):
#     """Get all attendance records for a specific session"""
#     conn = get_db_connection()

#     # First check the session exists
#     session = conn.execute(
#         "SELECT * FROM sessions WHERE id = ?", (session_id,)
#     ).fetchone()

#     if not session:
#         conn.close()
#         return jsonify({"success": False, "message": "Session not found"}), 404

#     # Get all attendance records for this session
#     # JOIN with students table so we get the student name too
#     records = conn.execute("""
#         SELECT 
#             attendance.id,
#             attendance.student_id,
#             students.name,
#             attendance.timestamp
#         FROM attendance
#         JOIN students ON attendance.student_id = students.student_id
#         WHERE attendance.session_id = ?
#         ORDER BY attendance.timestamp ASC
#     """, (session_id,)).fetchall()

#     conn.close()

#     return jsonify({
#         "success": True,
#         "session_id": session_id,
#         "is_active": bool(session["is_active"]),
#         "total_present": len(records),
#         "data": [dict(row) for row in records]
#     }), 200


# @attendance_bp.route('/current', methods=['GET'])
# def get_current_attendance():
#     """Get attendance for the currently active session"""
#     conn = get_db_connection()

#     # Find the active session
#     session = conn.execute(
#         "SELECT * FROM sessions WHERE is_active = 1"
#     ).fetchone()

#     if not session:
#         conn.close()
#         return jsonify({"success": False, "message": "No active session"}), 404

#     # Get attendance records for this session
#     records = conn.execute("""
#         SELECT 
#             attendance.id,
#             attendance.student_id,
#             students.name,
#             attendance.timestamp
#         FROM attendance
#         JOIN students ON attendance.student_id = students.student_id
#         WHERE attendance.session_id = ?
#         ORDER BY attendance.timestamp ASC
#     """, (session["id"],)).fetchall()

#     conn.close()

#     return jsonify({
#         "success": True,
#         "session_id": session["id"],
#         "start_time": session["start_time"],
#         "total_present": len(records),
#         "data": [dict(row) for row in records]
#     }), 200


# @attendance_bp.route('/history', methods=['GET'])
# def get_attendance_history():
#     """Get all past sessions with attendance counts"""
#     conn = get_db_connection()

#     # Get all sessions with a count of how many students attended each
#     sessions = conn.execute("""
#         SELECT 
#             sessions.id,
#             sessions.start_time,
#             sessions.end_time,
#             sessions.is_active,
#             COUNT(attendance.id) as total_present
#         FROM sessions
#         LEFT JOIN attendance ON attendance.session_id = sessions.id
#         GROUP BY sessions.id
#         ORDER BY sessions.start_time DESC
#     """).fetchall()

#     conn.close()

#     return jsonify({
#         "success": True,
#         "total_sessions": len(sessions),
#         "data": [dict(row) for row in sessions]
#     }), 200


# @attendance_bp.route('/mark', methods=['POST'])
# def mark_attendance():
#     # Placeholder — needs face matching and sessions to be ready first
#     return jsonify({"success": True, "message": "attendance/mark endpoint working"})



from flask import Blueprint, jsonify, request
from database import get_db_connection
from services.face_service import match_face

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/mark', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    matric = data.get("matric_number")
    live_encoding = data.get("face_encoding")

    if not matric or not live_encoding:
        return jsonify({"success": False, "message": "Matric number and face encoding are required"}), 400

    conn = get_db_connection()

    session = conn.execute(
        "SELECT * FROM sessions WHERE is_active = 1"
    ).fetchone()

    if not session:
        conn.close()
        return jsonify({"success": False, "message": "No active session"}), 400

    student = conn.execute(
        "SELECT * FROM students WHERE student_id = ?", (str(matric),)
    ).fetchone()

    if not student:
        conn.close()
        return jsonify({"success": False, "message": "Student not found"}), 404

    if not student["face_encoding"]:
        conn.close()
        return jsonify({"success": False, "message": "Student has not enrolled their face yet"}), 400

    already_marked = conn.execute("""
        SELECT * FROM attendance 
        WHERE session_id = ? AND student_id = ?
    """, (session["id"], str(matric))).fetchone()

    if already_marked:
        conn.close()
        return jsonify({"success": False, "message": "Attendance already marked for this session"}), 400

    is_match = match_face(live_encoding, student["face_encoding"])

    if not is_match:
        conn.close()
        return jsonify({"success": False, "message": "Face does not match"}), 401

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attendance (session_id, student_id)
        VALUES (?, ?)
    """, (session["id"], str(matric)))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Attendance marked successfully",
        "data": {
            "student_id": matric,
            "name": student["name"],
            "session_id": session["id"],
        }
    }), 200


@attendance_bp.route('/session/<int:session_id>', methods=['GET'])
def get_session_attendance(session_id):
    conn = get_db_connection()

    session = conn.execute(
        "SELECT * FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()

    if not session:
        conn.close()
        return jsonify({"success": False, "message": "Session not found"}), 404

    records = conn.execute("""
        SELECT 
            attendance.id,
            attendance.student_id,
            students.name,
            attendance.timestamp
        FROM attendance
        JOIN students ON attendance.student_id = students.student_id
        WHERE attendance.session_id = ?
        ORDER BY attendance.timestamp ASC
    """, (session_id,)).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "session_id": session_id,
        "is_active": bool(session["is_active"]),
        "total_present": len(records),
        "data": [dict(row) for row in records]
    }), 200


@attendance_bp.route('/current', methods=['GET'])
def get_current_attendance():
    conn = get_db_connection()

    session = conn.execute(
        "SELECT * FROM sessions WHERE is_active = 1"
    ).fetchone()

    if not session:
        conn.close()
        return jsonify({"success": False, "message": "No active session"}), 404

    records = conn.execute("""
        SELECT 
            attendance.id,
            attendance.student_id,
            students.name,
            attendance.timestamp
        FROM attendance
        JOIN students ON attendance.student_id = students.student_id
        WHERE attendance.session_id = ?
        ORDER BY attendance.timestamp ASC
    """, (session["id"],)).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "session_id": session["id"],
        "start_time": session["start_time"],
        "total_present": len(records),
        "data": [dict(row) for row in records]
    }), 200


@attendance_bp.route('/history', methods=['GET'])
def get_attendance_history():
    conn = get_db_connection()

    sessions = conn.execute("""
        SELECT 
            sessions.id,
            sessions.start_time,
            sessions.end_time,
            sessions.is_active,
            COUNT(attendance.id) as total_present
        FROM sessions
        LEFT JOIN attendance ON attendance.session_id = sessions.id
        GROUP BY sessions.id
        ORDER BY sessions.start_time DESC
    """).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "total_sessions": len(sessions),
        "data": [dict(row) for row in sessions]
    }), 200