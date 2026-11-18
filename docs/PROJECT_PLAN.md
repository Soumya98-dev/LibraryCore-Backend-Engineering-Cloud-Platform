# LibraryCore: Backend Engineering & Cloud Platform

**Target completion:** December 15, 2026

**Purpose:** Portfolio project for backend engineering and cloud engineering job applications.

**Resume project title:** LibraryCore — Multi-User Library Management Backend

**Application start date:** January 15, 2027

## Table of Contents

- [1. Project Objective](#1-project-objective)

- [2. Technology Stack](#2-technology-stack)

  - [2.1 Backend](#21-backend)

  - [2.2 Database](#22-database)

  - [2.3 Caching and Background Processing](#23-caching-and-background-processing)

  - [2.4 Authentication and Security](#24-authentication-and-security)

  - [2.5 DevOps and Infrastructure](#25-devops-and-infrastructure)

  - [2.6 Azure Services](#26-azure-services)

  - [2.7 Testing and Performance](#27-testing-and-performance)

- [3. Database Design](#3-database-design)

  - [3.1 Users](#31-users)

  - [3.2 Authors](#32-authors)

  - [3.3 Books](#33-books)

  - [3.4 Idempotency Records](#34-idempotency-records)

  - [3.5 Refresh Tokens](#35-refresh-tokens)

  - [3.6 Database Design Principles](#36-database-design-principles)

  - [3.7 Optional Future Tables](#37-optional-future-tables)

- [4. Functional and Engineering Requirements](#4-functional-and-engineering-requirements)

  - [4.1 Core Backend and Database Engineering](#41-core-backend-and-database-engineering)

  - [4.2 Authentication and Authorization](#42-authentication-and-authorization)

  - [4.3 API Reliability and Data Consistency](#43-api-reliability-and-data-consistency)

  - [4.4 Redis and Distributed Processing](#44-redis-and-distributed-processing)

    - [4.4.1 Caching](#441-caching)

    - [4.4.2 Rate Limiting](#442-rate-limiting)

    - [4.4.3 Background Jobs](#443-background-jobs)

  - [4.5 Testing and Quality Assurance](#45-testing-and-quality-assurance)

  - [4.6 Docker and CI/CD](#46-docker-and-cicd)

- [5. Azure Cloud Deployment](#5-azure-cloud-deployment)

- [6. Performance and Load Testing](#6-performance-and-load-testing)

- [7. Engineering Challenges to Demonstrate](#7-engineering-challenges-to-demonstrate)

- [8. Final Deployment Architecture](#8-final-deployment-architecture)

- [9. Documentation Requirements](#9-documentation-requirements)

- [10. Definition of Done](#10-definition-of-done)

- [11. Project Execution Guidelines](#11-project-execution-guidelines)

- [12. Certification Goal](#12-certification-goal)

- [13. Portfolio Goals](#13-portfolio-goals)

- [14. Project Scope and Final Objective](#14-project-scope-and-final-objective)

- [15. Implementation Order](#15-implementation-order)

- [16. Current Progress and Immediate Next Task](#16-current-progress-and-immediate-next-task)

- [17. Timeline and Career Milestone](#17-timeline-and-career-milestone)

> **Reference convention:** Use section numbers when discussing requirements (for example, “see §4.4.1 for caching” or “§5.4 for the deployment pipeline”).

## 1. Project Objective

Expand my existing FastAPI Personal Library API into **LibraryCore**, a production-style, multi-user backend system that demonstrates practical backend engineering, relational database design, distributed systems fundamentals, application security, performance optimization, reliability and cloud deployment.

The objective is not simply to implement CRUD endpoints or demonstrate familiarity with different technologies.

The focus is on understanding and solving real engineering problems involving:

- Database consistency and transaction management.

- Concurrency and race conditions.

- Authentication and authorization.

- Database performance and query optimization.

- Caching and cache invalidation.

- Background job processing.

- API reliability and fault handling.

- Containerization and CI/CD.

- Cloud infrastructure and deployment.

- Monitoring and performance measurement.

The final application should demonstrate the ability to design, implement, test, deploy, monitor and troubleshoot a backend system.

## 2. Technology Stack

### 2.1 Backend

- Python

- FastAPI

- SQLAlchemy 2.0

- Pydantic

### 2.2 Database

- PostgreSQL

- Alembic for database migrations

### 2.3 Caching and Background Processing

- Redis

- RQ (Redis Queue)

### 2.4 Authentication and Security

- JWT authentication

- Secure password hashing

- Role-Based Access Control (RBAC)

- Refresh-token rotation and revocation

- Secure secrets management

### 2.5 DevOps and Infrastructure

- Docker

- Docker Compose

- GitHub Actions

- Azure Container Registry

- Azure Container Apps

### 2.6 Azure Services

- Azure Database for PostgreSQL

- Azure Managed Redis, subject to regional availability and budget

- Azure Key Vault

- Managed Identity

- Application Insights

- Azure Monitor

### 2.7 Testing and Performance

- Pytest

- Unit and integration testing

- Locust for load testing

## 3. Database Design

The application should initially use five core tables.

### 3.1 Users

Responsible for authentication, authorization and library ownership.

Suggested fields:

- id (primary key)

- email (unique)

- password_hash

- role (admin/user)

- is_active

- created_at

- updated_at

Requirements:

- Secure password hashing.

- Unique email constraint.

- Role-based authorization.

- Active/inactive account handling.

A separate Roles table is unnecessary for the initial two-role system.

### 3.2 Authors

Represents the shared author catalogue.

Suggested fields:

- id (primary key)

- name

- biography

- created_at

- updated_at

Requirements:

- One-to-many relationship with Books.

- Appropriate validation and constraints.

- Admin-controlled author creation, modification and deletion.

- Authenticated users can read author information.

### 3.3 Books

Represents books belonging to individual users.

Suggested fields:

- id (primary key)

- title

- description

- publication_year

- author_id (foreign key referencing Authors)

- owner_id (foreign key referencing Users)

- created_at

- updated_at

Requirements:

- Maintain the existing one-to-many Author–Book relationship.

- Introduce user-specific book ownership.

- Users should only access and modify their own books.

- Admins should have appropriate administrative access.

- Prevent unauthorized access to another user's resources.

The same author can have multiple books, and different users can own their own entries for the same book.

### 3.4 Idempotency Records

Responsible for preventing duplicate operations when clients retry requests.

Suggested fields:

- id (primary key)

- user_id

- idempotency_key

- request_hash

- response_status

- response_body (JSONB)

- created_at

- expires_at

Requirements:

- Unique constraint on (user_id, idempotency_key).

- Store the original request hash.

- Store the completed response.

- Return the original result for a repeated request with the same key and payload.

- Reject reuse of the same key with a different payload.

- Handle simultaneous requests using database constraints and transactions.

- Define how expired records are cleaned up.

### 3.5 Refresh Tokens

Responsible for persistent refresh-token management.

Suggested fields:

- id (primary key)

- user_id

- token_hash

- token_family_id

- expires_at

- revoked_at

- created_at

Requirements:

- Store hashed refresh tokens rather than plaintext tokens.

- Implement refresh-token rotation.

- Revoke previously used tokens after rotation.

- Handle expired and revoked tokens.

- Detect refresh-token reuse where applicable.

- Support logout and token revocation.

### 3.6 Database Design Principles

- Use proper foreign keys and constraints.

- Define NOT NULL and unique constraints where appropriate.

- Add indexes based on actual query patterns.

- Use Alembic for all schema changes.

- Understand transaction boundaries and rollback.

- Use PostgreSQL as the primary development database early in the project.

- Migrate existing SQLite data appropriately or recreate development data when safe.

- Avoid unnecessary tables and abstractions.

### 3.7 Optional Future Tables

- AuditLogs for persistent administrative activity tracking.

- ExportRecords if persistent export history becomes necessary.

These are not required for the initial implementation.

## 4. Functional and Engineering Requirements

### 4.1 Core Backend and Database Engineering

- Complete CRUD operations for Books and Authors.

- Implement proper Author–Book relationships.

- Introduce PostgreSQL.

- Use SQLAlchemy 2.0 ORM patterns.

- Implement Alembic migrations.

- Define appropriate foreign keys, unique constraints and NOT NULL constraints.

- Implement indexes based on query patterns.

- Understand and implement transaction boundaries.

- Handle transaction rollback and database failures.

- Implement pagination, filtering and sorting.

- Investigate N+1 queries.

- Optimize database access using appropriate ORM loading strategies.

- Use EXPLAIN ANALYZE to inspect query execution plans.

### 4.2 Authentication and Authorization

- Implement user registration and login.

- Securely hash passwords.

- Implement JWT access and refresh tokens.

- Implement token expiration and refresh handling.

- Implement refresh-token rotation and revocation.

- Introduce Admin and Regular User roles.

- Implement role-based endpoint authorization.

- Enforce resource ownership.

- Prevent unauthorized access to other users' books.

- Protect sensitive endpoints and configuration.

### 4.3 API Reliability and Data Consistency

- Implement consistent API error responses.

- Use appropriate HTTP status codes.

- Implement request validation using Pydantic.

- Implement idempotency for selected write operations.

- Prevent duplicate resource creation during concurrent requests.

- Handle simultaneous updates and database conflicts.

- Understand transaction isolation and locking.

- Introduce request IDs and structured application logging.

- Implement consistent error handling for database and external service failures.

### 4.4 Redis and Distributed Processing

#### 4.4.1 Caching

- Implement Redis caching for frequently accessed resources.

- Introduce cache expiration using TTL.

- Implement cache invalidation after create, update and delete operations.

- Understand cache-aside patterns.

- Handle Redis unavailability gracefully.

- Test stale-cache scenarios and concurrent access.

#### 4.4.2 Rate Limiting

- Implement Redis-backed rate limiting.

- Apply limits based on authenticated users or client IPs.

- Ensure rate-limit updates are atomic under concurrent requests.

- Define behaviour when Redis becomes unavailable.

#### 4.4.3 Background Jobs

- Implement asynchronous background processing using RQ.

- Run workers independently of FastAPI.

- Implement a practical background task such as CSV library export or report generation.

- Handle job failures and retries.

- Track job status using RQ and Redis.

- Understand what happens when a worker crashes or restarts.

### 4.5 Testing and Quality Assurance

Use Pytest for automated testing.

Implement:

- Unit tests for services and business logic.

- Integration tests against PostgreSQL and Redis.

- Authentication and authorization tests.

- Database constraint tests.

- Transaction rollback tests.

- Concurrent request tests.

- Idempotency tests under simultaneous requests.

- Cache invalidation tests.

- Rate-limiting tests.

- Background job execution and failure tests.

- API validation and error-response tests.

Testing should be introduced alongside each feature, not postponed until the end.

### 4.6 Docker and CI/CD

#### 4.6.1 Docker

- Create production-oriented Dockerfiles.

- Use Docker Compose for local development.

- Containerize FastAPI and the background worker independently.

- Configure PostgreSQL and Redis containers.

- Use environment-based configuration.

- Implement appropriate health checks.

#### 4.6.2 GitHub Actions

Implement CI/CD workflows that:

- Run linting and formatting checks.

- Execute automated tests.

- Validate database migrations.

- Build Docker images.

- Publish images to Azure Container Registry.

- Deploy the application to Azure.

Use secure GitHub-to-Azure authentication, preferably OpenID Connect, rather than storing long-lived cloud credentials in repository secrets.

## 5. Azure Cloud Deployment

Deploy the application using Microsoft Azure.

### 5.1 Infrastructure

- Create a personal Azure account and subscription.

- Understand Azure Portal and Azure CLI.

- Create and organize Azure resource groups.

- Understand regions, resource provisioning and pricing.

- Deploy FastAPI using Azure Container Apps.

- Store Docker images in Azure Container Registry.

- Use Azure Database for PostgreSQL.

- Configure Azure Managed Redis, subject to availability and budget.

- Deploy the background worker as a separate containerized service.

### 5.2 Security

- Store application secrets in Azure Key Vault.

- Configure Managed Identity for supported Azure service-to-service authentication.

- Avoid hardcoded credentials and secrets.

- Configure database authentication securely.

- Understand Azure RBAC and access control.

- Restrict unnecessary public access to infrastructure.

### 5.3 Monitoring and Reliability

- Integrate Application Insights.

- Implement structured logging.

- Implement request correlation IDs.

- Implement health and readiness endpoints.

- Monitor API failures and latency.

- Monitor database and container resource usage.

- Understand how to troubleshoot deployment and connectivity failures.

- Investigate application exceptions using telemetry.

### 5.4 Deployment Pipeline

The deployment pipeline should follow a controlled sequence:

1. Code changes pushed to GitHub.

2. Automated linting and tests.

3. Docker image built.

4. Image published to Azure Container Registry.

5. Database migrations executed as a controlled deployment step.

6. Azure Container Apps updated.

7. Health checks performed.

8. Deployment success or failure reported.

Database migrations must not independently execute from every API replica.

## 6. Performance and Load Testing

Use Locust to evaluate API performance.

Measure:

- Requests per second (throughput).

- p50 latency.

- p95 latency.

- p99 latency.

- Error rate.

- Database query performance.

- Cached versus uncached response performance.

Conduct baseline and optimized performance tests.

Test scenarios should include:

- Reading books with pagination.

- Filtering books.

- Authenticated write operations.

- Concurrent requests.

- Redis caching enabled and disabled.

- Increasing concurrent user loads.

Document:

- Test environment and resource configuration.

- Dataset size.

- Number of concurrent users.

- Test duration.

- Bottlenecks identified.

- Optimizations implemented.

- Before-and-after performance results.

Never report unmeasured performance improvements.

## 7. Engineering Challenges to Demonstrate

The project should explicitly demonstrate the following:

1. Consistency: Prevent inconsistent database state during concurrent operations.

2. Concurrency: Handle simultaneous requests, duplicate submissions and conflicting updates.

3. Database performance: Use indexes, query plans and appropriate ORM loading strategies.

4. Cache consistency: Prevent stale cached data after database modifications.

5. Reliability: Handle database, Redis and background worker failures.

6. Security: Enforce authentication, authorization and secure secret management.

7. Observability: Identify failures and performance bottlenecks through logs and telemetry.

8. Scalability: Understand how API replicas and background workers behave under increasing load.

The objective is to understand the engineering trade-offs behind these implementations, not merely to make them work.

## 8. Final Deployment Architecture

The final logical architecture should consist of:

- FastAPI API service deployed on Azure Container Apps.

- Independent background worker deployed as a separate containerized service.

- Azure Database for PostgreSQL for persistent storage.

- Azure Managed Redis for caching, rate limiting and job queues.

- Azure Key Vault for secrets.

- Azure Container Registry for Docker images.

- GitHub Actions for CI/CD.

- Application Insights for monitoring and diagnostics.

The architecture should support independent API and worker scaling.

## 9. Documentation Requirements

The GitHub repository must include:

- Project overview and technical objectives.

- Architecture diagram.

- Database schema and entity relationship diagram.

- API documentation.

- Local setup instructions.

- Environment configuration documentation.

- Database migration instructions.

- Testing instructions.

- Docker and deployment instructions.

- CI/CD workflow explanation.

- Azure infrastructure overview.

- Load-testing methodology and results.

- Engineering decisions and trade-offs.

- Known limitations and future improvements.

Include a dedicated section explaining important engineering decisions, such as:

- Why PostgreSQL was selected.

- Why Redis caching was introduced.

- How cache invalidation works.

- How idempotency is enforced.

- How transactions protect data consistency.

- How the application handles external service failures.

- How database queries were optimized.

- How deployment and monitoring work.

## 10. Definition of Done

The project is considered complete when:

- Core API functionality is implemented.

- Authentication and authorization work correctly.

- User-specific book ownership is enforced.

- PostgreSQL migrations and constraints are implemented.

- Transactions and idempotency work correctly.

- Redis caching and rate limiting work correctly.

- Background jobs execute independently.

- Unit and integration tests pass.

- Concurrency scenarios have been tested.

- Dockerized services run locally.

- GitHub Actions CI/CD pipeline works.

- The application is deployed on Azure.

- Key Vault and supported Managed Identity integrations are configured.

- Application Insights receives application telemetry.

- Load testing has been completed with documented results.

- Repository documentation is sufficient for another developer to run and understand the system.

## 11. Project Execution Guidelines

Act as a Senior Backend Engineering Mentor.

I want to implement this project myself and understand the engineering decisions behind it.

Do not write the implementation code for me unless I explicitly request it.

### 11.1 Task Workflow

1. Inspect the existing repository before suggesting modifications.

2. Explain the engineering problem being solved.

3. Explain the relevant concepts and trade-offs.

4. Identify the files and components I should work on.

5. Break the task into manageable implementation steps.

6. Define acceptance criteria.

7. Suggest appropriate tests.

8. Wait for me to implement the changes.

9. Review my implementation and identify design flaws, security problems, performance issues and incorrect assumptions.

### 11.2 Additional Rules

- Never restart or rewrite the existing project without justification.

- Do not dump complete code implementations.

- Do not introduce unnecessary technologies or abstractions.

- Do not skip important engineering concepts.

- Do not move to the next task before reviewing the current task.

- Challenge incorrect technical decisions.

- Prioritize correctness and understanding over implementation speed.

Give me exactly ONE next task at a time.

## 12. Certification Goal

- Pass Microsoft Azure Fundamentals (AZ-900).

- Obtain the certification and add it to my resume and LinkedIn.

## 13. Portfolio Goals

- Complete and deploy **LibraryCore — Multi-User Library Management Backend**.

- Have a publicly accessible API or documented deployment.

- Maintain a clean GitHub repository.

- Include architecture documentation and actual performance benchmarks.

- Be able to explain the implementation and engineering trade-offs in technical interviews.

## 14. Project Scope and Final Objective

The project should prioritize backend engineering depth and practical Azure experience.

Avoid adding frontend development, AI features, microservices or unnecessary infrastructure to this project.

The final objective is to demonstrate genuine backend engineering ability, not merely familiarity with a large technology stack.

## 15. Implementation Order

Build the project incrementally in the following order. Do not begin later phases until the current phase has been implemented, tested and reviewed.

### Phase 1 — Complete the Existing API

- Finish Update and Delete operations for Books and Authors.
- Validate Author–Book relationship behaviour.
- Handle missing records and invalid foreign keys.
- Use appropriate HTTP status codes.
- Add tests for CRUD behaviour, validation and relationship constraints.

### Phase 2 — PostgreSQL and Database Migrations

- Introduce PostgreSQL as the primary development database.
- Configure SQLAlchemy 2.0 database access.
- Introduce Alembic.
- Create and apply the initial migration.
- Add the Users table and the `owner_id` relationship on Books.
- Add database constraints and indexes based on actual access patterns.
- Plan how existing SQLite records will be migrated or safely recreated.
- Verify migration upgrade and downgrade behaviour.

### Phase 3 — Authentication, Authorization and Ownership

- Implement user registration and login.
- Implement password hashing and JWT access tokens.
- Implement refresh-token rotation and revocation.
- Enforce Admin and Regular User permissions.
- Enforce user-specific book ownership.
- Add authentication, authorization and ownership tests.

### Phase 4 — API Reliability and Database Correctness

- Implement pagination, filtering and sorting.
- Implement structured errors and request correlation IDs.
- Implement idempotency records and concurrent duplicate-request handling.
- Define transaction boundaries and rollback behaviour.
- Handle conflicting updates and database failures.
- Inspect query plans and address N+1 queries.

### Phase 5 — Redis and Background Processing

- Add Redis to the local Docker Compose environment.
- Implement cache-aside behaviour and TTL.
- Implement cache invalidation.
- Implement atomic Redis-backed rate limiting.
- Implement an independent RQ worker.
- Add a practical export or report-generation job.
- Test Redis and worker failure scenarios.

### Phase 6 — Testing and Containerization

- Build unit and integration tests alongside the implementation.
- Run integration tests against PostgreSQL and Redis.
- Add concurrency and failure-path tests.
- Create production-oriented Dockerfiles.
- Run the API, worker, PostgreSQL and Redis locally using Docker Compose.
- Add health checks and configuration validation.

### Phase 7 — CI/CD and Azure Deployment

- Create GitHub Actions workflows for linting, tests and migration validation.
- Build and publish images to Azure Container Registry.
- Provision Azure resources with cost and regional availability in mind.
- Deploy the API and worker to Azure Container Apps.
- Configure Azure Database for PostgreSQL and managed Redis.
- Configure Key Vault and supported Managed Identity integrations.
- Run database migrations as a controlled release step.
- Configure Application Insights and verify telemetry.

### Phase 8 — Performance, Documentation and Final Review

- Establish a repeatable Locust baseline.
- Measure p50, p95 and p99 latency, throughput and error rate.
- Compare cached and uncached requests.
- Identify and address measured bottlenecks.
- Document the environment, dataset, concurrency and test duration.
- Complete the architecture diagram, database diagram and engineering decision records.
- Verify the deployment and repository from a clean setup.

## 16. Current Progress and Immediate Next Task

### Current implementation status

The existing project currently has:

- FastAPI application.
- SQLAlchemy models for Authors and Books.
- One-to-many Author–Book relationship.
- Create operations for Authors and Books.
- Read operations for Authors and Books.
- SQLite database and session management.

### Immediate next task

Complete Update and Delete operations for the existing Books and Authors resources.

Before changing the architecture:

1. Inspect the existing models, schemas, routes and database session management.
2. Review how the current Create and Read operations are structured.
3. Identify any correctness issues in the existing implementation.
4. Implement Update and Delete incrementally.
5. Add tests for successful updates, successful deletions, missing records, invalid relationships and relevant constraint behaviour.

After this task is reviewed and complete, move to PostgreSQL and Alembic.

Do not restart the project or introduce authentication, Redis or Azure deployment before the existing API and its data model have been reviewed.

## 17. Timeline and Career Milestone

**Project completion target:** December 15, 2026  
**Job application start date:** January 15, 2027  
**Suggested project effort:** Approximately 15–20 focused hours per week during this compressed schedule, adjusted around full-time work. This is an aggressive target and requires strict scope control.

### Certification milestone

- Prepare for Microsoft Azure Fundamentals (AZ-900).
- Target the AZ-900 exam by December 20, 2026.
- Use the PwC certification voucher if its eligibility, coverage and expiry terms permit.
- Keep the certification profile associated with a personal Microsoft account.
- Add the certification to the resume and LinkedIn after passing.

### Project milestones

The project deadline has been moved forward to **December 15, 2026**. This is an aggressive four-week schedule. Work in small increments, keep the scope frozen and prioritize a working, tested deployment over optional sophistication.

| Period | Target outcome |
|---|---|
| November 18–22, 2026 | Finish Update and Delete for Books and Authors; add tests; move the development database to PostgreSQL; configure Alembic and create the initial migration |
| November 23–28, 2026 | Add the Users table; implement password hashing, JWT access/refresh tokens, RBAC and user-specific book ownership; migrate the existing schema safely |
| November 29–December 3, 2026 | Implement pagination, filtering, structured errors, transaction handling and idempotency; add database constraints and query-focused indexes |
| December 4–7, 2026 | Implement Redis caching and invalidation, rate limiting, and one useful RQ background job; run the API and worker locally with PostgreSQL and Redis |
| December 8–10, 2026 | Complete critical unit/integration tests, concurrency and failure-path tests; create Dockerfiles and Docker Compose; establish GitHub Actions CI for linting, migrations and tests |
| December 11–13, 2026 | Deploy the API to Azure Container Apps; publish the image to Azure Container Registry; connect Azure Database for PostgreSQL; configure Key Vault, supported Managed Identity access and basic Application Insights telemetry |
| December 14–15, 2026 | Run a repeatable Locust test; document p50/p95/p99 latency, throughput and error rate; finish architecture and setup documentation; verify the deployed application and freeze the release |

**Scope control for the December 15 deadline:**

- The required outcome is one correctly deployed API, one independently runnable background worker, a working CI pipeline, core security and data-consistency features, and documented performance results.
- Keep advanced features such as elaborate refresh-token reuse detection, multiple deployment environments, autoscaling experiments, extensive failure-injection scenarios and a sophisticated audit system out of the critical path. Add them only after the required release works.
- Use Docker Compose locally for PostgreSQL and Redis. Provision Azure Managed Redis only if the service is available in the chosen region and the cost fits the budget; otherwise document the Redis hosting choice and keep the local integration fully tested.
- Do not claim a feature is complete until it has been implemented and tested. If a cloud integration cannot be completed safely by December 15, document the limitation rather than presenting it as deployed.

December 16, 2026–January 14, 2027 is reserved for AZ-900 completion (target exam date remains December 20), fixing issues found during review, polishing the README and GitHub repository, updating the resume and preparing for interviews. Do not use this buffer to expand the project's scope before the first application date.

### January 15 application-readiness criteria

By January 15, the intended outcomes are:

- AZ-900 passed.
- LibraryCore deployed or accompanied by a reproducible deployment walkthrough.
- Core backend functionality, authentication and authorization implemented.
- PostgreSQL migrations and constraints working.
- Redis caching and rate limiting implemented.
- Background worker operational.
- Automated tests and CI pipeline working.
- Azure deployment, secrets management and monitoring demonstrated.
- Actual load-test results documented.
- GitHub README and architecture documentation complete.
- Able to explain design decisions, trade-offs, failure handling and performance results in interviews.
