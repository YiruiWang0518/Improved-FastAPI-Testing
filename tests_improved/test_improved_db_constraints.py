
import pytest

def test_duplicate_email_registration_is_rejected(client, unique_user):
    # first registration
    r1 = client.post("/api/users", json={"user": unique_user})
    assert r1.status_code in (200, 201)

    # second registration with the same email
    r2 = client.post("/api/users", json={"user": {"email": unique_user["email"], "username": unique_user["username"] + "_2", "password": unique_user["password"]}})
    # RealWorld implementations commonly return 400/422/409 for duplicate keys; assert not success
    assert r2.status_code in (400, 409, 422)

def test_duplicate_username_registration_is_rejected(client, unique_user):
    # initial
    r1 = client.post("/api/users", json={"user": unique_user})
    assert r1.status_code in (200, 201)
    # duplicate username different email
    r2 = client.post("/api/users", json={"user": {"email": "dup_" + unique_user["email"], "username": unique_user["username"], "password": unique_user["password"]}})
    assert r2.status_code in (400, 409, 422)
