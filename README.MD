# SaleScope Backend

SaleScope is a simple platform that helps local shops understand their sales.  
This backend is built with **Python** and **FastAPI**. It allows stores to save products, register sales, and get basic reports and demand predictions.

---

##  Features

- Register products and daily sales  
- View simple reports:
  - Best-selling products  
  - Days with higher sales  
  - Weekly average sales  
- Basic demand prediction using:
  - Moving averages  
  - Simple linear regression  
- Authentication system  
- REST API ready to connect with a Next.js frontend  

---

##  Tech Stack

- **Python**  
- **FastAPI**  
- **PostgreSQL** or **MongoDB**  
- **SQLAlchemy**  
- **Pydantic**  
- **Uvicorn** (development server)

---

##  Project Structure

```bash
    SaleScope-Backend/
    ├── backend/
    │   ├── app/
    │   │   ├── analysis/
    │   │   ├── config.py
    │   │   ├── database.py
    │   │   ├── main.py
    │   │   ├── models/
    │   │   ├── routers/
    │   │   ├── schemas/
    │   │   └── services/
    │   ├── run.py
    │   └── venv/
    ├── .env
    ├── .gitignore
    ├── README.MD
    └── requirements.txt
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/IntegrativeProject/Salescope-Backend.git
```


### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
```bash
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up environment variables
Create a `.env` file in the root directory and add the following variables:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/salescope
SECRET_KEY=your-secret-key
```

### 6. Run the application
```bash
python run.py
```

### 7. Access the API
Open your browser and navigate to `http://localhost:8000` to access the API documentation.

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

##  API Endpoints (basic)

- `POST /products` – add a product  
- `POST /sales` – register a sale  
- `GET /reports/daily` – see daily sales  
- `GET /reports/prediction` – demand prediction  

---

##  Future Work

- Better machine learning models  
- Role-based authentication  
- Admin panel  
- Full integration with the Next.js frontend  

---

##  License

This project is open source. You can use it for learning and personal projects.