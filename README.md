# Coderr - Freelancer Platform API

A Django REST Framework based platform for connecting customers with freelance programmers. This API provides comprehensive endpoints for user management, service offers, orders, and reviews.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **User Profiles**: Separate customer and business user profiles
- **Service Offers**: Business users can create offers with multiple pricing tiers
- **Order Management**: Customers can place orders and track their status
- **Review System**: Customers can review business users
- **Admin Interface**: Full Django admin interface for platform management

## Tech Stack

- **Backend**: Django 5.2.5
- **API Framework**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (development)
- **Image Handling**: Pillow
- **Filtering**: django-filter
- **CORS**: django-cors-headers

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd coderr
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Documentation

### Authentication Endpoints

#### Register User
- **POST** `/api/registration/`
- Creates new user with profile
- Body: `{"username": "string", "email": "string", "password": "string", "repeated_password": "string", "type": "customer|business"}`

#### Login User  
- **POST** `/api/login/`
- Authenticates user and returns JWT token
- Body: `{"username": "string", "password": "string"}`

### Profile Endpoints

#### Get/Update Profile
- **GET/PATCH** `/api/profile/{user_id}/`
- Retrieve or update user profile details
- Authentication required

#### List Business Profiles
- **GET** `/api/profiles/business/`
- Returns all business user profiles
- Authentication required

#### List Customer Profiles
- **GET** `/api/profiles/customer/`
- Returns all customer user profiles  
- Authentication required

### Offer Endpoints

#### List/Create Offers
- **GET/POST** `/api/offers/`
- List all offers (with filtering) or create new offer
- POST requires business user authentication
- Query params: `creator_id`, `min_price`, `max_delivery_time`, `search`, `ordering`

#### Get/Update/Delete Offer
- **GET/PATCH/DELETE** `/api/offers/{offer_id}/`
- Manage specific offers
- PATCH/DELETE require owner authentication

#### Get Offer Detail
- **GET** `/api/offerdetails/{detail_id}/`
- Get specific offer detail package
- Authentication required

### Order Endpoints

#### List/Create Orders
- **GET/POST** `/api/orders/`
- List user's orders or create new order
- POST requires customer authentication
- Body for POST: `{"offer_detail_id": integer}`

#### Update Order Status
- **PATCH** `/api/orders/{order_id}/`
- Update order status (business users only)
- Body: `{"status": "in_progress|completed|cancelled"}`

#### Delete Order
- **DELETE** `/api/orders/{order_id}/`
- Delete order (admin only)

#### Order Statistics
- **GET** `/api/order-count/{business_user_id}/`
- Get count of in-progress orders for business user
- **GET** `/api/completed-order-count/{business_user_id}/`
- Get count of completed orders for business user

### Review Endpoints

#### List/Create Reviews
- **GET/POST** `/api/reviews/`
- List reviews (with filtering) or create new review
- POST requires customer authentication
- Query params: `business_user_id`, `reviewer_id`, `ordering`

#### Update/Delete Review
- **PATCH/DELETE** `/api/reviews/{review_id}/`
- Update or delete review (owner only)

### Base Information

#### Platform Statistics
- **GET** `/api/base-info/`
- Get platform statistics (public endpoint)
- Returns: review count, average rating, business profile count, offer count

## Project Structure

```
coderr/
├── core/                   # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── auth_app/              # Authentication functionality
│   └── api/
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
├── profile_app/           # User profiles
│   ├── models.py
│   ├── admin.py
│   └── api/
├── offer_app/             # Service offers
│   ├── models.py
│   ├── admin.py
│   └── api/
├── order_app/             # Order management
│   ├── models.py
│   ├── admin.py
│   └── api/
├── review_app/            # Review system
│   ├── models.py
│   ├── admin.py
│   └── api/
├── base_app/              # Platform statistics
│   └── api/
├── media/                 # User uploaded files
├── requirements.txt       # Python dependencies
└── manage.py
```

## Key Features & Business Logic

### User Types
- **Customer**: Can place orders and write reviews
- **Business**: Can create offers and manage orders

### Offer System
- Each offer must have exactly 3 details: Basic, Standard, Premium
- Details include price, delivery time, revisions, and features
- Automatic calculation of minimum price and delivery time

### Order Workflow
1. Customer selects offer detail
2. Order created with details copied from offer
3. Business user can update order status
4. Order progresses through: in_progress → completed/cancelled

### Review System
- Customers can review business users
- One review per customer per business user
- Ratings from 1-5 stars
- Reviews affect platform statistics

## Security & Permissions

- JWT token authentication for protected endpoints
- Role-based permissions (customer vs business users)
- Object-level permissions for profile/offer/order ownership
- Admin-only access for sensitive operations

## Development Guidelines

### Code Standards
- PEP8 compliant code formatting
- Comprehensive docstrings for all classes and methods
- Maximum 14 lines per function/method
- No commented code or print statements in production

### Testing
- Minimum 95% test coverage required
- Unit tests for all business logic
- Integration tests for API endpoints

## Deployment Notes

### Environment Variables
Create `.env` file for production:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
```

### Production Settings
- Change `DEBUG = False`
- Set proper `ALLOWED_HOSTS`
- Use PostgreSQL or MySQL for production database
- Configure static/media file serving
- Set up proper CORS origins

## Admin Interface

Access Django admin at `/admin/` to:
- Manage users and profiles
- Monitor offers and orders  
- Moderate reviews
- View platform statistics

## API Testing

Use tools like Postman or curl to test endpoints:

```bash
curl -X POST http://127.0.0.1:8000/api/registration/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","repeated_password":"testpass123","type":"customer"}'

curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

curl -X GET http://127.0.0.1:8000/api/offers/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Contributing

1. Follow the established code structure and conventions
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure PEP8 compliance
5. Submit pull requests for review

## License

This project is proprietary software. All rights reserved.

## Support

For technical issues or questions, please contact the development team.
