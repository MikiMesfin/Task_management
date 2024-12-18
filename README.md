# Task Management API

A robust Django REST API for managing tasks and categories with user authentication, task sharing, and recurring tasks functionality.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-5.1-green.svg)](https://djangoproject.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔐 User Authentication and Authorization
- 📋 Task Creation and Management
- 🔄 Recurring Tasks
- 📁 Task Categories
- 🤝 Task Sharing
- 📅 Due Date Tracking
- 📧 Email Notifications
- 🔍 Advanced Filtering
- 📱 REST API
- 📚 API Documentation (Swagger/ReDoc)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MikiMesfin/task-management-api.git
   cd task-management-api
   ```

2. Create and activate a virtual environment:
   - On Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints
Here are the main API endpoints available in the Task Management API:

### User Registration and Authentication
- **POST /register/** – Register a new user
- **POST /login/** – Log in a user
- **POST /token/refresh/** – Refresh JWT token

### Task Management
- **GET /tasks/** – List all tasks
- **POST /tasks/** – Create a new task
- **GET /tasks/drafts/** – List user's draft tasks
- **GET, PUT, DELETE /tasks/<task_id>/** – Retrieve, update, or delete a specific task

### Task Features
- **POST /tasks/<task_id>/complete/** – Mark a specific task as complete
- **POST /tasks/<task_id>/incomplete/** – Mark a specific task as incomplete
- **GET /tasks/completed/** – List all completed tasks

### Filtering and Sorting
- **GET /tasks/category/<category_id>/** – Filter tasks by category
- **GET /tasks/priority/<priority>/** – Filter tasks by priority
- **GET /tasks/sorted/** – Sort tasks by due date or priority

## Authentication
This project uses JWT (JSON Web Token) for authentication. To access protected endpoints, include a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## Testing
To run the test suite:
```bash
python manage.py test
```

## Deployment
To deploy the Task Management API on platforms like Heroku or PythonAnywhere, follow these steps:

1. Create an account on your chosen platform.
2. Create a new app in the platform's dashboard.
3. Set environment variables:
   - SECRET_KEY
   - DEBUG (set to False for production)
   - Database settings (e.g., PostgreSQL for production)
4. Deploy your code using Git:
   - On Heroku: `git push heroku main`
   - On PythonAnywhere: Follow their Django deployment guide.
5. Test your deployed API by accessing the public URL provided by the platform.

## Contributing
Contributions are welcome! To contribute to the Task Management API:

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any inquiries or feedback, please reach out to: mikimesfin45@gmail.com
