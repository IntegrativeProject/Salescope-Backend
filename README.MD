# SaleScope Backend

SaleScope is a comprehensive e-commerce platform that helps businesses manage their products, process orders, and gain insights into their sales performance. This backend is built with **Python** and **FastAPI**, providing a robust and scalable API for the SaleScope platform.

---

## 🚀 Features

### User Management
- User registration and authentication
- Role-based access control (Admin, Staff, Customer)
- User profile management
- Soft delete functionality

### Product Catalog
- CRUD operations for products
- Product categorization and inventory management
- Soft delete support
- Product search and filtering

### Order Processing
- Order creation and management
- Order items handling
- Order status tracking (pending, paid, shipped, cancelled)
- Soft delete with restore capability

### Reporting & Analytics
- Sales reports and analytics
- Best-selling products
- Revenue tracking
- Order history

### Audit Logging
- Comprehensive activity tracking
- Change history
- User action logging

---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **API Documentation**: Swagger UI & ReDoc
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic
- **Server**: Uvicorn (ASGI server)

---

##  Project Structure

```
SaleScope-Backend/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   ├── orders.py
│   │   │   ├── order_item.py
│   │   │   └── audit_log.py
│   │   ├── schemas/          # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   └── orders.py
│   │   ├── services/         # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   └── orders.py
│   │   ├── routers/          # API routes
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   └── orders.py
│   │   ├── database.py       # Database configuration
│   │   └── main.py           # Application entry point
│   ├── .env.example          # Example environment variables
│   ├── requirements.txt      # Project dependencies
│   └── run.py                # Development server script
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/IntegrativeProject/Salescope-Backend.git
cd SaleScope-Backend
```

### 2. Create and activate a virtual environment
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the `backend` directory with the following variables:
```env
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_PORT=your-db-port
DB_NAME=your-db-name
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run database migrations
```bash
alembic upgrade head
```

### 6. Start the development server
```bash
uvicorn app.main:app --reload
```

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

## 📚 API Documentation

### Authentication
Authorization: Bearer <your-jwt-token>

### Available Endpoints

#### Users (`/users`)
- **POST** `/users/` - Create a new user
- **GET** `/users/` - List all users (paginated)
- **GET** `/users/{user_id}` - Get user by ID
- **PUT** `/users/{user_id}` - Update user
- **DELETE** `/users/{user_id}` - Soft delete user
- **POST** `/users/{user_id}/restore` - Restore soft-deleted user

#### Products (`/products`)
- **POST** `/products/` - Create a new product
- **GET** `/products/` - List all products (paginated)
- **GET** `/products/{product_id}` - Get product by ID
- **PUT** `/products/{product_id}` - Update product
- **DELETE** `/products/{product_id}` - Soft delete product
- **POST** `/products/{product_id}/restore` - Restore soft-deleted product

#### Orders (`/orders`)
- **POST** `/orders/` - Create a new order
- **GET** `/orders/` - List all orders (paginated)
- **GET** `/orders/{order_id}` - Get order by ID
- **PUT** `/orders/{order_id}` - Update order status
- **DELETE** `/orders/{order_id}` - Soft delete order
- **POST** `/orders/{order_id}/restore` - Restore soft-deleted order

---

## 🔄 Migrations

To create a new migration after making model changes:
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🚀 Future Work

- Enhanced reporting and analytics
- Integration with payment gateways
- Email notifications
- Inventory management
- Multi-tenant support
- API rate limiting
- Caching layer for better performance
- More comprehensive test coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For support or questions, please open an issue on the [GitHub repository](https://github.com/IntegrativeProject/Salescope-Backend).

---
*SaleScope Backend - Powering your e-commerce needs*