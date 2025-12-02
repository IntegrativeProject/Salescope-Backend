# SaleScope Backend

SaleScope is a comprehensive e-commerce platform that helps businesses manage their products, process orders, and gain insights into their sales performance. This backend is built with **Python** and **FastAPI**, providing a robust and scalable API for the SaleScope platform. The application follows a clean architecture with a focus on maintainability and testability.

---

## Features

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
- Complete order lifecycle management
- Order items with automatic price calculation
- Order status tracking (pending, processing, completed, cancelled)
- Soft delete with restore capability
- Automatic order total calculation

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

## Tech Stack

- **Framework**: FastAPI (Async-capable)
- **Database**: PostgreSQL (with soft delete support)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **API Documentation**: Swagger UI & ReDoc
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic v2
- **Server**: Uvicorn (ASGI server)
- **Architecture**: Service pattern with dependency injection
- **Testing**: Pytest (with async support)

---

## Project Structure

```
SaleScope-Backend/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── users.py      # User model with authentication
│   │   │   ├── products.py   # Product catalog
│   │   │   ├── orders.py     # Order management
│   │   │   └── order_item.py # Order line items
│   │   │   └── audit_log.py  # Audit trail
│   │   ├── schemas/          # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   ├── orders.py
│   │   │   └── order_item.py  # Order item payloads/responses
│   │   ├── services/         # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── order_service.py   # Order service class
│   │   │   ├── order_item_service.py # Order item service class
│   │   │   ├── users.py      # Legacy service functions (wrappers)
│   │   │   ├── products.py   # Legacy service functions (wrappers)
│   │   │   ├── orders.py     # Legacy service functions (wrappers)
│   │   │   └── order_items.py # Legacy service functions (wrappers)
│   │   ├── routers/          # API routes
│   │   │   ├── __init__.py
│   │   │   ├── users.py      # User endpoints
│   │   │   ├── products.py   # Product endpoints
│   │   │   ├── orders.py     # Order endpoints
│   │   └── order_items.py # Order item endpoints
│   │   ├── database.py       # Database configuration
│   │   └── main.py           # Application entry point
│   ├── .env.example          # Example environment variables
│   ├── requirements.txt      # Project dependencies
│   └── run.py                # Development server script
├── .gitignore
└── README.md
```

---

## Setup

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

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints throughout the codebase
- Document public APIs with docstrings
- Keep functions small and focused
- Use dependency injection for better testability

### Testing
Run the test suite with:
```bash
pytest
```

### Code Quality
We use pre-commit hooks to ensure code quality. Install with:
```bash
pre-commit install
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## API Documentation

### Authentication
Authorization: Bearer <your-jwt-token>

### Available Endpoints

#### Auth (`/auth`)
- **POST** `/auth/register` - Register a new user (hashes password, returns JWT)
- **POST** `/auth/login` - Login with email/password (returns JWT)

#### Users (`/users`)
- **POST** `/users/` - Create a new user (admin/internal, expects pre-hashed `password_hash`)
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

#### Order Items (`/orders/{order_id}/items`)
- **GET** `/orders/{order_id}/items` - List items for an order
- **GET** `/orders/{order_id}/items/{item_id}` - Get a specific order item
- **POST** `/orders/{order_id}/items` - Add a new item to an order
- **PUT** `/orders/{order_id}/items/{item_id}` - Update an order item's quantity
- **DELETE** `/orders/{order_id}/items/{item_id}` - Delete an order item

---

## API Examples (cURL)

Base URL variable:
```bash
BASE_URL=https://integrative-salescope.onrender.com
```

If you use tokens, add: `-H "Authorization: Bearer <token>"`

### Auth

- Register (recommended for creating users)
```bash
curl -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Alice",
    "email": "alice@example.com",
    "password": "pass123",
    "role_name": "customer"
  }'
```

- Login
```bash
curl -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "pass123"
  }'
