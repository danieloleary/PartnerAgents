
import sys
import os
from collections import OrderedDict, deque
from pathlib import Path
import pytest

# Add scripts to path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

# Import app and caches
from partner_agents.web import app, rate_limit_store, response_cache, MAX_CACHE_SIZE

def test_gzip_middleware_enabled():
    """Verify GZip middleware is active if using real FastAPI."""
    if hasattr(app, "user_middleware"):
        # Real FastAPI
        middleware_names = [m.cls.__name__ for m in app.user_middleware if hasattr(m, "cls")]
        assert "GZipMiddleware" in middleware_names
    else:
        # Using FastAPI shim
        pytest.skip("Using FastAPI shim, cannot verify middleware via user_middleware attribute")

def test_cache_data_structures():
    """Verify caches use OrderedDict for efficient LRU pruning."""
    assert isinstance(rate_limit_store, OrderedDict)
    assert isinstance(response_cache, OrderedDict)

def test_rate_limit_pruning():
    """Verify rate limit store prunes oldest entries when exceeding MAX_CACHE_SIZE."""
    from partner_agents.web import check_rate_limit

    # Clear store for testing
    rate_limit_store.clear()

    # Fill store
    for i in range(MAX_CACHE_SIZE + 10):
        check_rate_limit(f"192.168.1.{i}")

    assert len(rate_limit_store) <= MAX_CACHE_SIZE
    # The first 10 should have been pruned (0 to 9)
    assert "192.168.1.0" not in rate_limit_store
    assert "192.168.1.9" not in rate_limit_store
    assert f"192.168.1.{MAX_CACHE_SIZE + 9}" in rate_limit_store
