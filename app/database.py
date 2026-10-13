
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Allow the app to be imported in environments where the database
# is configured separately, such as automated tests.
engine = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = (
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    if engine is not None
    else None
)

Base = declarative_base()


def get_db():
    if SessionLocal is None:
        raise RuntimeError(
            "DATABASE_URL is not configured. "
            "Set it in your local .env file or environment."
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
