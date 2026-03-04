"""
test_comments.py
----------------
Test suite for the /comments endpoint.

Categories covered:
  - Functional tests  (status code, JSON structure, field values)
  - Negative tests    (non-existent comment, invalid query param)
  - Edge cases        (response time, email format in comments)
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

class TestCommentsFunctional:
    """Functional tests for GET /comments."""

    def test_get_comments_status_code_200(self):
        """Verify GET /comments returns HTTP 200 OK."""
        response = get_request("/comments")
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. Body: {response.text}"
        )

    def test_get_comments_returns_list(self):
        """Verify GET /comments response is a non-empty JSON list."""
        response = get_request("/comments")
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        assert len(data) > 0, "Comments list must not be empty"

    def test_get_comments_required_fields(self):
        """Verify each comment object contains all expected fields."""
        required_fields = {"postId", "id", "name", "email", "body"}
        response = get_request("/comments")
        comments = response.json()
        for comment in comments[:5]:  # spot-check first 5
            missing = required_fields - comment.keys()
            assert not missing, (
                f"Comment id={comment.get('id')} missing fields: {missing}"
            )

    def test_get_single_comment_status_code_200(self):
        """Verify GET /comments/1 returns HTTP 200 OK."""
        response = get_request("/comments/1")
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

    def test_get_single_comment_data_fields(self):
        """Verify GET /comments/1 returns correct id and non-empty name/body."""
        response = get_request("/comments/1")
        comment = response.json()
        assert comment["id"] == 1, f"Expected id=1, got {comment['id']}"
        assert comment["postId"] == 1, f"Expected postId=1, got {comment['postId']}"
        assert isinstance(comment["name"], str) and len(comment["name"]) > 0
        assert isinstance(comment["body"], str) and len(comment["body"]) > 0

    def test_filter_comments_by_post_id(self):
        """Verify GET /comments?postId=1 filters correctly."""
        response = get_request("/comments", params={"postId": 1})
        assert response.status_code == 200
        comments = response.json()
        assert len(comments) > 0, "Filtered comments list should not be empty"
        for comment in comments:
            assert comment["postId"] == 1, (
                f"Expected postId=1, got {comment['postId']}"
            )


# ---------------------------------------------------------------------------
# Negative Tests
# ---------------------------------------------------------------------------

class TestCommentsNegative:
    """Negative tests for /comments endpoint."""

    def test_get_nonexistent_comment_returns_404(self):
        """Verify GET /comments/99999 returns HTTP 404 Not Found."""
        response = get_request("/comments/99999")
        assert response.status_code == 404, (
            f"Expected 404, got {response.status_code}"
        )

    def test_filter_with_invalid_post_id_returns_empty(self):
        """
        Verify GET /comments?postId=99999 returns 200 with an empty list
        (the API returns 200 + [] for unknown postId values).
        """
        response = get_request("/comments", params={"postId": 99999})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0, (
            f"Expected empty list for non-existent postId, got {len(data)} items"
        )


# ---------------------------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------------------------

class TestCommentsEdgeCases:
    """Edge-case tests for /comments endpoint."""

    def test_response_time_under_threshold(self, response_time_threshold):
        """Verify GET /comments responds within the accepted time threshold."""
        response = get_request("/comments")
        elapsed = response.elapsed.total_seconds()
        logger.info(
            "GET /comments elapsed: %.3fs (threshold: %.1fs)",
            elapsed,
            response_time_threshold,
        )
        assert elapsed < response_time_threshold, (
            f"Response too slow: {elapsed:.3f}s > {response_time_threshold}s"
        )

    def test_response_body_is_not_empty(self):
        """Verify GET /comments response body is not empty."""
        response = get_request("/comments")
        assert len(response.content) > 0, "Response body must not be empty"

    def test_comment_emails_are_valid(self):
        """Verify commenter email fields match basic email pattern."""
        response = get_request("/comments")
        comments = response.json()
        for comment in comments[:10]:  # spot-check first 10
            email = comment.get("email", "")
            assert EMAIL_REGEX.match(email), (
                f"Comment id={comment['id']} has invalid email: '{email}'"
            )
