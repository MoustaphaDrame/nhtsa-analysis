# NHTSA Analysis

Backend application built with Python and FastAPI to retrieve, process, and analyze vehicle data from the NHTSA APIs.

The project currently provides vehicle catalog endpoints and complaint analysis, with PostgreSQL used to cache vehicle catalog data.

## Tech Stack

- Python 3.10
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pytest
- Ruff
- mypy
- Docker
- Docker Compose
- GitHub Actions

## Project Structure

```text
nhtsa-analysis/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── clients/
│   ├── db/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── tests/
├── alembic/
├── frontend/
├── .github/
│   └── workflows/
├── Dockerfile
├── compose.yaml
├── alembic.ini
├── requirements.txt
└── README.md
```

## Architecture

The backend is organized into several layers with distinct responsibilities:

- **API**: FastAPI routes and HTTP exception handling.
- **Services**: application and business logic.
- **Repositories**: database access.
- **Clients**: communication with external NHTSA APIs.
- **Schemas**: API data models.
- **Database**: SQLAlchemy configuration and persistence models.

## Running the Application with Docker

Build and start the application and PostgreSQL database:

```bash
docker compose up --build
```

The API is then available at:

```text
http://localhost:8000
```

FastAPI interactive documentation is available at:

```text
http://localhost:8000/docs
```

To stop the containers:

```bash
docker compose down
```

## Database Migrations

Database schema changes are managed with Alembic.

Apply all migrations:

```bash
alembic upgrade head
```

## Tests

Run the test suite with:

```bash
pytest -v
```

## Code Quality

Run Ruff linting:

```bash
ruff check .
```

Check code formatting:

```bash
ruff format --check .
```

Run static type checking:

```bash
mypy app
```

## Continuous Integration

The project uses GitHub Actions for continuous integration.

The CI pipeline currently performs:

1. Dependency installation
2. Ruff linting
3. Ruff formatting check
4. mypy static type checking
5. Alembic database migrations
6. Pytest test suite

The workflow uses a PostgreSQL service container so database-related tests and migrations can run in an isolated CI environment.

## External Data Sources

Vehicle and complaint data are retrieved from NHTSA APIs, including the Vehicle Product Information Catalog (vPIC) API and the NHTSA complaints API.