from flask import Blueprint, jsonify, request
from database import get_db_connection

students_bp = Blueprint('students', __name__)


@students_bp.route('/verify-matric', methods=['POST'])
def verify_matric():
    data = request.get_json()
    matric = data.get("matric_number")

    if not matric:
        return jsonify({"success": False, "message": "Matric number is required"}), 400

    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE student_id = ?", (str(matric),)
    ).fetchone()
    conn.close()

    if student:
        return jsonify({
            "success": True,
            "message": "Student found",
            "data": {
                "matric_number": student["student_id"],
                "name": student["name"],
                "enrolled": student["face_encoding"] is not None  # True if face already saved
            }
        }), 200
    else:
        return jsonify({"success": False, "message": "Student not found"}), 404


@students_bp.route('/enroll-face', methods=['POST'])
def enroll_face():
    data = request.get_json()
    matric = data.get("matric_number")
    face_encoding = data.get("face_encoding")  # list of numbers sent from frontend

    if not matric or not face_encoding:
        return jsonify({"success": False, "message": "Matric number and face encoding are required"}), 400

    conn = get_db_connection()

    # Check student exists first
    student = conn.execute(
        "SELECT * FROM students WHERE student_id = ?", (str(matric),)
    ).fetchone()

    if not student:
        conn.close()
        return jsonify({"success": False, "message": "Student not found"}), 404

    # Save the face encoding as JSON string
    import json
    conn.execute(
        "UPDATE students SET face_encoding = ? WHERE student_id = ?",
        (json.dumps(face_encoding), str(matric))
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Face enrolled successfully"}), 200