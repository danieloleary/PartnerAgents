"""Test Partner Onboarding Flow
Tests the complete partner lifecycle using the test partner."""

import os
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"


def test_first_partner_path_documents_exist():
    """Verify all documents in First Partner Path exist."""
    required_docs = [
        "docs/strategy/02-ideal-partner-profile.md",
        "docs/recruitment/10-icp-tracker.md",
        "docs/recruitment/01-email-sequence.md",
        "docs/recruitment/03-qualification-framework.md",
        "docs/recruitment/04-discovery-call.md",
        "docs/recruitment/05-pitch-deck.md",
        "docs/recruitment/07-proposal.md",
        "docs/recruitment/08-agreement.md",
        "docs/recruitment/09-onboarding.md",
        "docs/enablement/01-roadmap.md",
    ]

    missing = []
    for doc in required_docs:
        if not (REPO_ROOT / doc).exists():
            missing.append(doc)

    assert len(missing) == 0, f"Missing documents: {missing}"


def test_onboarding_path_document_exists():
    """Verify First Partner Onboarding Path document exists."""
    path = DOCS_DIR / "getting-started" / "first-partner-path.md"
    assert path.exists(), "First Partner Onboarding Path document not found"


def test_test_partner_directory_exists():
    """Verify test partner example exists."""
    test_partner_dir = REPO_ROOT / "examples" / "test-partner"
    assert test_partner_dir.exists(), "Test partner directory not found"

    readme = test_partner_dir / "README.md"
    assert readme.exists(), "Test partner README not found"


def test_onboarding_templates_have_frontmatter():
    """Verify onboarding path templates have required frontmatter."""
    templates = [
        DOCS_DIR / "strategy" / "02-ideal-partner-profile.md",
        DOCS_DIR / "recruitment" / "01-email-sequence.md",
        DOCS_DIR / "recruitment" / "07-proposal.md",
        DOCS_DIR / "recruitment" / "09-onboarding.md",
    ]

    missing_frontmatter = []
    for template in templates:
        if template.exists():
            with open(template, "r") as f:
                content = f.read()
                if not content.startswith("---"):
                    missing_frontmatter.append(str(template))

    assert len(missing_frontmatter) == 0, (
        f"Templates missing frontmatter: {missing_frontmatter}"
    )


def test_getting_started_folder_structure():
    """Verify getting-started folder has all expected documents."""
    gs_dir = DOCS_DIR / "getting-started"

    expected = [
        "quick-start.md",
        "first-partner-path.md",
        "lifecycle.md",
        "how-to-use.md",
    ]

    missing = []
    for doc in expected:
        if not (gs_dir / doc).exists():
            missing.append(doc)

    assert len(missing) == 0, f"Missing getting-started documents: {missing}"


def test_examples_directory_structure():
    """Verify examples directory has correct structure."""
    examples_dir = REPO_ROOT / "examples"

    # Check main directories exist
    assert (examples_dir / "complete-examples").exists(), "complete-examples missing"
    assert (examples_dir / "demo-company").exists(), "demo-company missing"
    assert (examples_dir / "test-partner").exists(), "test-partner missing"


if __name__ == "__main__":
    print("Running PartnerAgents Onboarding Tests...\n")

    print("1. test_first_partner_path_documents_exist...")
    test_first_partner_path_documents_exist()
    print("   PASS")

    print("\n2. test_onboarding_path_document_exists...")
    test_onboarding_path_document_exists()
    print("   PASS")

    print("\n3. test_test_partner_directory_exists...")
    test_test_partner_directory_exists()
    print("   PASS")

    print("\n4. test_onboarding_templates_have_frontmatter...")
    test_onboarding_templates_have_frontmatter()
    print("   PASS")

    print("\n5. test_getting_started_folder_structure...")
    test_getting_started_folder_structure()
    print("   PASS")

    print("\n6. test_examples_directory_structure...")
    test_examples_directory_structure()
    print("   PASS")

    print("\n=== All Onboarding Tests Passed! ===")
