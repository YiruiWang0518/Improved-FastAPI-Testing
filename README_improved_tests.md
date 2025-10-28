
# Improved Test Suite for `fastapi-realworld-example-app`

This folder contains an _add-on_ pytest suite (`tests_improved/`) designed to **augment** the repository's existing tests by:
- Expanding **code coverage** across routers, error handlers, and happy/edge paths.
- Exercising the app's **use of external libraries** (FastAPI `TestClient`, Pydantic validation, SQLAlchemy uniqueness, JWT rejection paths).
- Including **malicious/abusive inputs** (XSS-like strings, invalid shapes/types, tampered JWT).
- Producing machine-readable **reports**: JUnit XML (`reports/junit.xml`) and Coverage (terminal + HTML via `coverage html`).

## How to run (local)
1. Start Postgres (the repo's `compose.yaml` spins a dev and a test DB):
   ```bash
   docker compose up -d
   ```

2. Install dependencies (follow the repo's README). Example using `uv`:
   ```bash
   uv sync && uv venv
   # optionally seed/migrate if needed
   uv run alembic upgrade head
   ```

3. Run the full test suite (repo + improved):
   ```bash
   pytest
   ```

4. Generate coverage HTML:
   ```bash
   coverage html -d reports/html
   ```

Artifacts:
- **JUnit**: `reports/junit.xml`
- **Coverage HTML**: `reports/html/index.html`

## Notes
- The tests assume the API is mounted under the `/api` prefix as documented in the upstream README.
- If your DB is not available at the default location, set `DATABASE_URL` before running `pytest`.
- `pytest.ini` is configured with `--cov-fail-under` disabled by default to avoid blocking you; set a threshold if desired.
