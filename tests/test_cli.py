#!/usr/bin/env python3
"""
CLI Tests for PartnerAgents.

Tests the CLI functionality including partner extraction, rich formatting, and error handling.

Run with: pytest tests/test_cli.py -v
"""

import sys
import asyncio
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def test_rich_available():
    """Test that rich library is available."""
    from scripts.partner_agents import cli

    assert cli.RICH_AVAILABLE is True


def test_console_created():
    """Test that console is created when rich is available."""
    from scripts.partner_agents import cli

    assert cli.console is not None


def test_print_banner():
    """Test banner printing doesn't crash."""
    from scripts.partner_agents.cli import print_banner

    print_banner()


def test_print_help():
    """Test help printing doesn't crash."""
    from scripts.partner_agents.cli import print_help

    print_help()


def test_print_response_dict():
    """Test response printing with dict input."""
    from scripts.partner_agents.cli import print_response

    response = {
        "response": "Hello world",
        "agent": "test",
    }
    print_response(response)


def test_print_response_empty():
    """Test response printing with empty input."""
    from scripts.partner_agents.cli import print_response

    print_response({})


def test_cli_module_imports():
    """Test that CLI module can be imported."""
    from scripts.partner_agents import cli

    assert cli is not None
    assert hasattr(cli, "print_banner")
    assert hasattr(cli, "print_help")
    assert hasattr(cli, "print_response")


def test_get_api_key_env():
    """Test getting API key from environment."""
    import os
    from scripts.partner_agents.cli import get_api_key

    os.environ["OPENROUTER_API_KEY"] = "test-key-123"
    key = get_api_key()
    assert key == "test-key-123"
    del os.environ["OPENROUTER_API_KEY"]


def test_get_model_default():
    """Test default model selection."""
    from scripts.partner_agents.cli import get_model

    model = get_model()
    assert model == "qwen/qwen3.5-plus-02-15"


@pytest.mark.asyncio
async def test_router_partner_extraction_lowercase():
    """Test partner extraction with lowercase input."""
    from scripts.partner_agents import router

    r = router.Router()
    result = await r.route("onboard slalom", {"partners": []})

    assert result.intents
    assert result.intents[0].name == "onboard"
    assert result.intents[0].entities.get("partner_name") == "slalom"


@pytest.mark.asyncio
async def test_router_partner_extraction_uppercase():
    """Test partner extraction with uppercase input."""
    from scripts.partner_agents import router

    r = router.Router()
    result = await r.route("onboard Acme Corp", {"partners": []})

    assert result.intents
    assert result.intents[0].name == "onboard"
    assert result.intents[0].entities.get("partner_name") == "Acme Corp"


@pytest.mark.asyncio
async def test_router_status_skill():
    """Test status skill extraction."""
    from scripts.partner_agents import router

    r = router.Router()
    result = await r.route("status slalom", {"partners": []})

    assert result.intents
    assert "status" in result.intents[0].name
    assert result.intents[0].entities.get("partner_name") == "slalom"


@pytest.mark.asyncio
async def test_router_roi_skill():
    """Test ROI skill extraction (no partner needed)."""
    from scripts.partner_agents import router

    r = router.Router()
    result = await r.route("roi", {"partners": []})

    assert result.intents
    assert "roi" in result.intents[0].name


@pytest.mark.asyncio
async def test_conversation_context():
    """Test that last_partner is used when partner is omitted."""
    from scripts.partner_agents.cli import send_message

    # First message with partner
    response1 = await send_message("status slalom", "", "qwen/qwen3.5-plus-02-15")
    assert response1.get("partner") == "slalom"

    # Second message without partner - should use context
    response2 = await send_message(
        "status", "", "qwen/qwen3.5-plus-02-15", last_partner="slalom"
    )
    assert "slalom" in response2.get("response", "")


def test_readline_available():
    """Test that readline import works."""
    from scripts.partner_agents.cli import READLINE_AVAILABLE

    # readline should be available on macOS/Linux
    assert READLINE_AVAILABLE is True
