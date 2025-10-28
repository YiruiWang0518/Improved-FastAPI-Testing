
import os
import uuid
import pytest

from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def test_env(monkeypatch):
    """
    Ensure the application runs against a test configuration.
    If DATABASE_URL is not set by the user, assume a local Postgres is running.
    The upstream repo's compose.yaml spins a *test* database; this fixture
    allows local runs without modifying the app code.
    """
    monkeypatch.setenv("APP_ENV", os.getenv("APP_ENV", "test"))
    # SECRET_KEY is only used by the app when generating tokens;
    # set a default to keep behavior deterministic in local runs.
    monkeypatch.setenv("SECRET_KEY", os.getenv("SECRET_KEY", "test-secret-please-change"))
    if "DATABASE_URL" not in os.environ:
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "realworld_test")
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        monkeypatch.setenv("DATABASE_URL", f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")
    yield

@pytest.fixture(scope="session")
def client(test_env):
    """
    Create a synchronous TestClient against the FastAPI app.
    """
    from app.main import app  # import after env vars are in place
    with TestClient(app) as c:
        yield c

@pytest.fixture
def unique_user():
    u = uuid.uuid4().hex[:12]
    return {"email": f"{u}@example.com", "username": f"user_{u}", "password": "Password123!"}

def register_user(client, user_payload):
    return client.post("/api/users", json={"user": user_payload})

def login_user(client, email, password):
    return client.post("/api/users/login", json={"user": {"email": email, "password": password}})

def auth_headers(token: str):
    return {"Authorization": f"Token {token}"}
