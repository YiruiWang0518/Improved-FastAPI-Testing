
import pytest

def test_tampered_token_is_rejected_with_401(client, unique_user):
    # Register new user to obtain a valid token
    r = client.post("/api/users", json={"user": unique_user})
    assert r.status_code in (200, 201)
    token = r.json()["user"]["token"]

    # Tamper with token by flipping the last character
    flipped = token[:-1] + ("A" if token[-1] != "A" else "B")
    res = client.get("/api/user", headers={"Authorization": f"Token {flipped}"})
    assert res.status_code in (401, 403)

def test_missing_bearer_token_cannot_create_article(client, unique_user):
    # Unauthenticated create should fail
    payload = {"article": {"title": "T", "description": "D", "body": "B", "tagList": ["x"]}}
    res = client.post("/api/articles", json=payload)
    assert res.status_code in (401, 403)
