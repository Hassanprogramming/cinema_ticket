# Cinema Ticket Booking System

This is a web-based cinema booking system built with **Django**, **Django REST framework**, **PostgreSQL**, and **Docker**. It supports:

* Cinema rooms & scheduled movies
* sees available movies (with title, date and time) for the selected room
* User clicks on a movie, after which user sees available and not available seats for the selected
movie.
* Admin panel for managing movies, rooms, and seats
* JWT-based API authentication

---

## Features

* Schedule movies per room
* Manage seat layout and bookings
* JWT Authentication (using SimpleJWT)
* Dockerized for development & production

---

## Requirements

* Docker & Docker Compose
* (Optional) Python 3.12+ and pip if running locally without Docker

---

## Project Structure

```
cinema_ticket/
├── cinema/               # Main app (Rooms, Movies, Seats, Bookings)
├── cinema_ticket/               # Django ASGI/Uvicorn config
├── static/               # Static files collected for production
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Running with Docker

### 1. Clone the Repo

```bash
git clone https://github.com/your-user/cinema-ticket.git
cd cinema-ticket
```

### 2. Build and Start

```bash
docker compose up --build
```

> The project defaults to **DEBUG=True**. You can switch it in `docker-compose.yml`.

### 3. Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```
* for accessing the adminpanel with the username and password created for superuser
      
      http://localhost:8000/admin/ 
     
---

## Authentication

This project uses **JWT tokens** via `rest_framework_simplejwt`.

### Login Endpoint:

```http
POST /api/token/
{
  "username": "admin",
  "password": "yourpassword"
}
```

### Response:

```json
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```

### Refresh Token:

```http
POST /api/token/refresh/
{
  "refresh": "JWT_REFRESH_TOKEN"
}
```

Token lifetime can be customized in `settings.py`:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
}
```

## Development Notes

### Local Setup Without Docker (Optional)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
PROJECT_DEBUG=True uvicorn cinema_ticket.asgi:application --reload --host 0.0.0.0 --port 8000
```

---

## Deployment

For production, be sure to:

* Set `PROJECT_DEBUG=False`
* Set `DJANGO_ALLOWED_HOSTS`
* Use a production WSGI/ASGI server (e.g., gunicorn/uvicorn)
* Serve static files via WhiteNoise or a reverse proxy (e.g., Nginx)

---

## .dockerignore

```dockerignore
__pycache__
*.sqlite3
*.env
*.log
*.db
.env
.vscode/
.idea/
.venv/
media/
staticfiles/
```

---

## .gitignore

```gitignore
__pycache__/
*.db
*.sqlite3
*.log
.env
.venv/
.env/
staticfiles/
media/
.DS_Store
.vscode/
.idea/
```

## API Documentation
* This project uses drf-spectacular to auto-generate API docs.

* The OpenAPI schema is available at:

      http://localhost:8000/api/schema/

* The interactive Swagger UI docs are available at:
      
      http://localhost:8000/api/docs/

* The interactive Redoc UI is available at:
        
      http://localhost:8000/api/schema/redoc/

