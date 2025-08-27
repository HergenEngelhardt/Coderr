# Coderr

Coderr is a freelancer platform API built with Django REST Framework backend. It connects customers with freelance programmers, allowing businesses to offer services and customers to place orders with an integrated review system.

## Features

- User authentication and authorization
- Create and manage user profiles (Customer/Business)
- Create and manage service offers with multiple pricing tiers
- Order management system
- Review and rating system
- Role-based permissions (Customer, Business, Admin)

## Technology Stack

- **Backend**: Django 5.2.5, Django REST Framework 3.16.1
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: JWT token-based authentication
- **Image Handling**: Pillow for profile pictures and offer images
- **API Features**: Filtering, pagination, search functionality

## Prerequisites

- Python 3.8+
- Git
- Web browser

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/HergenEngelhardt/Coderr.git
cd Coderr
```

### 2. Set up virtual environment
```bash
python -m venv .venv
```

**On Windows:**
```bash
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Database setup
```bash
python manage.py migrate
```

### 5. Create a superuser
```bash
python manage.py createsuperuser
```

### 6. (Optional) Load sample data
```bash
python manage.py loaddata fixtures/sample_data.json
```

## Running the Project

### Start the backend server
```bash
python manage.py runserver
```

The server will start at http://127.0.0.1:8000/

### Access the application
- **API**: http://127.0.0.1:8000/api/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **Frontend**: Open your frontend files in a local development server

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/registration/` | User registration |
| `/api/login/` | User authentication |
| `/api/profile/{id}/` | Profile management |
| `/api/profiles/business/` | Business profile listings |
| `/api/profiles/customer/` | Customer profile listings |
| `/api/offers/` | Offer management |
| `/api/offerdetails/{id}/` | Offer detail management |
| `/api/orders/` | Order management |
| `/api/reviews/` | Review and rating system |
| `/api/base-info/` | Platform statistics |

## Development

### Code Quality
```bash
# Format code
black .

# Lint code  
flake8 .
```

### Database Operations
```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Production Deployment

1. Set `DEBUG=False` in your environment
2. Configure proper database (PostgreSQL recommended)
3. Set up proper CORS settings
4. Use environment variables for sensitive data
5. Configure static file serving

## Troubleshooting

### Common Issues
- **Migration errors**: Run `python manage.py migrate --fake-initial`
- **Permission errors**: Ensure proper file permissions on database
- **CORS errors**: Check CORS settings in settings.py

## Support

For issues and questions, please check the documentation or create an issue in the repository.