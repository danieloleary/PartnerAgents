"""Shared fixtures and constants for PartnerAgents tests."""

import pytest
from pathlib import Path

# Repository root
REPO_ROOT = Path(__file__).resolve().parents[1]

# Key directories
# DOCS_DIR is deprecated - we now use Starlight only (partneros-docs)
DOCS_DIR = REPO_ROOT / "docs"  # Deprecated - kept for backward compat only
STARLIGHT_DOCS_DIR = REPO_ROOT / "partneros-docs" / "src" / "content" / "docs"
PARTNER_AGENT_DIR = REPO_ROOT / "scripts" / "partner_agent"

# Valid categories
VALID_SECTIONS = [
    "strategy",
    "recruitment",
    "enablement",
    "legal",
    "finance",
    "security",
    "operations",
    "executive",
    "analysis",
    "agent",
    "getting-started",
]

# Valid tier values
VALID_TIERS = ["Bronze", "Silver", "Gold"]

# Valid difficulty values
VALID_DIFFICULTIES = ["easy", "medium", "hard"]

# Valid purpose values
VALID_PURPOSES = [
    "strategic",
    "operational",
    "tactical",
    "legal",
    "financial",
    "security",
    "executive",
    "analytical",
]

# Valid phase values
VALID_PHASES = [
    "recruitment",
    "onboarding",
    "enablement",
    "growth",
    "retention",
    "exit",
    "strategy",
    "operations",
    "analysis",
]

# Required frontmatter fields
REQUIRED_FIELDS = [
    "title",
    "section",
    "category",
    "template_number",
    "version",
    "last_updated",
    "author",
    "tier",
    "skill_level",
    "purpose",
    "phase",
    "time_required",
    "difficulty",
    "prerequisites",
    "description",
    "outcomes",
    "skills_gained",
]


@pytest.fixture
def repo_root():
    """Return the repository root path."""
    return REPO_ROOT


@pytest.fixture
def docs_dir():
    """Return the legacy docs directory."""
    return DOCS_DIR


@pytest.fixture
def starlight_docs_dir():
    """Return the Starlight docs directory."""
    return STARLIGHT_DOCS_DIR


@pytest.fixture
def valid_sections():
    """Return list of valid section names."""
    return VALID_SECTIONS
