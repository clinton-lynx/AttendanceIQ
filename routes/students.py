from flask import Blueprint, jsonify

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
def list_students():
    # Placeholder list students endpoint
    return jsonify({"success": True, "message": "students/list endpoint working"})

@students_bp.route('/enroll', methods=['POST'])
def enroll_student():
    # Placeholder enroll student endpoint
    return jsonify({"success": True, "message": "students/enroll endpoint working"})
