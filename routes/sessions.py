# from flask import Blueprint, jsonify, request
# from database import get_db_connection

# sessions_bp = Blueprint('sessions', __name__)


# @sessions_bp.route('/start', methods=['POST'])
# def start_session():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO sessions (is_active) VALUES (1)"
#     )
#     conn.commit()
#     new_id = cursor.lastrowid

#     session = conn.execute(
#         "SELECT * FROM sessions WHERE id = ?", (new_id,)
#     ).fetchone()
#     conn.close()

#     return jsonify({
#         "success": True,
#         "message": "Session started",
#         "data": {
#             "session_id": session["id"],
#             "start_time": session["start_time"],
#             "is_active": bool(session["is_active"])
#         }
#     }), 200


# @sessions_bp.route('/end', methods=['POST'])
# def end_session():
#     data = request.get_json()
#     session_id = data.get("session_id")

#     if not session_id:
#         return jsonify({"success": False, "message": "Session ID is required"}), 400

#     conn = get_db_connection()

#     session = conn.execute(
#         "SELECT * FROM sessions WHERE id = ?", (session_id,)
#     ).fetchone()

#     if not session:
#         conn.close()
#         return jsonify({"success": False, "message": "Session not found"}), 404

#     if not session["is_active"]:
#         conn.close()
#         return jsonify({"success": False, "message": "Session is already ended"}), 400

#     conn.execute("""
#         UPDATE sessions 
#         SET is_active = 0, end_time = CURRENT_TIMESTAMP
#         WHERE id = ?
#     """, (session_id,))
#     conn.commit()
#     conn.close()

#     return jsonify({
#         "success": True,
#         "message": "Session ended",
#         "data": {
#             "session_id": session_id,
#             "is_active": False
#         }
#     }), 200


# @sessions_bp.route('/status', methods=['GET'])
# def get_session_status():
#     conn = get_db_connection()

#     session = conn.execute(
#         "SELECT * FROM sessions WHERE is_active = 1"
#     ).fetchone()

#     conn.close()

#     if not session:
#         return jsonify({
#             "success": True,
#             "is_active": False,
#             "message": "No active session"
#         }), 200

#     return jsonify({
#         "success": True,
#         "is_active": True,
#         "message": "Session is active",
#         "data": {
#             "session_id": session["id"],
#             "start_time": session["start_time"]
#         }
#     }), 200



from flask import Blueprint, jsonify, request
from database import get_db_connection

sessions_bp = Blueprint('sessions', __name__)


@sessions_bp.route('/start', methods=['POST'])
def start_session():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (is_active) VALUES (1)"
    )
    conn.commit()
    new_id = cursor.lastrowid

    session = conn.execute(
        "SELECT * FROM sessions WHERE id = ?", (new_id,)
    ).fetchone()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Session started",
        "data": {
            "session_id": session["id"],
            "start_time": session["start_time"],
            "is_active": bool(session["is_active"])
        }
    }), 200


@sessions_bp.route('/end', methods=['POST'])
def end_session():
    data = request.get_json()
    session_id = data.get("session_id")

    if not session_id:
        return jsonify({"success": False, "message": "Session ID is required"}), 400

    conn = get_db_connection()

    session = conn.execute(
        "SELECT * FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()

    if not session:
        conn.close()
        return jsonify({"success": False, "message": "Session not found"}), 404

    if not session["is_active"]:
        conn.close()
        return jsonify({"success": False, "message": "Session is already ended"}), 400

    conn.execute("""
        UPDATE sessions 
        SET is_active = 0, end_time = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (session_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Session ended",
        "data": {
            "session_id": session_id,
            "is_active": False
        }
    }), 200


@sessions_bp.route('/status', methods=['GET'])
def get_session_status():
    conn = get_db_connection()

    session = conn.execute(
        "SELECT * FROM sessions WHERE is_active = 1"
    ).fetchone()

    conn.close()

    if not session:
        return jsonify({
            "success": True,
            "is_active": False,
            "message": "No active session"
        }), 200

    return jsonify({
        "success": True,
        "is_active": True,
        "message": "Session is active",
        "data": {
            "session_id": session["id"],
            "start_time": session["start_time"]
        }
    }), 200