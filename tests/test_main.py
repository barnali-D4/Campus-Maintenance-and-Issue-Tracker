
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


# Separate in-memory SQLite database for testing.
# This keeps tests isolated from the development PostgreSQL database.
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "VJIT CampusCare" in response.text


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_api_info(client):
    response = client.get("/api")

    assert response.status_code == 200

    data = response.json()
    assert data["project"] == "Campus Maintenance and Issue Tracker"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"


def test_classify_issue_api(client):
    response = client.post(
        "/api/classify",
        json={
            "category": "Electrical",
            "description": "Fire in laboratory",
        },
    )

    assert response.status_code == 200
    assert response.json()["priority"] == "Critical"


def test_create_issue_api(client):
    response = client.post(
        "/api/issues",
        json={
            "title": "Exposed electrical wire",
            "category": "Electrical",
            "description": "An exposed live wire near the laboratory",
            "location": "Science Block",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["message"] == "Issue created successfully"
    assert data["id"] == 1
    assert data["priority"] == "Critical"
    assert data["status"] == "Open"


def test_get_issues_api(client):
    client.post(
        "/api/issues",
        json={
            "title": "Broken classroom chair",
            "category": "Furniture",
            "description": "A chair is broken in the classroom",
            "location": "Room 101",
        },
    )

    response = client.get("/api/issues")

    assert response.status_code == 200

    issues = response.json()
    assert len(issues) == 1
    assert issues[0]["title"] == "Broken classroom chair"
    assert issues[0]["status"] == "Open"


def test_update_issue_status_api(client):
    create_response = client.post(
        "/api/issues",
        json={
            "title": "Classroom fan not working",
            "category": "Electrical",
            "description": "The ceiling fan is not working",
            "location": "Room 201",
        },
    )

    issue_id = create_response.json()["id"]

    response = client.patch(
        f"/api/issues/{issue_id}/status",
        params={"status": "In Progress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "In Progress"

    issues = client.get("/api/issues").json()
    assert issues[0]["status"] == "In Progress"


def test_update_missing_issue_status(client):
    response = client.patch(
        "/api/issues/9999/status",
        params={"status": "Resolved"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Issue not found"


def test_priority_classification_validation(client):
    response = client.post(
        "/api/classify",
        json={
            "category": "E",
            "description": "Bad",
        },
    )

    assert response.status_code == 422
