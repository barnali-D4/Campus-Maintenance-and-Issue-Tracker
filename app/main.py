
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import MaintenanceIssue
from app.priority import classify_priority


# Database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    if engine is not None:
        Base.metadata.create_all(bind=engine)
    yield


# Create FastAPI application
app = FastAPI(
    title="Campus Maintenance and Issue Tracker",
    description="Report and track campus maintenance issues.",
    version="1.0.0",
    lifespan=lifespan,
)


# Frontend configuration
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR / "static")),
    name="static",
)

templates = Jinja2Templates(
    directory=str(FRONTEND_DIR / "templates")
)


# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# API information
@app.get("/api")
def api_info():
    return {
        "project": "Campus Maintenance and Issue Tracker",
        "version": "1.0.0",
        "status": "running",
    }


# Priority classification request
class IssueRequest(BaseModel):
    category: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=1000)


# Classify priority without saving the issue
@app.post("/api/classify")
def classify_issue(issue: IssueRequest):
    priority = classify_priority(
        issue.category,
        issue.description,
    )

    return {
        "category": issue.category,
        "description": issue.description,
        "priority": priority,
    }


# New maintenance issue request
class IssueCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    category: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=1000)
    location: str = Field(min_length=1, max_length=150)


# Create and save an issue
@app.post("/api/issues", status_code=201)
def create_issue(
    issue: IssueCreate,
    db: Session = Depends(get_db),
):
    priority = classify_priority(
        issue.category,
        issue.description,
    )

    new_issue = MaintenanceIssue(
        title=issue.title,
        category=issue.category,
        description=issue.description,
        location=issue.location,
        priority=priority,
        status="Open",
    )

    try:
        db.add(new_issue)
        db.commit()
        db.refresh(new_issue)

        return {
            "message": "Issue created successfully",
            "id": new_issue.id,
            "title": new_issue.title,
            "priority": new_issue.priority,
            "status": new_issue.status,
        }

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save the issue",
        ) from exc


# Retrieve all maintenance issues
@app.get("/api/issues")
def get_issues(db: Session = Depends(get_db)):
    issues = (
        db.query(MaintenanceIssue)
        .order_by(MaintenanceIssue.id.desc())
        .all()
    )

    return [
        {
            "id": issue.id,
            "title": issue.title,
            "category": issue.category,
            "description": issue.description,
            "location": issue.location,
            "priority": issue.priority,
            "status": issue.status,
            "created_at": issue.created_at,
        }
        for issue in issues
    ]


from typing import Literal

@app.patch("/api/issues/{issue_id}/status")
def update_issue_status(
    issue_id: int,
    status: Literal["Open", "In Progress", "Resolved"],
    db: Session = Depends(get_db),
):
    issue = db.query(MaintenanceIssue).filter(
        MaintenanceIssue.id == issue_id
    ).first()

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    issue.status = status
    db.commit()
    db.refresh(issue)

    return {
        "message": "Issue status updated successfully",
        "id": issue.id,
        "status": issue.status,
    }
