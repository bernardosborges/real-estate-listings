# 🏡 Real Estate Listings Backend

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.99-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)
![Tests](https://img.shields.io/badge/Tests-PyTest-orange)

## 📌 Overview

This project is a backend API for property listings, designed for real estate agents and property owners to publish and manage properties for sale.

It applies **Clean Architecture principles** to clearly separate business rules from application logic and infrastructure concerns, ensuring maintainability, testability, and long-term evolution.

The API is intended to be consumed by multiple client application-web, mobile, or third-party platforms, while keeping the domain logic consistent and independent of tech choices.



## 🚧 Project Status

Status: **In development**



## 🎯 Purpose

This project provides a backend foundation that enables the development of user-focused applications. Unlike many existing real estate systems that prioritize internal convenience, it emphasizes **structured, reliable, up-to-date and flexible property records**, which are the cornerstone of trustworthy user experience.
By combining **Clean Architecture** with disciplined domain modeling, the API ensures maintainability, flexibility, and long-term evolution while empowering developers to build client applications that users actually enjoy.



## 🧠 Architecture Principles

- **Flexible Domain Modeling**: Property features and amenities are represented through **tags** rather than fixed fields, allowing the system to handle diverse property types and future requirements without schema changes.
- **Separation of Concerns**: Each layer has a clear responsibility (Domain, Application, Infrastructure, API), allowing business rules to evolve independently of frameworks and databases.
- **Domain-Centric Design**: Business logic around property listings is the core of the system, decoupled from technology and UI decisions.
- **Infrastructure as a Detail**: FastAPI, database and third party services are replaceable implementation details, not part of the core domain.
- **Data Integrity First**: Structured, robust and standardized property records ensure reliable information for client applications.
- **Testability & Maintainability**: Designed for unit and integration testing, making long-term maintenance predictable and safe.
- **User-Centric Orientation**: Backend supports the creation of applications that prioritize end-user experience over internal convenience.
- **Scalability & Extensibility**: System can grow with new features, integrations, and user types without breaking the core logic.



## 🏗️ Architecture Overview

### Domain Layer

**Responsibilities**:
- Defines business concepts and invariants
- Enforce business rules
- Independent from frameworks, databases, or external services

**Contains**:
- Entities
- Value objects
- Enums
- Domain exceptions

**Note:** This layer represents the core of the business and does NOT know other layers.


### Application Layer

**Responsibilities**:
- Execute application-specific workflows
- Coordinate domain objects
- Enforce application rules
- Control transaction boundaries

**Contains**:
- Use cases
- Application services
- DTOs
- Interfaces for external services
- Application exceptions

**Note:** This layer knows what needs to happen, but not how it is implemented.


### Infrastructure Layer

**Responsibilities**:
- Database access
- ORM models
- External service integration
- Hashing, messaging, caching, etc

**Contains**:
- Repository implementations
- ORM models
- External APIs clients
- Infrastructure exceptions

**Note:** This layer depends on the application layer, never the opposite.


### Interfaces / API Layer

**Responsibilities**:
- HTTP endpoints
- Request/response schemas
- Input validation
- Error translation (exceptions -> HTTP responses)

**Contains**:
- Controllers (routers)
- Schemas
- Dependency injection

**Note:** This layer converts HTTP concepts into application concepts, never leaking HTTP into the core.



## 🔐 Error Handling Strategy

- Domain exceptions represent business rule violations
- Application exceptions represent use case failures
- Infrastructure exceptions represent technical failures

The API layer translates these exceptions into appropriate HTTP responses without leaking internal details.



## 🧪 Testing Strategy

- Domain logic is fully testable without frameworks
- Use cases can be tested using mocks for repositories and services
- Infrastructure is tested separately
- Clear separation enables fast and reliable tests



## 🧰 Tech Stack

- **Language**: [Python](https://docs.python.org/3.13/)
- **Server**: [Uvicorn](https://uvicorn.dev/)
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/latest/)
- **Database**: [PostgreSQL](https://www.postgresql.org/docs/)
- **ORM**: [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- **Testing**: [PyTest](https://docs.pytest.org/en/stable/)



## 📝 Example

```
# Create a new property (authentication required)

POST /properties
Content-Type: application/json

{
    "description": "Apartamento com CEP automático",
    "price": 200000,
    "private_area": 80,
    "address": {
        "zip_code": "90020-000"
        "country": "BR",
        "state": "RS",
        "city": "Porto Alegre",
        "neighborhood": "Centro Histórico",
        "street": "Rua dos Andradas",
        "number": "420",
        "complement": "1101",
        "latitude": -29.263545,
        "longitude": -51.736234,
        "confidence": 1.0,
        "provider": "google"
    }
}

```



## ▶️ Running the Project

```
# Linux / macOS
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## ▶️ Running with Docker

For development, the backend and database can run fully in containers, no local setup required:
```
# Build and start the containers forcing env.local
docker-compose --env-file .env.local -f docker-compose.dev.yml up --build -d

# The backend applies all Alembic migrations automatically when starting.

# Access the backend
https://localhost:8000

# To stop and remove containers
docker-compose -f docker-compose.dev.yml down

# Database persistence is configured via Docker volumes, data is kept even if the containers stop.
```

If you want to reset the database, you can run scripts inside the database container or simply remove the volume:
```
docker volume rm realestatelistings-backend_postgres_data
```

- Use **.env.local** for development environment variables.
- Use **.env** for production.

The following environment variables are required:
```
# ==== POSTGRES DATABASE ====
DB_HOST=                            # Hostname of the database (e.g. "db" for development)
DB_PORT=                            # Database port (default: 5432)
DB_NAME=                            # Database name
DB_USER=                            # Database username
DB_PASSWORD=                        # Database password

# ==== AWS S3 STORAGE ====
AWS_ACCESS_KEY_ID=""                # Your AWS access key
AWS_SECRET_ACCESS_KEY=""            # Your AWS secret key
AWS_REGION=""                       # AWS region (e.g. "us-east-1")
AWS_S3_BUCKET=""                    # AWS S3 bucket name

# === AUTH ===
SECRET_KEY=""                       # Secret key for JWT tokens
ALGORITHM=""                        # Algorithm for JWT (default: "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=        # Token expiration in minutes (default: 60)

# === GEOCODING ===
GOOGLE_CODING_API_KEY=""            # Your API key for Google Maps / Geocoding services
```


## 🔥 Next Steps
- Property clustering for maps
- Financial simulator for property affordability and mortgage calculations
- Likes system to desired/absent amenities in properties
- Chat-based property search using an agent bot to interact with users
- Setup CI/CD and automated tests
- Expose Model-Context-Protocol interface for AI agents



## 📎 Final Notes

This project is intended as a **reference backend** for building user-centric property listing applications using Clean Architecture principles. Contribuitions, feedback, and suggestions are welcome.
