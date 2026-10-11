from flask import Blueprint, jsonify
from models import MenuItem

# Blueprint for cafe routes
cafe_bp = Blueprint('cafe', __name__)


# Basic Health Check Route
@cafe_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Cafe REST API is running!",
        "version": "1.0.0"
    }), 200


# Home Page Route: Returns menu items (name, photo/image_url, price, description, etc.)
@cafe_bp.route('/', methods=['GET'])
@cafe_bp.route('/api/home', methods=['GET'])
def get_home_data():
    items = MenuItem.query.all()
    return jsonify([item.to_dict() for item in items]), 200

