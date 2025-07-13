# Clust API

Clust API is a backend service built with FastAPI that provides an event and group management platform. It supports user roles such as organizers and attendees, allowing users to create and manage groups, events, RSVPs, feedback, and file uploads.

## Project Architecture

- **FastAPI**: Web framework for building the API.
- **PostgreSQL**: Asynchronous database backend using `asyncpg`.
- **Alembic**: Database schema migrations.
- **Redis**: Used for caching and Celery broker.
- **Celery**: Task queue for background jobs.
- **SendGrid**: Email delivery service.
- **JWT**: JSON Web Tokens for authentication and authorization.
- **Pytest & Pytest-Asyncio**: Testing framework for synchronous and asynchronous tests.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Mentorled-Projects/clust_backend
   cd clust_backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file in the root directory. Example variables:

   ```env
   ENVIRONMENT=development
   POSTGRES_SERVER=localhost
   POSTGRES_USER=youruser
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_DB=yourdb
   SECRET_KEY=your_secret_key
   BACKEND_CORS_ORIGINS=http://localhost,http://localhost:3000
   VERIFICATION_BASE_URL=http://localhost:8000
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALGORITHM=HS256
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   SENDGRID_API_KEY=your_sendgrid_api_key
   ```

5. Run database migrations using Alembic:

   ```bash
   alembic upgrade head
   ```

### Database Migrations with Alembic

This project uses Alembic to manage database schema migrations. Alembic is configured to use the database URL from the environment variables defined in your `.env` file.

#### Setting up

- Ensure your `.env` file contains the correct PostgreSQL connection details (`POSTGRES_SERVER`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`).
- Alembic dynamically reads the database URL from the application settings and converts the asyncpg URL to a synchronous psycopg2 URL for migrations.

#### Creating a new migration

After making changes to your SQLAlchemy models, create a new migration script with:

```bash
alembic revision --autogenerate -m "describe your changes"
```

This command will generate a new migration file in the `alembic/versions` directory based on the differences detected in your models and the current database schema.

#### Applying migrations

To apply all pending migrations and update your database schema, run:

```bash
alembic upgrade head
```

#### Additional Alembic commands

- To downgrade the database to a previous migration:

  ```bash
  alembic downgrade <revision>
  ```

- To view the current revision of the database:

  ```bash
  alembic current
  ```

- To show the history of migrations:

  ```bash
  alembic history
  ```

## Usage

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Overview

### Root Endpoint: `GET /`

Returns a welcome message:

```json
{ "message": "Welcome to the Clust API!" }
```

### Healthcheck Endpoint: `GET /healthcheck`

Returns the status of the API:

```json
{ "status": "ok" }
```

## Authentication

The Clust API provides user authentication with email verification and JWT-based access tokens.

### Signup

* **Endpoint**: `POST /api/v1/auth/signup`
* **Description**: Register a new user with email and password. Sends a verification email with a token link.
* **Request Body**:

  ```json
  {
    "email": "user@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "SecurePass123!",
    "password_verify": "SecurePass123!"
  }
  ```
* **Password Requirements**:

  * Minimum 8 characters
  * At least one uppercase letter
  * At least one lowercase letter
  * At least one digit
  * At least one special character (e.g., !@#\$%^&\*())
* **Response**:

  ```json
  { "message": "Verification email sent" }
  ```

### Email Verification

* **Endpoint**: `GET /api/v1/auth/verify-email`
* **Description**: Verify user email by clicking the link sent to the registered email. The token expires in 1 hour.
* **Response**:

  * Success:

    ```json
    { "message": "Email verified successfully" }
    ```
  * Failure (expired or invalid token):

    ```json
    { "message": "Token expired" }
    ```

    or

    ```json
    { "message": "Invalid token" }
    ```

### Login

* **Endpoint**: `POST /api/v1/auth/login`
* **Description**: Authenticate user with email and password. Requires verified email.
* **Request Body**:

  ```json
  {
    "email": "user@example.com",
    "password": "StrongP@ssw0rd!"
  }
  ```
* **Response**:

  * Success:

    ```json
    {
      "access_token": "jwt_token_here",
      "token_type": "bearer"
    }
    ```
  * Failure:

    * Invalid credentials
    * Email not verified

## JWT Access Tokens

* The API uses JWT tokens for authentication.
* Tokens are created with expiration (default 30 minutes).

## Data Models

### User

Represents a user with roles organizer or attendee.

* Fields: `name`, `email`, `password_hash`, `role`, `is_verified`
* Relationships: organizes events and groups, RSVPs to events, provides feedback, uploads files

### Group

Represents a group created by an organizer.

* Fields: `name`, `description`, `organizer_id`

### Event

Represents an event organized by a user.

* Fields: `title`, `description`, `location`, `start_time`, `end_time`, `organizer_id`
* Relationships: feedbacks and files associated with the event

### RSVP

Tracks user attendance status for events.

### Feedback

User feedback related to events.

### File

Files uploaded by users related to events.

## Running Tests

The project uses `pytest` and `pytest-asyncio` for testing.

To run the tests, execute:

```bash
pytest
```

## Configuration

Configuration is managed via environment variables and the `.env` file. Key settings include:

* `ENVIRONMENT`: Application environment (development, production)
* `POSTGRES_*`: Database connection details
* `SECRET_KEY`: Secret key for JWT and security
* `BACKEND_CORS_ORIGINS`: Allowed CORS origins for the API
* `VERIFICATION_BASE_URL`: Base URL used in email verification links
* `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time in minutes
* `ALGORITHM`: JWT signing algorithm
* `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`: Redis connection details
* `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`: Celery configuration
* `SENDGRID_API_KEY`: API key for SendGrid email service

## License

This project is licensed under the MIT License. See the LICENSE file for details.
