
from typing import Dict
import pytest

def test_register_invalid_email_returns_422(client):
    bad = {"user": {"email": "not-an-email", "username": "someone", "password": "Password123!"}}
    res = client.post("/api/users", json=bad)
    assert res.status_code == 422
    body = res.json()
    assert "detail" in body  # FastAPI/Pydantic validation error structure

def test_register_missing_envelope_returns_422(client):
    # RealWorld API wraps payloads in {"user": {...}}
    res = client.post("/api/users", json={"email": "x@y.com", "username": "x", "password": "Password123!"})
    assert res.status_code == 422

def test_get_current_user_requires_auth(client):
    res = client.get("/api/user")
    assert res.status_code in (401, 403)

def test_register_login_and_access_user_endpoint(client, unique_user):
    # Register
    r1 = client.post("/api/users", json={"user": unique_user})
    assert r1.status_code in (200, 201)
    token = r1.json()["user"]["token"]

    # Login explicitly and ensure the same user can authenticate
    r2 = client.post("/api/users/login", json={"user": {"email": unique_user["email"], "password": unique_user["password"]}})
    assert r2.status_code == 200
    token2 = r2.json()["user"]["token"]
    assert isinstance(token2, str) and len(token2) > 10

    # Access /api/user with auth
    r3 = client.get("/api/user", headers={"Authorization": f"Token {token2}"})
    assert r3.status_code == 200
    assert r3.json()["user"]["email"] == unique_user["email"]
