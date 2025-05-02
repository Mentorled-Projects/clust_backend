# Clust API

Clust API is a backend service built with FastAPI that provides an event and group management platform. It supports user roles such as organizers and attendees, allowing users to create and manage groups, events, RSVPs, feedback, and file uploads.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
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
   ```
   ENVIRONMENT=development
   POSTGRES_SERVER=localhost
   POSTGRES_USER=youruser
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_DB=yourdb
   SECRET_KEY=your_secret_key
   BACKEND_CORS_ORIGINS=http://localhost,http://localhost:3000
   ```

5. Run database migrations using Alembic:
   ```bash
   alembic upgrade head
   ```

## Usage

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Overview

- **Root Endpoint**: `GET /`  
  Returns a welcome message:  
  ```json
  { "message": "Welcome to the Clust API!" }
  ```

- **Healthcheck Endpoint**: `GET /healthcheck`  
  Returns the status of the API:  
  ```json
  { "status": "ok" }
  ```

## Data Models

- **User**  
  Represents a user with roles `organizer` or `attendee`.  
  Fields: `name`, `email`, `password_hash`, `role`.  
  Relationships: organizes events and groups, RSVPs to events, provides feedback, uploads files.

- **Group**  
  Represents a group created by an organizer.  
  Fields: `name`, `description`, `organizer_id`.

- **Event**  
  Represents an event organized by a user.  
  Fields: `title`, `description`, `location`, `start_time`, `end_time`, `organizer_id`.  
  Relationships: feedbacks and files associated with the event.

- **RSVP**  
  Tracks user attendance status for events.

- **Feedback**  
  User feedback related to events.

- **File**  
  Files uploaded by users related to events.

## Database

The project uses PostgreSQL as the database backend with asynchronous support via `asyncpg`. Database schema migrations are managed using Alembic.

## Configuration

Configuration is managed via environment variables and the `.env` file. Key settings include:

- `ENVIRONMENT`: Application environment (development, production)
- `POSTGRES_*`: Database connection details
- `SECRET_KEY`: Secret key for JWT and security
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins for the API

## License

This project is licensed under the MIT License. See the LICENSE file for details.
