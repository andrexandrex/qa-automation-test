"""Pruebas CRUD de usuario contra PetStore."""

import time
from uuid import uuid4

import pytest
import requests

from api_tests.config import BASE_URL, DEFAULT_TIMEOUT


RETRY_ATTEMPTS = 5
RETRY_DELAY_SECONDS = 1


def _unique_user():
    suffix = uuid4().hex[:12]
    username = f"qa_user_{suffix}"
    return {
        "id": int(uuid4().int % 1_000_000_000),
        "username": username,
        "firstName": "QA",
        "lastName": "Automation",
        "email": f"{username}@example.com",
        "password": "qa-password-123",
        "phone": "555-0101",
        "userStatus": 1,
    }


def _request(method, path, **kwargs):
    return requests.request(
        method,
        f"{BASE_URL}{path}",
        timeout=DEFAULT_TIMEOUT,
        **kwargs,
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


def _get_user(username):
    return _request("GET", f"/user/{username}")


@pytest.mark.api
def test_petstore_user_crud():
    user = _unique_user()
    username = user["username"]
    updated_user = {
        **user,
        "firstName": "QA Updated",
        "lastName": "CRUD",
        "phone": "555-0202",
    }

    try:
        create_response = _request("POST", "/user", json=user)
        assert create_response.status_code == 200

        def assert_user_created():
            response = _get_user(username)
            assert response.status_code == 200
            body = response.json()
            assert body["username"] == username
            assert body["firstName"] == user["firstName"]
            assert body["email"] == user["email"]
            return body

        created_user = _retry_until(assert_user_created)
        assert created_user["id"] == user["id"]

        update_response = _request("PUT", f"/user/{username}", json=updated_user)
        assert update_response.status_code == 200

        def assert_user_updated():
            response = _get_user(username)
            assert response.status_code == 200
            body = response.json()
            assert body["firstName"] == updated_user["firstName"]
            assert body["lastName"] == updated_user["lastName"]
            assert body["phone"] == updated_user["phone"]
            return body

        _retry_until(assert_user_updated)

        delete_response = _request("DELETE", f"/user/{username}")
        assert delete_response.status_code == 200

        def assert_user_deleted():
            response = _get_user(username)
            assert response.status_code == 404
            return response

        _retry_until(assert_user_deleted)
    finally:
        _request("DELETE", f"/user/{username}")
