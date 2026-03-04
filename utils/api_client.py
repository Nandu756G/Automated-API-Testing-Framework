"""
api_client.py
-------------
Centralized API client module for the test framework.
Provides reusable get_request and post_request helpers with
base URL handling, default headers, and built-in logging.
"""

import logging
import requests

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("api_client")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_URL = "https://jsonplaceholder.typicode.com"

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Default timeout (seconds) for all requests
REQUEST_TIMEOUT = 10


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def get_request(endpoint: str, params: dict | None = None) -> requests.Response:
    """
    Perform an HTTP GET request.

    Args:
        endpoint: API path, e.g. ``"/posts"`` or ``"/posts/1"``.
        params:   Optional query-string parameters dict.

    Returns:
        :class:`requests.Response` object.

    Raises:
        requests.exceptions.RequestException: on network / timeout errors.
    """
    url = f"{BASE_URL}{endpoint}"
    logger.info("GET %s  params=%s", url, params)

    response = requests.get(
        url, headers=DEFAULT_HEADERS, params=params, timeout=REQUEST_TIMEOUT
    )

    logger.info(
        "Response: status=%s  elapsed=%.3fs  size=%d bytes",
        response.status_code,
        response.elapsed.total_seconds(),
        len(response.content),
    )
    if not response.ok:
        logger.warning("Response body: %s", response.text)

    return response


def post_request(endpoint: str, payload: dict) -> requests.Response:
    """
    Perform an HTTP POST request with a JSON body.

    Args:
        endpoint: API path, e.g. ``"/posts"``.
        payload:  Dictionary that will be serialised as JSON.

    Returns:
        :class:`requests.Response` object.

    Raises:
        requests.exceptions.RequestException: on network / timeout errors.
    """
    url = f"{BASE_URL}{endpoint}"
    logger.info("POST %s  payload=%s", url, payload)

    response = requests.post(
        url, headers=DEFAULT_HEADERS, json=payload, timeout=REQUEST_TIMEOUT
    )

    logger.info(
        "Response: status=%s  elapsed=%.3fs  size=%d bytes",
        response.status_code,
        response.elapsed.total_seconds(),
        len(response.content),
    )
    if not response.ok:
        logger.warning("Response body: %s", response.text)

    return response
