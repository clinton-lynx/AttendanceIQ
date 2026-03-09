from flask import Flask, jsonify
from flask_cors import CORS

import config
from routes.auth import auth_bp
from routes.students import students_bp
from routes.sessions import sessions_bp
from routes.attendance import attendance_bp

def create_app():
    app = Flask(__name__)
    
    # Enable Cross-Origin Resource Sharing
    CORS(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

    @app.route('/')
    def index():
        # Serve the single placeholder HTML page
        from flask import send_from_directory
        return send_from_directory('static', 'index.html')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Endpoint not found"}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=config.HOST, port=config.PORT, debug=True)
