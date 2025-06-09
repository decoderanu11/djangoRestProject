# Customer Management API

A Django REST API for customer management with JWT authentication and PostgreSQL integration.

## Features

- **JWT Authentication**: Secure token-based authentication
- **Customer CRUD**: Complete customer management operations
- **PostgreSQL**: Robust database backend
- **Search & Pagination**: Advanced querying capabilities
- **Input Validation**: Comprehensive data validation
- **UUID Primary Keys**: Secure, non-sequential identifiers

## Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Validation**: Custom serializer validators

## API Endpoints

### Authentication
```
POST /api/register/        - User registration
POST /api/token/          - Get JWT tokens
POST /api/token/refresh/  - Refresh JWT token
```

### Customer Management
```
GET    /api/customers/           - List customers (with search & pagination)
POST   /api/customers/           - Create customer
GET    /api/customers/{uuid}/    - Get specific customer
PUT    /api/customers/{uuid}/    - Update customer
DELETE /api/customers/{uuid}/    - Delete customer
```

### Query Parameters
```
GET /api/customers/?search=john     - Search by name or email
GET /api/customers/?ordering=-name  - Order by field (prefix - for desc)
GET /api/customers/?page=2          - Pagination
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### 2. Clone Repository
```bash
git clone https://github.com/decoderanu11/djangoRestProject.git
cd djangoRestProject
```

### 3. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. PostgreSQL Setup

#### Using PostgreSQL locally
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE djangorest-db;
CREATE USER api_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE djangorest-db TO api_user;
\q
```
or visit official site for more information https://www.postgresql.org/

### 6. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 7. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/api/`

## Usage Examples

### 1. Register User
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "strongpassword123",
    "password_confirm": "strongpassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Get JWT Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "strongpassword123"
  }'
```

### 3. Create Customer
```bash
curl -X POST http://127.0.0.1:8000/api/customers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "mobile": "+1234567890",
    "address": "123 Main St, City, State"
  }'
```

### 4. List Customers
```bash
curl -X GET http://127.0.0.1:8000/api/customers/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Search Customers
```bash
curl -X GET "http://127.0.0.1:8000/api/customers/?search=john" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure
```
djangoRestProject/
├── customers/           # Customer app
│   ├── models.py       # Customer model
│   ├── serializers.py  # API serializers
│   ├── views.py        # API views
│   └── urls.py         # URL routing
├── users/              # Authentication app
│   ├── serializers.py  # User serializers
│   ├── views.py        # Auth views
│   └── urls.py         # Auth URLs
├── djangoRestProject/            # Main project
│   ├── settings.py     # Django settings
│   └── urls.py         # Root URL config
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Error Handling

The API returns consistent error responses:

```json
{
  "error": "Validation failed",
  "details": {
    "email": ["Customer with this email already exists."]
  }
}
```

## Security Features

- JWT token authentication
- Password validation
- SQL injection protection (Django ORM)
- CORS configuration
- Input sanitization
- UUID primary keys (non-sequential)
