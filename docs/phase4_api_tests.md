# Phase 4 - PetStore API CRUD

This phase validates the PetStore user CRUD flow independently from the E2E
browser tests.

## Files

- `api_tests/config.py`: stores the PetStore base URL and request timeout. API
  tests import these values so URLs and timeouts are not duplicated across test
  files.
- `api_tests/test_user_crud.py`: contains one complete user lifecycle test:
  create, read, update, read again, delete, and confirm the user no longer
  exists.
- `.github/workflows/api.yml`: runs only the API tests in GitHub Actions using
  `pytest -m api`.

## Why the test uses unique data

The test creates a username with a UUID suffix, such as
`qa_user_abc123...`. This avoids collisions with users left behind by previous
runs or by other people using the public PetStore service.

## Why retries are included

PetStore is a public demo API and can show small consistency delays after
`POST`, `PUT`, or `DELETE`. The test retries the verification steps instead of
retrying the action itself:

- after `POST`, it retries `GET` until the created user is visible;
- after `PUT`, it retries `GET` until updated fields are visible;
- after `DELETE`, it retries `GET` until PetStore returns `404`.

This keeps the CRUD actions single and explicit while making assertions more
tolerant of eventual consistency.

## Checkpoint

Run:

```bash
source venv/bin/activate
pytest -m api
```

Expected result:

```text
1 passed
```
