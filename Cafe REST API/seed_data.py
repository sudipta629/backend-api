from extensions import db
from models import MenuItem

SAMPLE_MENU_ITEMS = [
    {
        "name": "Espresso Intenso",
        "category": "Hot Coffee",
        "price": 149.00,
        "description": "Rich, bold and aromatic classic Italian espresso shot.",
        "image_url": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=500",
        "is_available": True,
        "rating": 4.8
    },
    {
        "name": "Creamy Cappuccino",
        "category": "Hot Coffee",
        "price": 229.00,
        "description": "Balanced blend of espresso, velvety steamed milk and rich milk foam.",
        "image_url": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=500",
        "is_available": True,
        "rating": 4.9
    },
    {
        "name": "Vanilla Latte",
        "category": "Hot Coffee",
        "price": 249.00,
        "description": "Smooth espresso with steamed milk and a delicate touch of vanilla.",
        "image_url": "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=500",
        "is_available": True,
        "rating": 4.7
    },
    {
        "name": "Caramel Macchiato",
        "category": "Hot Coffee",
        "price": 279.00,
        "description": "Freshly brewed espresso, vanilla syrup topped with rich caramel drizzle.",
        "image_url": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=500",
        "is_available": True,
        "rating": 4.9
    },
    {
        "name": "Nitro Cold Brew",
        "category": "Cold Coffee",
        "price": 299.00,
        "description": "Slow-brewed for 12 hours, smooth and creamy cold brew coffee.",
        "image_url": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=500",
        "is_available": True,
        "rating": 4.8
    },
    {
        "name": "Iced Mocha Frappuccino",
        "category": "Cold Coffee",
        "price": 349.00,
        "description": "Delightful blend of rich chocolate mocha, coffee, ice and whipped cream.",
        "image_url": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=500",
        "is_available": True,
        "rating": 4.6
    },
    {
        "name": "French Butter Croissant",
        "category": "Bakery",
        "price": 189.00,
        "description": "Freshly baked, golden, flaky croissant made with pure butter.",
        "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500",
        "is_available": True,
        "rating": 4.7
    },
    {
        "name": "Blueberry Crumble Muffin",
        "category": "Bakery",
        "price": 199.00,
        "description": "Soft and moist muffin packed with wild blueberries and crunchy crumble topping.",
        "image_url": "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=500",
        "is_available": True,
        "rating": 4.6
    },
    {
        "name": "New York Cheesecake",
        "category": "Dessert",
        "price": 299.00,
        "description": "Silky smooth cream cheese over a crunchy graham cracker crust.",
        "image_url": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=500",
        "is_available": True,
        "rating": 4.9
    },
    {
        "name": "Molten Chocolate Lava Cake",
        "category": "Dessert",
        "price": 349.00,
        "description": "Warm dark chocolate cake with a rich molten chocolate center.",
        "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500",
        "is_available": True,
        "rating": 5.0
    }
]

def seed_database():
    """Populate or update database with initial cafe menu items in INR (₹)."""
    for item_data in SAMPLE_MENU_ITEMS:
        item = MenuItem.query.filter_by(name=item_data["name"]).first()
        if item:
            item.price = item_data["price"]
            item.category = item_data["category"]
            item.description = item_data["description"]
            item.image_url = item_data["image_url"]
            item.rating = item_data["rating"]
        else:
            db.session.add(MenuItem(**item_data))

    db.session.commit()
    print("-> Menu items updated with INR (₹) prices successfully.")
