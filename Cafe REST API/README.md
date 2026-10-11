# ☕ Cafe Website REST API

A comprehensive **Python Flask** REST API backend for a cafe or restaurant website. Features menu management, order processing, table reservations, and customer reviews.

---

## 🚀 How to Run

1. Open a terminal and navigate to the project directory:
```bash
cd "d:\coding\backend-api\Cafe REST API"
```

2. Activate the virtual environment (Windows PowerShell):
```powershell
..\venv\Scripts\Activate.ps1
```
*(Or via Command Prompt: `..\venv\Scripts\activate.bat`)*

3. Ensure dependencies are installed:
```bash
pip install -r ..\requirements.txt
```

4. Start the server:
```bash
python run.py
```
The server will run on `http://127.0.0.1:5000`.

---

## 📌 API Endpoints

### 1. Health Check
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Check API server status |

---

### 2. Menu Items
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/menu` | List all menu items (Filters: `?category=Coffee`, `?search=latte`, `?available=true`) |
| `GET` | `/api/menu/categories` | List all distinct categories |
| `GET` | `/api/menu/<id>` | Get details of a specific menu item |
| `POST` | `/api/menu` | Add a new menu item |
| `PUT` / `PATCH` | `/api/menu/<id>` | Update an existing menu item |
| `DELETE` | `/api/menu/<id>` | Delete a menu item |

#### 📝 Add Menu Item Request Body (POST `/api/menu`):
```json
{
  "name": "Iced Hazelnut Latte",
  "category": "Cold Coffee",
  "price": 4.50,
  "description": "Chilled espresso and milk infused with hazelnut syrup.",
  "image_url": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5",
  "is_available": true,
  "rating": 4.8
}
```

---

### 3. Customer Orders
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/orders` | Place a new order |
| `GET` | `/api/orders` | List all orders (Filter: `?status=Pending`) |
| `GET` | `/api/orders/<id>` | Get order details |
| `PATCH` | `/api/orders/<id>/status` | Update order status |

#### 📝 Place Order Request Body (POST `/api/orders`):
```json
{
  "customer_name": "John Doe",
  "customer_phone": "+1234567890",
  "customer_email": "john@example.com",
  "order_type": "Dine-in",
  "table_number": 4,
  "total_amount": 8.00,
  "notes": "Less sugar please",
  "items": [
    {
      "item_id": 1,
      "name": "Espresso Intenso",
      "quantity": 1,
      "price": 2.50
    },
    {
      "item_id": 10,
      "name": "Molten Chocolate Lava Cake",
      "quantity": 1,
      "price": 5.50
    }
  ]
}
```

#### 📝 Update Order Status Request Body (PATCH `/api/orders/<id>/status`):
```json
{
  "status": "Preparing"
}
```
*(Available statuses: `Pending`, `Preparing`, `Ready`, `Completed`, `Cancelled`)*

---

### 4. Table Reservations
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/reservations` | Book a table |
| `GET` | `/api/reservations` | List all reservations (Filters: `?date=2026-10-15`, `?status=Pending`) |
| `PATCH` | `/api/reservations/<id>/status` | Update reservation status (Confirm / Cancel) |

#### 📝 Reservation Request Body (POST `/api/reservations`):
```json
{
  "customer_name": "Sarah Connor",
  "customer_phone": "+1987654321",
  "customer_email": "sarah@example.com",
  "guest_count": 2,
  "reservation_date": "2026-10-15",
  "reservation_time": "19:00",
  "special_requests": "Window side table preferred"
}
```

---

### 5. Customer Reviews
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/reviews` | List all reviews |
| `POST` | `/api/reviews` | Submit a new review |

#### 📝 Submit Review Request Body (POST `/api/reviews`):
```json
{
  "customer_name": "Alex Johnson",
  "rating": 5,
  "comment": "Amazing coffee and wonderful cozy ambiance!"
}
```

---

## 🛠️ Tech Stack
- **Python 3**
- **Flask**
- **Flask-SQLAlchemy** (SQLite)
- **Flask-CORS** (Enables seamless integration with frontend frameworks like React, Vue, Next.js, or HTML/JS)
