"""
conftest.py
-----------
Shared pytest fixtures and session-level logging setup.
Fixtures defined here are automatically available to all test files.
"""

import logging
import pytest

# ---------------------------------------------------------------------------
# Session-level logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger("conftest")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def response_time_threshold() -> float:
    """Maximum acceptable response time in seconds for any API call."""
    return 3.0


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Return the base URL for the API under test."""
    return "https://jsonplaceholder.typicode.com"
