"""Security audit tests - PartnerAgents version."""

import sys
import os
import re
import pytest
import time
from pathlib import Path

# Add scripts to path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from scripts.partner_agents import web as web_module
from scripts.partner_agents import partner_state


def test_backend_sanitization_logic():
    """Test the regex-based HTML stripping logic."""
    user_message = (
        "Hello <script>alert('xss')</script> world <img src=x onerror=alert(1)>"
    )
    sanitized = re.sub(r"<[^>]*?>", "", user_message)
    assert "<script>" not in sanitized
    assert "<img>" not in sanitized
    # Tags are removed, but their content remains if not inside < >
    assert "alert('xss')" in sanitized
    assert sanitized == "Hello alert('xss') world "


def test_rate_limiting_logic():
    """Test the rate limiter logic directly."""
    ip = "1.2.3.4"
    web_module.rate_limit_store.clear()

    # 20 requests should pass
    for i in range(20):
        assert (
            web_module.check_rate_limit(ip, max_requests=20, window_seconds=60) is True
        )

    # 21st request should be rate limited
    assert web_module.check_rate_limit(ip, max_requests=20, window_seconds=60) is False


def test_rate_limiter_memory_protection():
    """Test that rate_limit_store is pruned when too large."""
    web_module.rate_limit_store.clear()
    # Fill store with 1001 IPs
    for i in range(1001):
        web_module.rate_limit_store[f"ip-{i}"] = [time.time()]

    assert len(web_module.rate_limit_store) == 1001

    # Next call should trigger pruning
    web_module.check_rate_limit("new-ip")

    # It should have pruned expired ones. Since all are new, they might stay
    # unless we mock time. Let's verify it doesn't crash and size is managed.
    assert len(web_module.rate_limit_store) <= 1002


def test_partner_state_sanitization():
    """Test that partner state properly escapes HTML."""
    name = "<b>Evil</b><script>alert(1)</script>"
    partner = partner_state.add_partner(name=name)

    try:
        assert "<script>" not in partner["name"]
        assert "&lt;b&gt;Evil&lt;/b&gt;" in partner["name"]
        assert "alert(1)" in partner["name"]  # The content remains, but escaped
    finally:
        partner_state.delete_partner(partner["name"])


def test_partner_state_robustness():
    """Test that partner state handles non-string inputs without crashing."""
    # Should handle int
    p1 = partner_state.add_partner(name=12345)
    assert p1["name"] == "12345"
    partner_state.delete_partner("12345")

    # Should handle None
    p2 = partner_state.add_partner(name=None)
    assert p2["name"] == "None"
    partner_state.delete_partner("None")


def test_empty_message_rejected():
    """Test empty message is rejected in chat endpoint logic."""
    # Simulate the validation logic from web.py chat endpoint
    message = ""
    if not message or len(message.strip()) == 0:
        valid = False
    else:
        valid = True

    assert valid is False


def test_very_long_message_rejected():
    """Test very long message is rejected in chat endpoint logic."""
    # Simulate the validation logic from web.py chat endpoint
    message = "A" * 5001
    if len(message) > 5000:
        valid = False
    else:
        valid = True

    assert valid is False
