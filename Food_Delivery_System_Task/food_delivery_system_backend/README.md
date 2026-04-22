# Food Delivery System Backend

Food Delivery System. Built with Django and Django REST Framework.

## Features
- **User Management**: Authentication and authorization with diffrent roles like Customers, Restaurant Owners, and Delivery Drivers.
- **Restaurant & Menu**: Complete CRUD endpoints for restaurants, menu items, and reviews.
- **Cart & Order Management**: Endpoints for creating shopping carts, placing orders, and tracking order history.
- **API Documentation**: Interactive documentation generated with `drf-spectacular`.

## Requirements
- Python 3.10+
- PostgreSQL
- Redis

## Setup Instructions

1. **Clone the repository and set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Copy the `.env.example` file to `.env` and configure your local Postgres credentials:

4. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## API Documentation
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI Schema: `http://127.0.0.1:8000/api/schema/`
