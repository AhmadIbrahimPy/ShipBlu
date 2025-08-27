# ShipBlu Orders API
This is a Django REST API for managing customer orders. It allows creating, retrieving, updating, and deleting orders, tracking order status changes, and searching/filtering customers and orders. This API is built using Django and Django REST Framework.

## Requirements
- Python 3.13
- Django 4.x
- Django REST Framework
- django-filter
- SQLite (default) or PostgreSQL

## Setup Instructions
Clone the repository: git clone <repository_link> cd <project_folder> Create a virtual environment and activate it: python -m venv venv source venv/bin/activate  # On macOS/Linux venv\Scripts\activate     # On Windows Install dependencies: pip install -r requirements.txt Apply migrations: python manage.py migrate Create a superuser (optional, for admin panel): python manage.py createsuperuser Run the development server: python manage.py runserver The API will be accessible at http://127.0.0.1:8000/.

## API Endpoints
### Customers
List all customers (with search, filter, ordering, pagination): GET /app/customers/?search=Ahmad&ordering=name&page=1 Retrieve a single customer: GET /app/customers/{id}/ Create a new customer: POST /app/customers/ { "name": "Ahmad Ibrahim", "phone_number": "+201130772477" } Update a customer: PATCH /app/customers/{id}/ { "name": "Updated Name" } Delete a customer: DELETE /app/customers/{id}/

### Orders
List all orders (filter by status, search by tracking_number or customer name, pagination): GET /app/orders/?status=CREATED&search=TRACK123&page=1 Retrieve a single order: GET /app/orders/{id}/ Create a new order: POST /app/orders/ { "tracking_number": "TRACK123", "customer_id": 1, "status": "CREATED" } Update order status (only valid transitions): PATCH /app/orders/{id}/ { "status": "PICKED" } Delete an order: DELETE /app/orders/{id}/

### Order Tracking Events (History)
List all tracking events: GET /app/tracking-events/?search=TRACK123 This shows status changes and comments for each order.

## Assumptions
Orders status transitions must follow: CREATED → PICKED → DELIVERED `tracking_number` is unique for each order Pagination is enabled (10 items per page by default) Filtering and searching are supported for Customers and Orders

## Running Tests
To run all tests: python manage.py test This will run all API tests for Customers, Orders, and OrderTrackingEvent functionality.

## Notes
The API is designed for local development; no deployment configuration is included. Admin panel is available at /admin/ if superuser is created. All endpoints follow RESTful conventions and return JSON responses.
