import json
from datetime import datetime, timezone
from extensions import db

# 1. Menu Item Model
class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., Hot Coffee, Cold Coffee, Bakery, Dessert
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(300), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=4.5)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "is_available": self.is_available,
            "rating": self.rating,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }


# 2. Customer Order Model
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120), nullable=True)
    items_json = db.Column(db.Text, nullable=False)  # Order items stored as JSON string
    total_amount = db.Column(db.Float, nullable=False)
    order_type = db.Column(db.String(30), default='Dine-in')  # Dine-in, Takeaway, Delivery
    table_number = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(30), default='Pending')  # Pending, Preparing, Ready, Completed, Cancelled
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        try:
            parsed_items = json.loads(self.items_json)
        except Exception:
            parsed_items = self.items_json

        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_email": self.customer_email,
            "items": parsed_items,
            "total_amount": self.total_amount,
            "order_type": self.order_type,
            "table_number": self.table_number,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }


# 3. Table Reservation Model
class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120), nullable=True)
    guest_count = db.Column(db.Integer, nullable=False)
    reservation_date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    reservation_time = db.Column(db.String(20), nullable=False)  # e.g., 18:30
    special_requests = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='Pending')  # Pending, Confirmed, Cancelled
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_email": self.customer_email,
            "guest_count": self.guest_count,
            "reservation_date": self.reservation_date,
            "reservation_time": self.reservation_time,
            "special_requests": self.special_requests,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }


# 4. Customer Review Model
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }
