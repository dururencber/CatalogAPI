📦 CatalogAPI

A scalable, containerized, and production-ready RESTful Web API built with ASP.NET Core 8, designed following modern Clean Architecture principles and Domain-Driven Design (DDD) fundamentals.

🎯 Project Overview

CatalogAPI serves as a core catalog management service for distributed e-commerce and inventory workflows. It showcases production-grade backend design patterns: decoupled layer structure, database abstraction using Entity Framework Core, stateless security with JWT authentication, secret management, and full containerization via Docker.

✨ Key Architectural Highlights

Layered Architecture: Clear separation of concerns spanning API, Application, Domain, and Infrastructure.

Stateless Security (JWT): Token-based authentication and role-based authorization ([Authorize(Roles = "...")]) to isolate sensitive administrative endpoints.

DTO & Data Isolation: Request and response schemas abstracted via Data Transfer Objects (DTOs) to prevent sensitive entity leakage.

Code-First ORM: Relational schema migrations, indexing, and seeds managed through Entity Framework Core and PostgreSQL.

Credential Isolation: Local secrets secured via .NET Secret Manager (dotnet user-secrets); container environments configured using decoupled environment variables.

Dockerized Workflows: Automated build and runtime packaging with multi-stage Dockerfile and docker-compose.yml declarations.

🏗️ Architecture & Layer Structure

CatalogAPI/
├── src/
│   ├── CatalogAPI.API/            # Controllers, middleware, dependency injection & Swagger setup
│   ├── CatalogAPI.Application/    # DTOs, CQRS/Service contracts, validation rules & business logic
│   ├── CatalogAPI.Domain/         # Domain entities, enums & repository contracts
│   └── CatalogAPI.Infrastructure/ # EF Core DbContext, PostgreSQL mappings & third-party integrations
├── docker-compose.yml             # Orchestration for API & PostgreSQL database
├── Dockerfile                     # Multi-stage production container build
└── README.md                      # Project documentation


🛠️ Tech Stack & Dependencies

Platform / Framework: C# / .NET 8 Web API

Database & ORM: PostgreSQL, Entity Framework Core 8

Authentication: JSON Web Tokens (Bearer Authentication)

API Documentation: Swagger / OpenAPI UI

Containerization: Docker & Docker Compose

Package Management: NuGet

🚀 Local Development & Setup

Prerequisites

.NET 8 SDK

Docker Desktop

Git

Step 1: Clone the Repository

git clone https://github.com/dururencber/CatalogAPI.git
cd CatalogAPI


Step 2: Spin Up Infrastructure (PostgreSQL)

You can launch the PostgreSQL container using Docker Compose:

docker compose up -d


Step 3: Configure Local Secrets

To prevent credential leakage in version control, inject your connection string via the .NET Secret Manager:

cd CatalogAPI.API
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Host=localhost;Port=5432;Database=CatalogDb;Username=postgres;Password=your_secure_password"


Step 4: Apply Database Migrations

Run database migrations to initialize tables and relationships:

dotnet ef database update --project ../CatalogAPI.Infrastructure


Step 5: Run the API

dotnet run


Once running, access the interactive Swagger interface at:

Swagger UI: https://localhost:5001/swagger or http://localhost:5000/swagger

🔒 Security & Best Practices

Zero Credential Exposure: Database strings and cryptographic keys are strictly excluded from git tracking.

Stateless Scalability: JWT-based request signing ensures the service can be horizontally scaled behind an API Gateway or AWS ALB without session stickiness.

Data Protection: Client inputs are strictly validated before hitting the domain layer.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
