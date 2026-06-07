from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from src.main import app
import os
os.environ["DB_URL"] = "sqlite:///./test.db"

from src.db import get_db, Base, get_engine
from src.dependencies import require_auth


# engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=get_engine())

Base.metadata.create_all(bind=get_engine())

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[require_auth] = lambda: "test-user"


@pytest.fixture(autouse=True)
def reset_db():
    yield
    # Drop and recreate between tests for a clean slate
    Base.metadata.drop_all(bind=get_engine())
    Base.metadata.create_all(bind=get_engine())