"""Configuration pytest pour WAZASH backend — EPIC-07."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import models so Base.metadata knows about them before create_all
import app.models  # noqa: F401

from app.core.config import settings
from app.core.database import Base, get_db
from app.core.security import get_current_user, verify_agent_key
from app.core.storage import seed_default_users
from app.main import app

# Force SQLite in-memory for tests
TEST_DATABASE_URL = "sqlite:///./test_wazash.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def override_get_current_user():
    from app.models.user import User
    return User(email="test@wazash.io", role="admin", is_active=True)


def override_verify_agent_key():
    return True


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[verify_agent_key] = override_verify_agent_key


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Crée les tables avant chaque test et les supprime après."""
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    seed_default_users(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Client HTTP avec les overrides de dépendances."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session():
    """Session DB directe pour les tests qui en ont besoin."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
