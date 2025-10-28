
def test_openapi_schema_exposes_realworld_paths(client):
    r = client.get("/api/openapi.json")
    # Some forks expose OpenAPI at /api/openapi.json, others at /openapi.json with a global /api prefix.
    # Try fallback if needed.
    if r.status_code != 200:
        r = client.get("/openapi.json")
    assert r.status_code == 200
    schema = r.json()
    # Spot-check key RealWorld endpoints exist:
    paths = schema.get("paths", {})
    candidates = ["/api/users", "/api/users/login", "/api/articles", "/api/tags"]
    # normalize: some schemas may not duplicate the /api prefix inside the schema if set globally
    normalized = set(paths.keys())
    hits = 0
    for p in candidates:
        if p in normalized or p.replace("/api", "") in normalized:
            hits += 1
    assert hits >= 3  # at least 3 of 4 endpoints are described
