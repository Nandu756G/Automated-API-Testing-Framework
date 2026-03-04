"""
test_posts.py
-------------
Test suite for the /posts endpoint.

Categories covered:
  - Functional tests  (status code, JSON structure, data fields)
  - Negative tests    (invalid endpoint, invalid post ID)
  - Edge cases        (response time, non-empty body)
"""

import logging
import pytest
from utils.api_client import get_request, post_request

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Functional Tests
# ---------------------------------------------------------------------------

class TestPostsFunctional:
    """Functional tests for GET /posts"""

    def test_get_posts_status_code_200(self):
        """Verify GET /posts returns HTTP 200 OK."""
        response = get_request("/posts")
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. Body: {response.text}"
        )

    def test_get_posts_returns_list(self):
        """Verify GET /posts response body is a non-empty JSON list."""
        response = get_request("/posts")
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        assert len(data) > 0, "Response list must not be empty"

    def test_get_posts_json_structure(self):
        """Verify each post object contains the required fields."""
        required_fields = {"userId", "id", "title", "body"}
        response = get_request("/posts")
        posts = response.json()
        for post in posts[:5]:  # spot-check first 5 records
            missing = required_fields - post.keys()
            assert not missing, (
                f"Post id={post.get('id')} is missing fields: {missing}"
            )

    def test_get_single_post_status_code_200(self):
        """Verify GET /posts/1 returns HTTP 200 OK."""
        response = get_request("/posts/1")
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

    def test_get_single_post_data_fields(self):
        """Verify GET /posts/1 returns expected field values."""
        response = get_request("/posts/1")
        post = response.json()
        assert post["id"] == 1, f"Expected id=1, got {post['id']}"
        assert post["userId"] == 1, f"Expected userId=1, got {post['userId']}"
        assert isinstance(post["title"], str) and len(post["title"]) > 0
        assert isinstance(post["body"], str) and len(post["body"]) > 0

    def test_create_post_returns_201(self):
        """Verify POST /posts returns HTTP 201 Created."""
        payload = {"title": "Automation Test", "body": "Test body", "userId": 1}
        response = post_request("/posts", payload)
        assert response.status_code == 201, (
            f"Expected 201, got {response.status_code}. Body: {response.text}"
        )

    def test_create_post_response_contains_id(self):
        """Verify POST /posts response contains a new resource ID."""
        payload = {"title": "New Post", "body": "Hello world", "userId": 2}
        response = post_request("/posts", payload)
        data = response.json()
        assert "id" in data, f"Response missing 'id' field: {data}"
        assert isinstance(data["id"], int), "id should be an integer"


# ---------------------------------------------------------------------------
# Negative Tests
# ---------------------------------------------------------------------------

class TestPostsNegative:
    """Negative tests for /posts endpoint."""

    def test_get_nonexistent_post_returns_404(self):
        """Verify GET /posts/99999 returns HTTP 404 Not Found."""
        response = get_request("/posts/99999")
        assert response.status_code == 404, (
            f"Expected 404, got {response.status_code}"
        )

    def test_invalid_sub_endpoint_returns_404(self):
        """Verify GET /posts/1/invalid_path returns 404."""
        response = get_request("/posts/1/invalid_path")
        assert response.status_code == 404, (
            f"Expected 404, got {response.status_code}"
        )


# ---------------------------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------------------------

class TestPostsEdgeCases:
    """Edge-case tests for /posts endpoint."""

    def test_response_time_under_threshold(self, response_time_threshold):
        """Verify GET /posts responds within the accepted time threshold."""
        response = get_request("/posts")
        elapsed = response.elapsed.total_seconds()
        logger.info("GET /posts elapsed: %.3fs (threshold: %.1fs)", elapsed, response_time_threshold)
        assert elapsed < response_time_threshold, (
            f"Response too slow: {elapsed:.3f}s > {response_time_threshold}s"
        )

    def test_response_body_is_not_empty(self):
        """Verify GET /posts response body is not empty."""
        response = get_request("/posts")
        assert len(response.content) > 0, "Response body must not be empty"

    def test_content_type_is_json(self):
        """Verify GET /posts returns Content-Type: application/json."""
        response = get_request("/posts")
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, (
            f"Expected JSON content type, got: {content_type}"
        )
