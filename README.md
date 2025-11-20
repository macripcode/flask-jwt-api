Product Catalog API

Description:
API for managing a product catalog built with Flask, JWT authentication, and Docker.
Provides secure user authentication and CRUD operations for products.

---- Tech Stack ----

Backend: 

Flask – Python micro-framework powering the REST API.
Flask-JWT-Extended (JWT) – Token-based authentication and authorization.
SQLAlchemy / Flask-SQLAlchemy – ORM for managing database models and queries.
SQLite (testing) / MySQL (production) – Database engines used across environments.

Testing: 

Pytest – Lightweight testing framework for endpoint and logic validation.
Pytest-cov – Code coverage reporting (optional).

DevOps & Infrastructure: 

Docker – Containerization for consistent application packaging and execution.
Docker Compose – Local and EC2 orchestration of the service and dependencies.
AWS EC2 – Virtual machine hosting the application in production.
AWS RDS (MySQL) – Managed relational database service for production.

GitHub Actions – CI/CD pipeline:

Runs automated tests on each push to the main branch.
Deploys to EC2 only if all tests pass.

Architecture: 

Flask Blueprints – Modular structure for organizing routes and endpoints.
JWT Authentication – Stateless session handling with access tokens.
App Factory Pattern – Flexible application creation depending on environment.