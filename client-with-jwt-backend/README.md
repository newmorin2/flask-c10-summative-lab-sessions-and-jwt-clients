# Notes API Backend

## A secure Flask REST API backend for a personal Notes application.
The API provides user authentication using JWT, password hashing with Bcrypt, database migrations, CRUD operations for notes, pagination, and user-based access control.

Users can only view, create, update, and delete their own notes.

## Features
- User registration and authentication
- JWT-based authentication
- Secure password hashing using Flask-Bcrypt
- User-owned notes resource
- Full CRUD operations
- Pagination on notes endpoint
- Protected routes
- User data isolation
- Database migrations using Flask-Migrate

## Technologies Used
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- Flask-RESTful
- SQLite
- Postman

## Setup Instructions
1. Clone the repository
```
git clone <repository-url>
```

Navigate into the backend folder:
```
cd backend
2. Create a virtual environment
python -m venv venv
```

2. Activate the environment.
```
Windows
venv\Scripts\activate
macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

## Database Setup

1. Initialize Flask-Migrate:
```
flask db init

Create a migration:

flask db migrate -m "create users and notes tables"
```

2. Apply migrations:
```
flask db upgrade

The SQLite database will be created:

instance/notes.db
Running the Application
```
3. Start the Flask server:
```
python app.py

The API will run on:

http://localhost:5555
```

## API Endpoints
### Authentication Routes
Method	Endpoint	Description
POST	/signup	Create a new user account
POST	/login	Authenticate a user
GET	/me	Get current logged-in user
Notes Routes

All notes routes require JWT authentication.

## Create Note
POST /notes

Headers:

Authorization: Bearer <token>

Body:

{
    "title": "Workout",
    "content": "Completed a 5km run"
}

Response:

{
    "message": "Note created",
    "note": {
        "id": 1,
        "title": "Workout",
        "content": "Completed a 5km run"
    }
}

## Get All Notes
GET /notes

Supports pagination:

GET /notes?page=1&per_page=5

Response:

{
    "notes": [],
    "page": 1,
    "pages": 2,
    "total": 10
}

## Get Single Note
GET /notes/<id>

Example:

GET /notes/1
Update Note
PATCH /notes/<id>

Example:

{
    "title": "Updated title"
}
Delete Note
DELETE /notes/<id>

Response:

{
    "message": "Note deleted"
}