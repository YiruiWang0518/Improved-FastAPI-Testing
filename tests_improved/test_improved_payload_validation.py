
import pytest

def test_comment_payload_wrong_type_returns_422(client, unique_user):
    # login
    r = client.post("/api/users", json={"user": unique_user})
    assert r.status_code in (200, 201)
    token = r.json()["user"]["token"]

    # create article
    payload = {"article": {"title": "T", "description": "D", "body": "B", "tagList": []}}
    ra = client.post("/api/articles", json=payload, headers={"Authorization": f"Token {token}"})
    slug = ra.json()["article"]["slug"]

    # send invalid payload type for comment (comment should be an object, not string)
    bad = {"comment": "not-an-object"}
    rc = client.post(f"/api/articles/{slug}/comments", json=bad, headers={"Authorization": f"Token {token}"})
    assert rc.status_code == 422

def test_article_payload_with_malicious_strings_is_accepted_or_rejected_safely(client, unique_user):
    # This test ensures that even if we provide XSS-like strings, the server responds deterministically
    # (200/201 if stored as-is, or 422 if rejected by validators) but never 500.
    r = client.post("/api/users", json={"user": unique_user})
    assert r.status_code in (200, 201)
    token = r.json()["user"]["token"]

    bad_body = "<script>alert('xss')</script>" * 10
    payload = {"article": {"title": "xss", "description": "x", "body": bad_body, "tagList": ["<img onerror=x />"]}}
    res = client.post("/api/articles", json=payload, headers={"Authorization": f"Token {token}"})
    assert res.status_code in (200, 201, 422)  # but never 500
