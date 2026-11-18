Project 1: LibraryCore: Backend Engineering & Cloud Platform
Target completion: Dec 15, 2026Purpose: Portfolio project for backend engineering and cloud engineering job applications.

1. Project Objective
Expand my existing FastAPI Personal Library API into a production-style backend system that demonstrates practical backend engineering, relational database design, distributed systems fundamentals, application security, performance optimization, reliability and cloud deployment.
The objective is not simply to implement CRUD endpoints or demonstrate familiarity with different technologies.
The focus is on understanding and solving real engineering problems involving:
* Database consistency and transaction management.
* Concurrency and race conditions.
* Authentication and authorization.
* Database performance and query optimization.
* Caching and cache invalidation.
* Background job processing.
* API reliability and fault handling.
* Containerization and CI/CD.
* Cloud infrastructure and deployment.
* Monitoring and performance measurement.
The final application should demonstrate the ability to design, implement, test, deploy, monitor and troubleshoot a backend system.
Backend
* Python
* FastAPI
* SQLAlchemy 2.0
* Pydantic
Database
* PostgreSQL
* Alembic for database migrations
Caching and Background Processing
* Redis
* RQ (Redis Queue)
Authentication and Security
* JWT authentication
* Secure password hashing
* Role-Based Access Control (RBAC)
* Refresh-token rotation and revocation
* Secure secrets management
DevOps and Infrastructure
* Docker
* Docker Compose
* GitHub Actions
* Azure Container Registry
* Azure Container Apps
Azure Services
* Azure Database for PostgreSQL
* Azure Managed Redis, subject to regional availability and budget
* Azure Key Vault
* Managed Identity
* Application Insights
* Azure Monitor
Testing and Performance
* Pytest
* Unit and integration testing
* Locust for load testing
4. Database Design
The application should initially use five core tables.
4.1 Users
Responsible for authentication, authorization and library ownership.
Suggested fields:
* id (primary key)
* email (unique)
* password_hash
* role (admin/user)
* is_active
* created_at
* updated_at
Requirements:
* Secure password hashing.
* Unique email constraint.
* Role-based authorization.
* Active/inactive account handling.
A separate Roles table is unnecessary for the initial two-role system.
4.2 Authors
Represents the shared author catalogue.
Suggested fields:
* id (primary key)
* name
* biography
* created_at
* updated_at
Requirements:
* One-to-many relationship with Books.
* Appropriate validation and constraints.
* Admin-controlled author creation, modification and deletion.
* Authenticated users can read author information.
4.3 Books
Represents books belonging to individual users.
Suggested fields:
* id (primary key)
* title
* description
* publication_year
* author_id (foreign key referencing Authors)
* owner_id (foreign key referencing Users)
* created_at
* updated_at
Requirements:
* Maintain the existing one-to-many Author–Book relationship.
* Introduce user-specific book ownership.
* Users should only access and modify their own books.
* Admins should have appropriate administrative access.
* Prevent unauthorized access to another user's resources.
The same author can have multiple books, and different users can own their own entries for the same book.
4.4 IdempotencyRecords
Responsible for preventing duplicate operations when clients retry requests.
Suggested fields:
* id (primary key)
* user_id
* idempotency_key
* request_hash
* response_status
* response_body (JSONB)
* created_at
* expires_at
Requirements:
* Unique constraint on (user_id, idempotency_key).
* Store the original request hash.
* Store the completed response.
* Return the original result for a repeated request with the same key and payload.
* Reject reuse of the same key with a different payload.
* Handle simultaneous requests using database constraints and transactions.
* Define how expired records are cleaned up.
4.5 RefreshTokens
Responsible for persistent refresh-token management.
Suggested fields:
* id (primary key)
* user_id
* token_hash
* token_family_id
* expires_at
* revoked_at
* created_at
Requirements:
* Store hashed refresh tokens rather than plaintext tokens.
* Implement refresh-token rotation.
* Revoke previously used tokens after rotation.
* Handle expired and revoked tokens.
* Detect refresh-token reuse where applicable.
* Support logout and token revocation.
Database Design Principles
* Use proper foreign keys and constraints.
* Define NOT NULL and unique constraints where appropriate.
* Add indexes based on actual query patterns.
* Use Alembic for all schema changes.
* Understand transaction boundaries and rollback.
* Use PostgreSQL as the primary development database early in the project.
* Migrate existing SQLite data appropriately or recreate development data when safe.
* Avoid unnecessary tables and abstractions.
Optional future tables:
* AuditLogs for persistent administrative activity tracking.
* ExportRecords if persistent export history becomes necessary.
These are not required for the initial implementation.
5. Functional and Engineering Requirements
A. Core Backend and Database Engineering
* Complete CRUD operations for Books and Authors.
* Implement proper Author–Book relationships.
* Introduce PostgreSQL.
* Use SQLAlchemy 2.0 ORM patterns.
* Implement Alembic migrations.
* Define appropriate foreign keys, unique constraints and NOT NULL constraints.
* Implement indexes based on query patterns.
* Understand and implement transaction boundaries.
* Handle transaction rollback and database failures.
* Implement pagination, filtering and sorting.
* Investigate N+1 queries.
* Optimize database access using appropriate ORM loading strategies.
* Use EXPLAIN ANALYZE to inspect query execution plans.
B. Authentication and Authorization
* Implement user registration and login.
* Securely hash passwords.
* Implement JWT access and refresh tokens.
* Implement token expiration and refresh handling.
* Implement refresh-token rotation and revocation.
* Introduce Admin and Regular User roles.
* Implement role-based endpoint authorization.
* Enforce resource ownership.
* Prevent unauthorized access to other users' books.
* Protect sensitive endpoints and configuration.
C. API Reliability and Data Consistency
* Implement consistent API error responses.
* Use appropriate HTTP status codes.
* Implement request validation using Pydantic.
* Implement idempotency for selected write operations.
* Prevent duplicate resource creation during concurrent requests.
* Handle simultaneous updates and database conflicts.
* Understand transaction isolation and locking.
* Introduce request IDs and structured application logging.
* Implement consistent error handling for database and external service failures.
D. Redis and Distributed Processing
Caching
* Implement Redis caching for frequently accessed resources.
* Introduce cache expiration using TTL.
* Implement cache invalidation after create, update and delete operations.
* Understand cache-aside patterns.
* Handle Redis unavailability gracefully.
* Test stale-cache scenarios and concurrent access.
Rate Limiting
* Implement Redis-backed rate limiting.
* Apply limits based on authenticated users or client IPs.
* Ensure rate-limit updates are atomic under concurrent requests.
* Define behaviour when Redis becomes unavailable.
Background Jobs
* Implement asynchronous background processing using RQ.
* Run workers independently of FastAPI.
* Implement a practical background task such as CSV library export or report generation.
* Handle job failures and retries.
* Track job status using RQ and Redis.
* Understand what happens when a worker crashes or restarts.
E. Testing and Quality Assurance
Use Pytest for automated testing.
Implement:
* Unit tests for services and business logic.
* Integration tests against PostgreSQL and Redis.
* Authentication and authorization tests.
* Database constraint tests.
* Transaction rollback tests.
* Concurrent request tests.
* Idempotency tests under simultaneous requests.
* Cache invalidation tests.
* Rate-limiting tests.
* Background job execution and failure tests.
* API validation and error-response tests.
Testing should be introduced alongside each feature, not postponed until the end.
F. Docker and CI/CD
Docker
* Create production-oriented Dockerfiles.
* Use Docker Compose for local development.
* Containerize FastAPI and the background worker independently.
* Configure PostgreSQL and Redis containers.
* Use environment-based configuration.
* Implement appropriate health checks.
GitHub Actions
Implement CI/CD workflows that:
* Run linting and formatting checks.
* Execute automated tests.
* Validate database migrations.
* Build Docker images.
* Publish images to Azure Container Registry.
* Deploy the application to Azure.
Use secure GitHub-to-Azure authentication, preferably OpenID Connect, rather than storing long-lived cloud credentials in repository secrets.
6. Azure Cloud Deployment
Deploy the application using Microsoft Azure.
A. Infrastructure
* Create a personal Azure account and subscription.
* Understand Azure Portal and Azure CLI.
* Create and organize Azure resource groups.
* Understand regions, resource provisioning and pricing.
* Deploy FastAPI using Azure Container Apps.
* Store Docker images in Azure Container Registry.
* Use Azure Database for PostgreSQL.
* Configure Azure Managed Redis, subject to availability and budget.
* Deploy the background worker as a separate containerized service.
B. Security
* Store application secrets in Azure Key Vault.
* Configure Managed Identity for supported Azure service-to-service authentication.
* Avoid hardcoded credentials and secrets.
* Configure database authentication securely.
* Understand Azure RBAC and access control.
* Restrict unnecessary public access to infrastructure.
C. Monitoring and Reliability
* Integrate Application Insights.
* Implement structured logging.
* Implement request correlation IDs.
* Implement health and readiness endpoints.
* Monitor API failures and latency.
* Monitor database and container resource usage.
* Understand how to troubleshoot deployment and connectivity failures.
* Investigate application exceptions using telemetry.
D. Deployment Pipeline
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
7. Performance and Load Testing
Use Locust to evaluate API performance.
Measure:
* Requests per second (throughput).
* p50 latency.
* p95 latency.
* p99 latency.
* Error rate.
* Database query performance.
* Cached versus uncached response performance.
Conduct baseline and optimized performance tests.
Test scenarios should include:
* Reading books with pagination.
* Filtering books.
* Authenticated write operations.
* Concurrent requests.
* Redis caching enabled and disabled.
* Increasing concurrent user loads.
Document:
* Test environment and resource configuration.
* Dataset size.
* Number of concurrent users.
* Test duration.
* Bottlenecks identified.
* Optimizations implemented.
* Before-and-after performance results.
Never report unmeasured performance improvements.
8. Engineering Challenges to Demonstrate
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
9. Final Deployment Architecture
The final logical architecture should consist of:
* FastAPI API service deployed on Azure Container Apps.
* Independent background worker deployed as a separate containerized service.
* Azure Database for PostgreSQL for persistent storage.
* Azure Managed Redis for caching, rate limiting and job queues.
* Azure Key Vault for secrets.
* Azure Container Registry for Docker images.
* GitHub Actions for CI/CD.
* Application Insights for monitoring and diagnostics.
The architecture should support independent API and worker scaling.
10. Documentation Requirements
The GitHub repository must include:
* Project overview and technical objectives.
* Architecture diagram.
* Database schema and entity relationship diagram.
* API documentation.
* Local setup instructions.
* Environment configuration documentation.
* Database migration instructions.
* Testing instructions.
* Docker and deployment instructions.
* CI/CD workflow explanation.
* Azure infrastructure overview.
* Load-testing methodology and results.
* Engineering decisions and trade-offs.
* Known limitations and future improvements.
Include a dedicated section explaining important engineering decisions, such as:
* Why PostgreSQL was selected.
* Why Redis caching was introduced.
* How cache invalidation works.
* How idempotency is enforced.
* How transactions protect data consistency.
* How the application handles external service failures.
* How database queries were optimized.
* How deployment and monitoring work.
11. Definition of Done
The project is considered complete when:
* Core API functionality is implemented.
* Authentication and authorization work correctly.
* User-specific book ownership is enforced.
* PostgreSQL migrations and constraints are implemented.
* Transactions and idempotency work correctly.
* Redis caching and rate limiting work correctly.
* Background jobs execute independently.
* Unit and integration tests pass.
* Concurrency scenarios have been tested.
* Dockerized services run locally.
* GitHub Actions CI/CD pipeline works.
* The application is deployed on Azure.
* Key Vault and supported Managed Identity integrations are configured.
* Application Insights receives application telemetry.
* Load testing has been completed with documented results.
* Repository documentation is sufficient for another developer to run and understand the system.
12. Implementation Guidelines for Codex
Act as a Senior Backend Engineering Mentor.
I want to implement this project myself and understand the engineering decisions behind it.
Do not write the implementation code for me unless I explicitly request it.
For each task:
1. Inspect the existing repository before suggesting modifications.
2. Explain the engineering problem being solved.
3. Explain the relevant concepts and trade-offs.
4. Identify the files and components I should work on.
5. Break the task into manageable implementation steps.
6. Define acceptance criteria.
7. Suggest appropriate tests.
8. Wait for me to implement the changes.
9. Review my implementation and identify design flaws, security problems, performance issues and incorrect assumptions.
Additional rules:
* Never restart or rewrite the existing project without justification.
* Do not dump complete code implementations.
* Do not introduce unnecessary technologies or abstractions.
* Do not skip important engineering concepts.
* Do not move to the next task before reviewing the current task.
* Challenge incorrect technical decisions.
* Prioritize correctness and understanding over implementation speed.
Give me exactly ONE next task at a time.
Certification
* Pass Microsoft Azure Fundamentals (AZ-900).
* Obtain the certification and add it to my resume and LinkedIn.
Portfolio
* Complete and deploy the Personal Library API.
* Have a publicly accessible API or documented deployment.
* Maintain a clean GitHub repository.
* Include architecture documentation and actual performance benchmarks.
* Be able to explain the implementation and engineering trade-offs in technical interviews.
The project should prioritize backend engineering depth and practical Azure experience.
Avoid adding frontend development, AI features, microservices or unnecessary infrastructure to this project.
The final objective is to demonstrate genuine backend engineering ability, not merely familiarity with a large technology stack.