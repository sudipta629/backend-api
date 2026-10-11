import sys
from flask import Flask
from config import Config
from extensions import db, cors
from routes import cafe_bp
from seed_data import seed_database

# Ensure UTF-8 console output on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def create_app():
    # 1. Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # 2. Configure extensions (Database & CORS)
    db.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    # 3. Register blueprints
    app.register_blueprint(cafe_bp)

    # 4. Create database tables and seed sample data
    with app.app_context():
        db.create_all()
        seed_database()

    return app

app = create_app()

if __name__ == '__main__':
    print("==================================================")
    print(" Cafe Website REST API Server is LIVE!")
    print(" Localhost URL:   http://localhost:5000")
    print(" Network URL:     http://0.0.0.0:5000")
    print(" Home Route:      http://localhost:5000/")
    print(" Home API:        http://localhost:5000/api/home")
    print(" Health Check:    http://localhost:5000/api/health")
    print("==================================================")
    app.run(debug=True, host='0.0.0.0', port=5000)
