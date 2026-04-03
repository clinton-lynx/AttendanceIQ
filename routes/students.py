# from flask import Blueprint, jsonify, request
# from database import get_db_connection
# import config

# students_bp = Blueprint('students', __name__)


# @students_bp.route('/verify-matric', methods=['POST'])
# def verify_matric():
#     data = request.get_json()
#     matric = data.get("matric_number")

#     if not matric:
#         return jsonify({"success": False, "message": "Matric number is required"}), 400

#     conn = get_db_connection()
#     student = conn.execute(
#         "SELECT * FROM students WHERE student_id = ?", (str(matric),)
#     ).fetchone()
#     conn.close()

#     if student:
#         return jsonify({
#             "success": True,
#             "message": "Student found",
#             "data": {
#                 "matric_number": student["student_id"],
#                 "name": student["name"],
#                 "enrolled": student["face_encoding"] is not None  # True if face already saved
#             }
#         }), 200
#     else:
#         return jsonify({"success": False, "message": "Student not found"}), 404


# @students_bp.route('/enroll-face', methods=['POST'])
# def enroll_face():
#     data = request.get_json()
#     matric = data.get("matric_number")
#     face_encoding = data.get("face_encoding")  # list of numbers sent from frontend

#     if not matric or not face_encoding:
#         return jsonify({"success": False, "message": "Matric number and face encoding are required"}), 400

#     try:
#         conn = get_db_connection()
        
#         # Check student exists first
#         student = conn.execute(
#             "SELECT * FROM students WHERE student_id = ?", (str(matric),)
#         ).fetchone()

#         if not student:
#             conn.close()
#             return jsonify({"success": False, "message": "Student not found"}), 404

#         # Save the face encoding as JSON string
#         import json
#         conn.execute(
#             "UPDATE students SET face_encoding = ? WHERE student_id = ?",
#             (json.dumps(face_encoding), str(matric))
#         )
#         conn.commit()
#         conn.close()
#         return jsonify({"success": True, "message": "Face enrolled successfully"}), 200

#     except Exception as e:
#         if 'conn' in locals():
#             conn.close()
#         print(f"Error enrolling face: {str(e)}")
#         # Assuming config is available or defined elsewhere for DEBUG
#         # If config is not defined, this line will cause a NameError.
#         # For this exercise, we'll include it as per instruction.
#         # In a real application, you'd ensure config is imported/defined.
#         return jsonify({
#             "success": False, 
#             "message": "Database error occurred. Please try again later.",
#             "error": str(e) if config.DEBUG else "Internal Server Error"
#         }), 500







from flask import Blueprint, jsonify, request
from database import get_db_connection
import json

students_bp = Blueprint('students', __name__)


@students_bp.route('/verify-matric', methods=['POST'])
def verify_matric():
    data = request.get_json()
    matric = data.get("matric_number")

    if not matric:
        return jsonify({"success": False, "message": "Matric number is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE student_id = %s", (str(matric),)
    )
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    if student:
        return jsonify({
            "success": True,
            "message": "Student found",
            "data": {
                "matric_number": student["student_id"],
                "name": student["name"],
                "enrolled": student["face_encoding"] is not None
            }
        }), 200
    else:
        return jsonify({"success": False, "message": "Student not found"}), 404


@students_bp.route('/enroll-face', methods=['POST'])
def enroll_face():
    data = request.get_json()
    matric = data.get("matric_number")
    face_encoding = data.get("face_encoding")

    if not matric or not face_encoding:
        return jsonify({"success": False, "message": "Matric number and face encoding are required"}), 400

    if not isinstance(face_encoding, list) or len(face_encoding) == 0:
        return jsonify({"success": False, "message": "face_encoding must be a non-empty array"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE student_id = %s", (str(matric),)
    )
    student = cursor.fetchone()

    if not student:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Student not found"}), 404

    if student["face_encoding"] is not None:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Student already enrolled", "enrolled": True}), 400

    cursor.execute(
        "UPDATE students SET face_encoding = %s WHERE student_id = %s",
        (json.dumps(face_encoding), str(matric))
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True, "message": "Face enrolled successfully"}), 200