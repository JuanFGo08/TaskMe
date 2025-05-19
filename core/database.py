from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config_loader import settings


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
# This is the base class for all models in the application.
class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependency that provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
