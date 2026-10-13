
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class MaintenanceIssue(Base):
    __tablename__ = "maintenance_issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(150), nullable=False)
    priority = Column(String(20), nullable=False, default="Low")
    status = Column(String(20), nullable=False, default="Open")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
