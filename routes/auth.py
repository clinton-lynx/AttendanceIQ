from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Placeholder login endpoint
    return jsonify({"success": True, "message": "auth/login endpoint working"})
