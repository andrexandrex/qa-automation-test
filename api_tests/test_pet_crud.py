"""Pruebas CRUD de mascota contra PetStore."""

import time
from uuid import uuid4

import pytest
import requests

from api_tests.config import API_BASE_URL, DEFAULT_TIMEOUT


RETRY_ATTEMPTS = 5
RETRY_DELAY_SECONDS = 1
SOLD_STATUS = "sold"
REQUEST_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/148.0 Safari/537.36"
    ),
}


def _unique_pet():
    suffix = uuid4().hex[:10]
    pet_id = int(uuid4().int % 1_000_000_000)
    return {
        "id": pet_id,
        "category": {
            "id": 1,
            "name": "qa-category",
        },
        "name": f"qa-pet-{suffix}",
        "photoUrls": [
            "https://example.com/qa-pet.png",
        ],
        "tags": [
            {
                "id": 1,
                "name": "qa-automation",
            }
        ],
        "status": "available",
    }


def _request(method, path, **kwargs):
    headers = {**REQUEST_HEADERS, **kwargs.pop("headers", {})}
    return requests.request(
        method,
        f"{API_BASE_URL}{path}",
        headers=headers,
        timeout=DEFAULT_TIMEOUT,
        **kwargs,
    )


def _assert_status(response, expected_status):
    assert response.status_code == expected_status, (
        f"Expected HTTP {expected_status}, got {response.status_code}. "
        f"URL: {response.url}. Response: {response.text[:500]}"
    )


def _retry_until(assertion):
    last_error = None
    for _ in range(RETRY_ATTEMPTS):
        try:
            return assertion()
        except AssertionError as exc:
            last_error = exc
            time.sleep(RETRY_DELAY_SECONDS)
    raise last_error


def _get_pet(pet_id):
    return _request("GET", f"/pet/{pet_id}")


@pytest.mark.api
def test_petstore_pet_crud_by_id_and_status():
    pet = _unique_pet()
    pet_id = pet["id"]
    updated_pet = {
        **pet,
        "name": f"{pet['name']}-updated",
        "status": SOLD_STATUS,
    }

    try:
        create_response = _request("POST", "/pet", json=pet)
        _assert_status(create_response, 200)
        assert create_response.json()["id"] == pet_id

        def assert_pet_created():
            response = _get_pet(pet_id)
            _assert_status(response, 200)
            body = response.json()
            assert body["id"] == pet_id
            assert body["name"] == pet["name"]
            assert body["status"] == pet["status"]
            return body

        _retry_until(assert_pet_created)

        update_response = _request("PUT", "/pet", json=updated_pet)
        _assert_status(update_response, 200)
        assert update_response.json()["name"] == updated_pet["name"]
        assert update_response.json()["status"] == SOLD_STATUS

        def assert_pet_updated_by_id():
            response = _get_pet(pet_id)
            _assert_status(response, 200)
            body = response.json()
            assert body["id"] == pet_id
            assert body["name"] == updated_pet["name"]
            assert body["status"] == SOLD_STATUS
            return body

        _retry_until(assert_pet_updated_by_id)

        def assert_pet_found_by_status():
            response = _request("GET", "/pet/findByStatus", params={"status": SOLD_STATUS})
            _assert_status(response, 200)
            matching_pets = [
                item
                for item in response.json()
                if item.get("id") == pet_id
                and item.get("name") == updated_pet["name"]
                and item.get("status") == SOLD_STATUS
            ]
            assert matching_pets
            return matching_pets[0]

        _retry_until(assert_pet_found_by_status)
    finally:
        _request("DELETE", f"/pet/{pet_id}")
