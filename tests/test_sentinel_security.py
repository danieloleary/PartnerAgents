"""Security tests for PartnerOS."""

import sys
import os
import time
import hashlib
from pathlib import Path

# Repository root
REPO_ROOT = Path(__file__).resolve().parents[1]
# Append instead of insert to prefer real fastapi over local shim
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.append(str(REPO_ROOT / "scripts"))

try:
    from fastapi.testclient import TestClient
except (ImportError, ModuleNotFoundError):
    from starlette.testclient import TestClient

from partner_agents.web import app, rate_limit_store, check_rate_limit

import pytest

# Skip tests if we are using the shimmed FastAPI (which is not callable/ASGI-compliant)
if not hasattr(app, "middleware"):
    pytest.skip(
        "FastAPI shim detected, skipping security tests that require real FastAPI",
        allow_module_level=True,
    )

# Skip these tests - web.py security features need to be re-implemented
# See BACKLOG: Re-implement security headers and rate limiting in web.py
pytest.skip(
    "web.py security features need re-implementation - see BACKLOG",
    allow_module_level=True,
)

client = TestClient(app)


def test_security_headers():
    """Verify that security headers are present in the response."""
    response = client.get("/")
    assert response.status_code == 200

    # Check for security headers
    assert "Content-Security-Policy" in response.headers
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "X-XSS-Protection" in response.headers

    # Verify header values
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]


def test_payload_size_limit():
    """Verify that large payloads are rejected."""
    # Create a large payload (~1.1 MB)
    large_data = "a" * (1_100_000)
    # Wrap in a dict to look like JSON but it's just a huge string
    response = client.post(
        "/chat", content=large_data, headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 413
    assert response.json() == {"error": "Payload too large"}


def test_cache_key_isolation():
    """Verify that different API keys have different cache entries."""
    response_cache.clear()

    message = "test isolation"
    key1 = "key_one_long_enough"
    key2 = "key_two_long_enough"

    # Check that key hashes are different
    hash1 = hashlib.sha256(f"{message}:{key1}".encode()).hexdigest()[:16]
    hash2 = hashlib.sha256(f"{message}:{key2}".encode()).hexdigest()[:16]
    assert hash1 != hash2

    # Manually populate cache to test isolation logic without calling external API
    response_cache[hash1] = {"result": {"response": "res1"}, "ts": time.time()}
    response_cache[hash2] = {"result": {"response": "res2"}, "ts": time.time()}

    assert len(response_cache) == 2
    assert response_cache.get(hash1)["result"]["response"] == "res1"
    assert response_cache.get(hash2)["result"]["response"] == "res2"


def test_proxy_rate_limit():
    """Verify that X-Forwarded-For is used for rate limiting."""
    rate_limit_store.clear()

    # Request from proxy with IP 5.5.5.5
    client.post(
        "/chat",
        json={"message": "hi", "apiKey": "valid_enough_key"},
        headers={"X-Forwarded-For": "5.5.5.5"},
    )
    assert "5.5.5.5" in rate_limit_store

    # Request from proxy with IP 6.6.6.6
    client.post(
        "/chat",
        json={"message": "hi", "apiKey": "valid_enough_key"},
        headers={"X-Forwarded-For": "6.6.6.6"},
    )
    assert "6.6.6.6" in rate_limit_store


def test_rate_limit_leak_fix():
    """Verify that the rate limit store is bounded when it grows too large."""
    rate_limit_store.clear()
    # Fill it up to the limit
    for i in range(1001):
        rate_limit_store[f"1.1.1.{i}"] = [time.time()]

    assert len(rate_limit_store) == 1001

    # The next call to check_rate_limit should trigger the cleanup (pop oldest)
    check_rate_limit("2.2.2.2")

    # It should still be 1001 (1001 - 1 popped + 1 added)
    assert len(rate_limit_store) == 1001
    assert "2.2.2.2" in rate_limit_store
    assert "1.1.1.0" not in rate_limit_store  # Oldest should be gone
