from extensions import db
from models import MenuItem, Review

SAMPLE_MENU_ITEMS = [
    {
        "name": "Espresso Intenso",
        "category": "Hot Coffee",
        "price": 2.50,
        "description": "Rich, bold and aromatic classic Italian espresso shot.",
        "image_url": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=500",
        "is_available": True,
        "rating": 4.8
    },
    {
        "name": "Creamy Cappuccino",
        "category": "Hot Coffee",
        "price": 3.80,
        "description": "Balanced blend of espresso, velvety steamed milk and rich milk foam.",
        "image_url": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=500",
        "is_available": True,
        "rating": 4.9
    },
    {
        "name": "Vanilla Latte",
        "category": "Hot Coffee",
        "price": 4.20,
        "description": "Smooth espresso with steamed milk and a delicate touch of vanilla.",
        "image_url": "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=500",
        "is_available": True,
        "rating": 4.7
    },
    {
        "name": "Caramel Macchiato",
        "category": "Hot Coffee",
        "price": 4.50,
        "description": "Freshly brewed espresso, vanilla syrup topped with rich caramel drizzle.",
        "image_url": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=500",
        "is_available": True,
        "rating": 4.9
    },
    {
        "name": "Nitro Cold Brew",
        "category": "Cold Coffee",
        "price": 4.50,
        "description": "Slow-brewed for 12 hours, smooth and creamy cold brew coffee.",
        "image_url": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=500",
        "is_available": True,
        "rating": 4.8
    },
    {
        "name": "Iced Mocha Frappuccino",
        "category": "Cold Coffee",
        "price": 4.90,
        "description": "Delightful blend of rich chocolate mocha, coffee, ice and whipped cream.",
        "image_url": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=500",
        "is_available": True,
        "rating": 4.6
    },
    {
        "name": "French Butter Croissant",
        "category": "Bakery",
        "price": 2.80,
        "description": "Freshly baked, golden, flaky croissant made with pure butter.",
        "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500",
        "is_available": True,
        "rating": 4.7
    },
    {
        "name": "Blueberry Crumble Muffin",
        "category": "Bakery",
        "price": 3.20,
        "description": "Soft and moist muffin packed with wild blueberries and crunchy crumble topping.",
        "image_url": "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=500",
        "is_available": True,
        "rating": 4.6
    },
    {
        "name": "New York Cheesecake",
        "category": "Dessert",
        "price": 5.00,
        "description": "Silky smooth cream cheese over a crunchy graham cracker crust.",
        "image_url": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=500",
        "is_available": True,
        "rating": 4.9
    },
    {
        "name": "Molten Chocolate Lava Cake",
        "category": "Dessert",
        "price": 5.50,
        "description": "Warm dark chocolate cake with a rich molten chocolate center.",
        "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500",
        "is_available": True,
        "rating": 5.0
    }
]

SAMPLE_REVIEWS = [
    {
        "customer_name": "John Doe",
        "rating": 5,
        "comment": "The caramel macchiato was absolutely amazing! Great cozy cafe atmosphere."
    },
    {
        "customer_name": "Emily Smith",
        "rating": 5,
        "comment": "Best cappuccino and fresh croissants in town. Will definitely visit again!"
    }
]

def seed_database():
    """Populate database with initial cafe menu items and reviews."""
    if MenuItem.query.first() is None:
        for item_data in SAMPLE_MENU_ITEMS:
            item = MenuItem(**item_data)
            db.session.add(item)
        print("-> Sample menu items seeded successfully.")

    if Review.query.first() is None:
        for rev_data in SAMPLE_REVIEWS:
            review = Review(**rev_data)
            db.session.add(review)
        print("-> Sample reviews seeded successfully.")

    db.session.commit()
