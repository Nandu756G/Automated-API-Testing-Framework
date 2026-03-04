"""
test_users.py
-------------
Test suite for the /users endpoint.

Categories covered:
  - Functional tests  (status code, JSON structure, field values)
  - Negative tests    (non-existent user, unknown endpoint)
  - Edge cases        (response time, email format)
"""

import logging
import re
import pytest
from utils.api_client import get_request

logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# ---------------------------------------------------------------------------
# Functional Tests
# ---------------------------------------------------------------------------

class TestUsersFunctional:
    """Functional tests for GET /users."""

    def test_get_users_status_code_200(self):
        """Verify GET /users returns HTTP 200 OK."""
        response = get_request("/users")
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. Body: {response.text}"
        )

    def test_get_users_returns_list(self):
        """Verify GET /users response is a non-empty JSON list."""
        response = get_request("/users")
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        assert len(data) > 0, "User list must not be empty"

    def test_get_users_json_structure(self):
        """Verify each user object contains the required top-level fields."""
        required_fields = {"id", "name", "username", "email", "address", "phone", "website", "company"}
        response = get_request("/users")
        users = response.json()
        for user in users:
            missing = required_fields - user.keys()
            assert not missing, (
                f"User id={user.get('id')} missing fields: {missing}"
            )

    def test_get_single_user_status_code_200(self):
        """Verify GET /users/1 returns HTTP 200 OK."""
        response = get_request("/users/1")
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

    def test_get_single_user_data_fields(self):
        """Verify GET /users/1 name and username are non-empty strings."""
        response = get_request("/users/1")
        user = response.json()
        assert isinstance(user["name"], str) and len(user["name"]) > 0
        assert isinstance(user["username"], str) and len(user["username"]) > 0
        assert user["id"] == 1, f"Expected id=1, got {user['id']}"

    def test_get_users_address_structure(self):
        """Verify the address sub-object contains required keys."""
        required_address_fields = {"street", "suite", "city", "zipcode", "geo"}
        response = get_request("/users")
        users = response.json()
        for user in users[:3]:
            address = user.get("address", {})
            missing = required_address_fields - address.keys()
            assert not missing, (
                f"User id={user['id']} address missing: {missing}"
            )


# ---------------------------------------------------------------------------
# Negative Tests
# ---------------------------------------------------------------------------

class TestUsersNegative:
    """Negative tests for /users endpoint."""

    def test_get_nonexistent_user_returns_404(self):
        """Verify GET /users/99999 returns HTTP 404 Not Found."""
        response = get_request("/users/99999")
        assert response.status_code == 404, (
            f"Expected 404, got {response.status_code}"
        )

    def test_invalid_nested_user_path_returns_404(self):
        """Verify GET /users/1/unknownpath returns 404."""
        response = get_request("/users/1/unknownpath")
        assert response.status_code == 404, (
            f"Expected 404, got {response.status_code}"
        )


# ---------------------------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------------------------

class TestUsersEdgeCases:
    """Edge-case tests for /users endpoint."""

    def test_response_time_under_threshold(self, response_time_threshold):
        """Verify GET /users responds within the accepted time threshold."""
        response = get_request("/users")
        elapsed = response.elapsed.total_seconds()
        logger.info("GET /users elapsed: %.3fs (threshold: %.1fs)", elapsed, response_time_threshold)
        assert elapsed < response_time_threshold, (
            f"Response too slow: {elapsed:.3f}s > {response_time_threshold}s"
        )

    def test_user_email_format_is_valid(self):
        """Verify all user emails match basic email pattern."""
        response = get_request("/users")
        users = response.json()
        for user in users:
            email = user.get("email", "")
            assert EMAIL_REGEX.match(email), (
                f"User id={user['id']} has invalid email: '{email}'"
            )

    def test_response_body_is_not_empty(self):
        """Verify GET /users response body is not empty."""
        response = get_request("/users")
        assert len(response.content) > 0, "Response body must not be empty"