```

### Users
Note: Use `/auth/register` to create users with a password. The `/users/` create endpoint is admin/internal and expects a pre-hashed `password_hash`.

- List users
```bash
curl "$BASE_URL/users/"
```

- Get user
```bash
curl "$BASE_URL/users/1"
```

- Update user
```bash
curl -X PUT "$BASE_URL/users/1" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Alice Smith" }'
```

- Soft delete user
```bash
curl -X DELETE "$BASE_URL/users/1"
```

- Restore user
```bash
curl -X PUT "$BASE_URL/users/1/restore"
```

### Products

- Create product
```bash
curl -X POST "$BASE_URL/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mouse",
    "description": "USB mouse",
    "price": 25.5,
    "stock": 100
  }'
```

- List products
```bash
curl "$BASE_URL/products/"
```

- Get product
```bash
curl "$BASE_URL/products/1"
```

- Update product
```bash
curl -X PUT "$BASE_URL/products/1" \
  -H "Content-Type: application/json" \
  -d '{ "price": 30.0, "stock": 90 }'
```

- Soft delete product
```bash
curl -X DELETE "$BASE_URL/products/1"
```

- Restore product
```bash
curl -X PUT "$BASE_URL/products/1/restore"
```

### Orders

- Create order (with initial items)
```bash
curl -X POST "$BASE_URL/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "items": [
      { "product_id": 1, "quantity": 2 }
    ]
  }'
```

- List orders
```bash
curl "$BASE_URL/orders/"
```

- Get order
```bash
curl "$BASE_URL/orders/1"
```

- Update order status
```bash
curl -X PUT "$BASE_URL/orders/1" \
  -H "Content-Type: application/json" \
  -d '{ "status": "completed" }'
```

- Soft delete order
```bash
curl -X DELETE "$BASE_URL/orders/1"
```

- Restore order
```bash
curl -X PUT "$BASE_URL/orders/1/restore"
```

### Order Items

- List items in an order
```bash
curl "$BASE_URL/orders/1/items"
```

- Add item to an order
```bash
curl -X POST "$BASE_URL/orders/1/items" \
  -H "Content-Type: application/json" \
  -d '{ "product_id": 1, "quantity": 3 }'
```

- Get a specific item
```bash
curl "$BASE_URL/orders/1/items/1"
```

- Update item quantity
```bash
curl -X PUT "$BASE_URL/orders/1/items/1" \
  -H "Content-Type: application/json" \
  -d '{ "quantity": 5 }'
```

- Delete item
```bash
curl -X DELETE "$BASE_URL/orders/1/items/1"
```

---

## Database Migrations

### Creating Migrations
After making model changes, create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

### Applying Migrations
To apply pending migrations:
```bash
alembic upgrade head
```

### Rollback Migrations
To rollback the last migration:
```bash
alembic downgrade -1
```

## Deploying to Render

We include a `render.yaml` at repo root which defines the web service.

### Steps
- Push this repo to GitHub.
- In Render: New → Web Service → Use "Build and deploy from a repository".
- Render auto-detects `render.yaml`.
- Set environment variables (below) and deploy.

### Required env vars
- `DATABASE_URL` (recommended include `?sslmode=require` on Render):
  - Example: `postgresql://user:pass@host/dbname?sslmode=require`
- `SECRET_KEY` (random string for JWT)
- Optional: `ALGORITHM` (default HS256), `ACCESS_TOKEN_EXPIRE_MINUTES` (default 30)

### The render.yaml we ship
```yml
services:
  - type: web
    name: salescope-backend
    env: python
    plan: free
    rootDir: backend
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    postDeployCommand: alembic upgrade head
    healthCheckPath: /
    autoDeploy: true
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.14
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: "30"
```

Notes:
- The service runs from `backend/` using `uvicorn app.main:app`.
- After each deploy, Alembic runs `upgrade head` automatically.
- Health check hits `/`.

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Follow the code style and add tests for your changes
4. Ensure all tests pass
5. Submit a pull request with a clear description of your changes

### Development Workflow
- Create an issue to discuss your proposed changes
- Write tests for new features
- Update documentation as needed
- Keep commits small and focused
- Write clear commit messages

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