# Phase 4 - PetStore API CRUD

This phase validates the PetStore pet flow independently from the E2E browser
tests.

## Files

- `api_tests/config.py`: stores the PetStore documentation root URL, `/v2` API
  prefix, and request timeout. Keeping the root URL and API prefix separate
  makes it clear that the exercise page is `https://petstore.swagger.io`, while
  the REST endpoints are served under `/v2`.
- `api_tests/test_pet_crud.py`: contains the requested pet flow: add a pet,
  search that pet by ID, update its name and status to `sold`, then search by
  status and confirm the modified pet appears in the response.
- `.github/workflows/api.yml`: runs only the API tests in GitHub Actions using
  `pytest -m api`.

## Why the test uses unique data

The test creates a pet ID and pet name with UUID-based values, such as
`qa-pet-abc123...`. This avoids collisions with pets left behind by previous
runs or by other people using the public PetStore service.

## Why retries are included

PetStore is a public demo API and can show small consistency delays after
`POST` or `PUT`. The test retries the verification steps instead of
retrying the action itself:

- after `POST /pet`, it retries `GET /pet/{petId}` until the pet is visible;
- after `PUT /pet`, it retries `GET /pet/{petId}` until the updated name and
  `sold` status are visible;
- after the update, it retries `GET /pet/findByStatus?status=sold` until the
  modified pet appears in the status search results.

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
