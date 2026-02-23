#!/usr/bin/env python3
"""
Test utilities for PartnerAgents Chat Orchestrator tests.

Provides helper functions for:
- Partner creation/cleanup
- Rate limit testing
- Document cleanup
- Memory management
- HTTP client mocking
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from unittest.mock import MagicMock

# Add scripts to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from partner_agents import partner_state, chat_orchestrator


# ============================================================================
# PARTNER STATE HELPERS
# ============================================================================


def create_test_partner(
    name: str, tier: str = "Bronze", email: str = ""
) -> Dict[str, Any]:
    """Create a test partner and return the partner dict.

    Args:
        name: Partner company name
        tier: Partner tier (Bronze/Silver/Gold)
        email: Contact email

    Returns:
        Partner dict with id, name, tier, etc.
    """
    import time

    unique_name = f"{name}_{int(time.time() * 1000000)}"
    return partner_state.add_partner(name=unique_name, tier=tier, email=email)


def cleanup_test_partner(name: str) -> bool:
    """Delete test partner if exists.

    Args:
        name: Partner name to delete

    Returns:
        True if deleted, False if not found
    """
    return partner_state.delete_partner(name)


def get_test_partner(name: str) -> Optional[Dict[str, Any]]:
    """Get partner by name.

    Args:
        name: Partner name to look up

    Returns:
        Partner dict or None if not found
    """
    return partner_state.get_partner(name)


def cleanup_all_test_partners(prefix: str = "Test") -> int:
    """Clean up all test partners with given prefix.

    Args:
        prefix: Name prefix to match (default: "Test")

    Returns:
        Number of partners cleaned up
    """
    partners = partner_state.list_partners()
    count = 0
    for p in partners:
        if p["name"].startswith(prefix):
            partner_state.delete_partner(p["name"])
            count += 1
    return count


# ============================================================================
# RATE LIMIT HELPERS
# ============================================================================


def reset_rate_limits():
    """Reset rate limit store for testing.

    Note: This clears the in-memory rate limit tracking.
    In production tests, you'd need to patch the rate_limit_store.
    """
    # This is a no-op for in-memory store
    # Tests should use mocking instead
    pass


def get_rate_limit_status(ip: str = "test") -> Dict[str, Any]:
    """Get current rate limit status for an IP.

    Args:
        ip: Client IP address

    Returns:
        Dict with count, oldest_timestamp, etc.
    """
    from scripts.partner_agents.web import rate_limit_store, RATE_LIMIT, RATE_WINDOW

    now = time.time()
    if ip not in rate_limit_store:
        return {"count": 0, "remaining": RATE_LIMIT, "reset_time": now + RATE_WINDOW}

    # Filter to active requests
    active = [t for t in rate_limit_store[ip] if now - t < RATE_WINDOW]

    return {
        "count": len(active),
        "remaining": max(0, RATE_LIMIT - len(active)),
        "reset_time": now + RATE_WINDOW,
    }


# ============================================================================
# DOCUMENT HELPERS
# ============================================================================


def cleanup_test_documents(partner_name: str):
    """Remove test documents for a partner.

    Args:
        partner_name: Partner name
    """
    import document_generator

    docs = document_generator.list_documents(partner_name)
    for doc in docs:
        path = Path(doc["path"])
        if path.exists():
            path.unlink()


def get_partner_documents_dir(partner_name: str) -> Path:
    """Get the documents directory for a partner.

    Args:
        partner_name: Partner name

    Returns:
        Path to documents directory
    """
    from scripts.partner_agents.document_generator import _slugify, DOCUMENTS_DIR

    slug = _slugify(partner_name)
    return DOCUMENTS_DIR / slug / "documents"


# ============================================================================
# MEMORY HELPERS
# ============================================================================


def clear_test_memory(conv_id: str = "test") -> bool:
    """Clear test conversation memory.

    Args:
        conv_id: Conversation ID to clear

    Returns:
        True if cleared
    """
    chat_orchestrator.memory.clear(conv_id)
    return True


def get_memory_file(conv_id: str) -> Path:
    """Get path to memory file for a conversation.

    Args:
        conv_id: Conversation ID

    Returns:
        Path to memory JSON file
    """
    return chat_orchestrator.memory._conversation_file(conv_id)


def cleanup_test_memory_files():
    """Clean up all test memory files."""
    mem_dir = chat_orchestrator.memory.memory_dir
    if mem_dir.exists():
        for f in mem_dir.glob("test*.json"):
            f.unlink()


# ============================================================================
# MOCK HELPERS
# ============================================================================


def mock_llm_response(response: str) -> MagicMock:
    """Create a mock LLM client that returns a specific response.

    Args:
        response: Response string to return

    Returns:
        Mock callable
    """
    mock = MagicMock()
    mock.return_value = response
    return mock


def mock_llm_error(error: Exception) -> MagicMock:
    """Create a mock LLM client that raises an error.

    Args:
        error: Exception to raise

    Returns:
        Mock callable that raises
    """
    mock = MagicMock()
    mock.side_effect = error
    return mock


def create_api_request_body(
    message: str,
    api_key: str = "test_key_123456789012345",
    model: str = "qwen/qwen3.5-plus-02-15",
) -> Dict[str, Any]:
    """Create a properly formatted API request body.

    Args:
        message: User message
        api_key: API key
        model: Model name

    Returns:
        Dict suitable for json= parameter
    """
    return {"message": message, "apiKey": api_key, "model": model}


# ============================================================================
# ASSERTION HELPERS
# ============================================================================


def assert_partner_exists(name: str) -> None:
    """Assert a partner exists.

    Args:
        name: Partner name

    Raises:
        AssertionError: If partner doesn't exist
    """
    partner = partner_state.get_partner(name)
    assert partner is not None, f"Partner '{name}' should exist"


def assert_partner_not_exists(name: str) -> None:
    """Assert a partner does not exist.

    Args:
        name: Partner name

    Raises:
        AssertionError: If partner exists
    """
    partner = partner_state.get_partner(name)
    assert partner is None, f"Partner '{name}' should not exist"


def assert_document_exists(partner_name: str, doc_type: str) -> None:
    """Assert a document exists for a partner.

    Args:
        partner_name: Partner name
        doc_type: Document type (nda, msa, dpa)

    Raises:
        AssertionError: If document doesn't exist
    """
    import document_generator

    path = document_generator.generator.get_document_path(partner_name, doc_type)
    assert path is not None and path.exists(), (
        f"Document '{doc_type}' should exist for '{partner_name}'"
    )


# ============================================================================
# TEST FIXTURES
# ============================================================================

import pytest


@pytest.fixture
def test_partner_name():
    """Generate a unique test partner name."""
    import time

    return f"TestPartner_{int(time.time() * 1000000)}"


@pytest.fixture
def test_partner(test_partner_name):
    """Create a test partner and clean up after test."""
    partner = partner_state.add_partner(name=test_partner_name, tier="Bronze")
    yield partner
    partner_state.delete_partner(test_partner_name)


@pytest.fixture
def test_memory_conv_id():
    """Generate unique conversation ID and clean up after test."""
    import time

    conv_id = f"test_{int(time.time() * 1000000)}"
    yield conv_id
    chat_orchestrator.memory.clear(conv_id)
    # Also delete the file
    mem_file = get_memory_file(conv_id)
    if mem_file.exists():
        mem_file.unlink()


@pytest.fixture
def mock_llm():
    """Provide a mock LLM client."""
    return mock_llm_response("Test response from mock LLM")
