from flask import Blueprint, jsonify, request
from extensions import db
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

