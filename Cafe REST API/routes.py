import re
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import Blueprint, jsonify, request, current_app
import jwt
from extensions import db
from models import MenuItem, User

# Blueprint for cafe routes
cafe_bp = Blueprint('cafe', __name__)

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


def generate_token(user):
    """Generate a JWT token valid for 7 days."""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
        'iat': datetime.now(timezone.utc)
    }
    secret = current_app.config.get('SECRET_KEY', 'cafe-super-secret-jwt-key-2026-production-ready-32b')
    return jwt.encode(payload, secret, algorithm='HS256')


def token_required(f):
    """Decorator to protect routes requiring JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Authorization token is missing"
            }), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({
                "status": "error",
                "message": "Invalid token format. Please use 'Bearer <token>'"
            }), 401

        token = parts[1]
        try:
            secret = current_app.config.get('SECRET_KEY', 'cafe-super-secret-jwt-key-2026-production-ready-32b')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            current_user = User.query.get(payload.get('user_id'))
            if not current_user:
                return jsonify({
                    "status": "error",
                    "message": "User not found"
                }), 401
        except jwt.ExpiredSignatureError:
            return jsonify({
                "status": "error",
                "message": "Token has expired, please log in again"
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "status": "error",
                "message": "Invalid authentication token"
            }), 401

        return f(current_user, *args, **kwargs)
    return decorated


# ==============================================================================
# Health Check Route
# ==============================================================================
@cafe_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Cafe REST API is running!",
        "version": "1.0.0"
    }), 200


# ==============================================================================
# Authentication Routes (Register & Login - No OTP)
# ==============================================================================

# User Registration (Email, Password, Name)
@cafe_bp.route('/api/auth/register', methods=['POST'])
@cafe_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()

    if not name:
        return jsonify({"status": "error", "message": "Name is required"}), 400

    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400

    if not re.match(EMAIL_REGEX, email):
        return jsonify({"status": "error", "message": "Please enter a valid email address"}), 400

    if not password:
        return jsonify({"status": "error", "message": "Password is required"}), 400

    if len(password) < 6:
        return jsonify({"status": "error", "message": "Password must be at least 6 characters long"}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({
            "status": "error",
            "message": "An account with this email already exists. Please log in."
        }), 409

    try:
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        token = generate_token(new_user)
        return jsonify({
            "status": "success",
            "message": "Registration successful! Welcome to Bean & Brew Cafe.",
            "token": token,
            "user": new_user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"Registration failed: {str(e)}"
        }), 500


# User Login (Email, Password)
@cafe_bp.route('/api/auth/login', methods=['POST'])
@cafe_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({
            "status": "error",
            "message": "Invalid email or password"
        }), 401

    token = generate_token(user)
    return jsonify({
        "status": "success",
        "message": "Login successful! Welcome back.",
        "token": token,
        "user": user.to_dict()
    }), 200


# Get Authenticated User Profile
@cafe_bp.route('/api/auth/me', methods=['GET'])
@cafe_bp.route('/api/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({
        "status": "success",
        "user": current_user.to_dict()
    }), 200


# User Logout
@cafe_bp.route('/api/auth/logout', methods=['POST'])
@cafe_bp.route('/api/logout', methods=['POST'])
def logout():
    return jsonify({
        "status": "success",
        "message": "Logged out successfully"
    }), 200


# ==============================================================================
# Menu Items Routes
# ==============================================================================

# Home & Menu Route: Returns all menu items (Supports ?category=... and ?search=...)
@cafe_bp.route('/', methods=['GET'])
@cafe_bp.route('/api/home', methods=['GET'])
@cafe_bp.route('/api/menu', methods=['GET'])
def get_menu():
    category = request.args.get('category')
    search = request.args.get('search')

    query = MenuItem.query
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(MenuItem.name.ilike(f"%{search}%"))

    items = query.all()
    return jsonify([item.to_dict() for item in items]), 200


# Distinct Categories Route
@cafe_bp.route('/api/menu/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(MenuItem.category).distinct().all()
    return jsonify([cat[0] for cat in categories if cat[0]]), 200


# Get Single Menu Item by ID
@cafe_bp.route('/api/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({"status": "error", "message": "Menu item not found"}), 404
    return jsonify(item.to_dict()), 200

