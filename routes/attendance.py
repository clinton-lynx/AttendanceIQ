from flask import Blueprint, jsonify
from database import get_db_connection

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/session/<int:session_id>', methods=['GET'])
def get_session_attendance(session_id):
    """Get all attendance records for a specific session"""
    conn = get_db_connection()

    # First check the session exists
    session = conn.execute(
        "SELECT * FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()

    if not session:
        conn.close()
        return jsonify({"success": False, "message": "Session not found"}), 404

    # Get all attendance records for this session
    # JOIN with students table so we get the student name too
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
    """Get attendance for the currently active session"""
    conn = get_db_connection()

    # Find the active session
    session = conn.execute(
        "SELECT * FROM sessions WHERE is_active = 1"
    ).fetchone()

    if not session:
        conn.close()
        return jsonify({"success": False, "message": "No active session"}), 404

    # Get attendance records for this session
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
    """Get all past sessions with attendance counts"""
    conn = get_db_connection()

    # Get all sessions with a count of how many students attended each
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


@attendance_bp.route('/mark', methods=['POST'])
def mark_attendance():
    # Placeholder — needs face matching and sessions to be ready first
    return jsonify({"success": True, "message": "attendance/mark endpoint working"})