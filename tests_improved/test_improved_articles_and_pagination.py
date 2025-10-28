
import uuid
import pytest

def _login_and_get_token(client, u):
    r = client.post("/api/users", json={"user": u})
    assert r.status_code in (200, 201)
    return r.json()["user"]["token"]

def test_create_article_happy_path_and_fetch_by_slug(client, unique_user):
    token = _login_and_get_token(client, unique_user)
    payload = {"article": {"title": "Hello World", "description": "Short", "body": "Body here", "tagList": ["intro"]}}
    r = client.post("/api/articles", json=payload, headers={"Authorization": f"Token {token}"})
    assert r.status_code in (200, 201)
    art = r.json()["article"]
    assert art["title"] == "Hello World"
    slug = art["slug"]

    # fetch by slug
    r2 = client.get(f"/api/articles/{slug}")
    assert r2.status_code == 200
    assert r2.json()["article"]["slug"] == slug

def test_create_article_missing_title_returns_422(client, unique_user):
    token = _login_and_get_token(client, unique_user)
    payload = {"article": {"description": "a", "body": "b", "tagList": []}}  # missing title
    r = client.post("/api/articles", json=payload, headers={"Authorization": f"Token {token}"})
    assert r.status_code == 422

def test_articles_pagination_bounds(client):
    # negative offset should be rejected by FastAPI validation (conint ge=0)
    r = client.get("/api/articles", params={"offset": -1})
    assert r.status_code == 422
    # absurdly large limit should also be rejected or constrained; at minimum it must not 500
    r2 = client.get("/api/articles", params={"limit": 10_000_000})
    assert r2.status_code in (200, 422)

def test_get_nonexistent_article_returns_404(client):
    slug = "does-not-exist-" + uuid.uuid4().hex[:8]
    r = client.get(f"/api/articles/{slug}")
    assert r.status_code == 404
