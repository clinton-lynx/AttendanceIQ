



# from flask import Flask, jsonify
# from flask_cors import CORS
# import config
# from routes.students import students_bp
# from routes.auth import auth_bp
# from routes.sessions import sessions_bp
# from routes.attendance import attendance_bp
# from database import init_db
# from seed import seed_students

# def create_app():
#     app = Flask(__name__)
#     CORS(app)


#       # Initialize database and seed students on every startup
#     init_db()
#     seed_students()


#     app.register_blueprint(auth_bp, url_prefix='/api/auth')
#     app.register_blueprint(students_bp, url_prefix='/api/students')
#     app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
#     app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

#     @app.route('/')
#     def index():
#         return jsonify({
#             "success": True,
#             "message": "AttendanceIQ API is Running",
#             "version": "1.0.0"
#         })

#     @app.errorhandler(404)
#     def not_found(e):
#         return jsonify({"success": False, "message": "Endpoint not found"}), 404

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(host=config.HOST, port=config.PORT, debug=True)



from flask import Flask, jsonify
from flask_cors import CORS
import config
from routes.students import students_bp
from routes.auth import auth_bp
from routes.sessions import sessions_bp
from routes.attendance import attendance_bp
from database import init_db, get_db_connection
from seed import seed_students


def run_migrations():
    """Fix sessions table if session_name column exists."""
    conn = get_db_connection()
    try:
        columns = [row[1] for row in conn.execute("PRAGMA table_info(sessions)").fetchall()]
        if "session_name" in columns:
            conn.executescript("""
                ALTER TABLE sessions RENAME TO sessions_old;

                CREATE TABLE sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    end_time DATETIME,
                    is_active BOOLEAN DEFAULT 1
                );

                INSERT INTO sessions SELECT id, start_time, end_time, is_active FROM sessions_old;
                DROP TABLE sessions_old;
            """)
            conn.commit()
            print("Migration complete: removed session_name column.")
        else:
            print("No migration needed.")
    finally:
        conn.close()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize database and seed students on every startup
    init_db()
    run_migrations()
    seed_students()

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

    @app.route('/')
    def index():
        return jsonify({
            "success": True,
            "message": "AttendanceIQ API is Running",
            "version": "1.0.0"
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Endpoint not found"}), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=config.HOST, port=config.PORT, debug=True)