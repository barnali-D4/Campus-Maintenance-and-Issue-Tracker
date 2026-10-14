
# Campus Maintenance & Issue Tracker

A web-based campus maintenance platform for reporting issues, automatically classifying their priority, and tracking resolution status. The project demonstrates full-stack development alongside containerization and continuous integration practices.

## Preview

<img width="1917" height="928" alt="Campus-Tracker-preview" src="https://github.com/user-attachments/assets/820a2025-420d-4554-a5cd-cf3851f21117" />

## Key Features

- **Issue Reporting:** Submit maintenance issues with a title, category, description, and location.
- **Automated Priority Classification:** Assigns Critical, High, Medium, or Low priority using rule-based classification.
- **Issue Tracking:** View reported issues and monitor their status.
- **Status Management:** Update issues through Open, In Progress, and Resolved.
- **Database Integration:** Stores issue records in PostgreSQL.
- **REST API:** Provides endpoints for issue creation, retrieval, priority classification, and status updates.
- **Automated Testing:** Uses Pytest to validate application functionality.
- **Continuous Integration:** GitHub Actions runs automated tests on pushes and pull requests to the main branch.
- **Containerization:** Docker and Docker Compose simplify application and database setup.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Testing | Pytest |
| API Testing | HTTPX |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Version Control | Git, GitHub |

## Architecture

The application follows a simple three-layer architecture:

1. **Frontend:** Provides the interface for submitting and tracking maintenance issues.
2. **Backend:** FastAPI handles API requests, validates input, classifies issue priorities, and manages status updates.
3. **Database:** PostgreSQL stores maintenance issue records, accessed through SQLAlchemy.

Docker Compose coordinates the application and database containers, while GitHub Actions automates test execution during code changes.

## Getting Started

### Prerequisites

- Python 3.12 or compatible version
- Docker Desktop with Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/barnali-D4/Campus-Maintenance-and-Issue-Tracker.git
cd Campus-Maintenance-and-Issue-Tracker
```

### 2. Configure Environment Variables

Create a `.env` file in the project root and configure the PostgreSQL password used by `docker-compose.yml`.

```dotenv
POSTGRES_PASSWORD=your_local_password
```

Use a strong local password. Do not commit `.env` or expose database credentials.

### 3. Start the Application

```bash
docker compose up -d --build
```

### 4. Open the Application

- **Web Application:** http://localhost:8000
- **Health Check:** http://localhost:8000/health
- **API Information:** http://localhost:8000/api
- **Interactive API Documentation:** http://localhost:8000/docs

### 5. Run Automated Tests

Activate your Python virtual environment, install the project dependencies, and run:

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

### 6. Stop the Containers

```bash
docker compose down
```

This stops and removes the containers while preserving the named PostgreSQL data volume.

## Continuous Integration

The GitHub Actions workflow runs the automated test suite when changes are pushed to `main` or a pull request targets `main`.

This helps detect regressions before changes are merged.

## Project Status

**Current Scope:** Functional issue reporting and tracking application with priority classification, PostgreSQL integration, Docker-based setup, automated tests, and GitHub Actions CI.

**Live Demo:** Coming soon

### Future Enhancements

- Role-based authentication for reporters, maintenance staff, and administrators.
- Selenium-based end-to-end browser testing.
- Jenkins-based deployment pipeline.
- Kubernetes deployment and orchestration.
- Automated container security scanning and application monitoring.

These enhancements are planned and are not represented as completed features.

## Contributors

1. Barnali Bhowmik
2. Vanatadapala Manaswini

## Academic Context

Developed as a DevOps Lab Project.

---

*This project explores the integration of web application development, database management, automated testing, containerization, and continuous integration in a campus maintenance use case.*
