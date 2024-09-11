# AHP Project

This Django project, named `ahp_project`, implements an Analytic Hierarchy Process (AHP) API. It consists of two main apps: `users` for user management and `ahp_api` for AHP calculations and project management.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Project](#running-the-project)
6. [API Endpoints](#api-endpoints)
7. [Models](#models)
8. [Testing](#testing)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Project Structure

```
ahp_project/
│
├── ahp_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── ahp_api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
└── requirements.txt
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ahp_project.git
   cd ahp_project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory and add the following variables:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

2. Update the database settings in `ahp_project/settings.py` if needed.

## Running the Project

1. Apply migrations:
   ```
   python manage.py migrate
   ```

2. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

3. Start the development server:
   ```
   python manage.py runserver
   ```

The project should now be running at `http://127.0.0.1:8000/`.

## API Endpoints

### User Management

- Register: `POST /users/register/`
- Login: `POST /users/login/`

### AHP API

- Calculate AHP: `POST /api/calculate/`
- User Projects: `GET /api/projects/`

## Models

### AHPProject

The `AHPProject` model in `ahp_api/models.py` stores the following information:

- user (ForeignKey to User)
- project_name (CharField)
- criteria (JSONField)
- alternatives (JSONField)
- pairwise_matrix (JSONField)
- alternative_matrices (JSONField)
- ranking_data (JSONField)
- ranking_list (JSONField)
- alternative_scores (JSONField)
- weights (JSONField)
- consistency_ratio (FloatField)

## Testing

To run the tests for the project:

```
python manage.py test
```

To test the APIs, you can use tools like [Postman](https://www.postman.com/) or [curl](https://curl.se/). Here are some example API calls:

1. Register a new user:
   ```
   curl -X POST http://127.0.0.1:8000/users/register/ -H "Content-Type: application/json" -d '{"username":"testuser", "password":"testpassword"}'
   ```

2. Login:
   ```
   curl -X POST http://127.0.0.1:8000/users/login/ -H "Content-Type: application/json" -d '{"username":"testuser", "password":"testpassword"}'
   ```

3. Calculate AHP (replace `your_auth_token` with the token received after login):
   ```
   curl -X POST http://127.0.0.1:8000/api/calculate/ -H "Authorization: Token your_auth_token" -H "Content-Type: application/json" -d '{
     "project_name": "My AHP Project",
     "criteria": ["Criteria1", "Criteria2", "Criteria3"],
     "alternatives": ["Alt1", "Alt2", "Alt3"],
     "pairwise_matrix": [[1, 2, 3], [0.5, 1, 2], [0.33, 0.5, 1]],
     "alternative_matrices": [
       [[1, 2, 3], [0.5, 1, 2], [0.33, 0.5, 1]],
       [[1, 3, 2], [0.33, 1, 0.5], [0.5, 2, 1]],
       [[1, 2, 0.5], [0.5, 1, 0.33], [2, 3, 1]]
     ]
   }'
   ```

4. Get user projects:
   ```
   curl -X GET http://127.0.0.1:8000/api/projects/ -H "Authorization: Token your_auth_token"
   ```

Remember to replace `your_auth_token` with the actual token you receive after logging in.

For more detailed information about each endpoint and its required payload, please refer to the API documentation or consult the project's developers.
