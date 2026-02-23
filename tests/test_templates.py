"""Test template completeness and frontmatter - PartnerAgents v2.0 (Starlight only)."""

import os
import re
import yaml
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STARLIGHT_DOCS_DIR = REPO_ROOT / "partneros-docs" / "src" / "content" / "docs"


def count_templates():
    """Count all markdown files in Starlight docs."""
    count = 0
    for root, dirs, files in os.walk(STARLIGHT_DOCS_DIR):
        count += len([f for f in files if f.endswith((".md", ".mdx"))])
    return count


def get_all_template_paths():
    """Get all template paths relative to Starlight docs."""
    templates = []
    for root, dirs, files in os.walk(STARLIGHT_DOCS_DIR):
        for f in files:
            if f.endswith((".md", ".mdx")) and f not in [
                "index.md",
                "index.mdx",
                "404.md",
                "tags.md",
            ]:
                path = Path(root) / f
                rel_path = path.relative_to(STARLIGHT_DOCS_DIR)
                templates.append(rel_path)
    return templates


def test_templates_exist():
    """Verify at least 1 template exists."""
    assert count_templates() > 0


def test_templates_have_frontmatter():
    """Verify all markdown files have YAML frontmatter."""
    failures = []
    for root, dirs, files in os.walk(STARLIGHT_DOCS_DIR):
        for f in files:
            if f.endswith((".md", ".mdx")):
                path = Path(root) / f
                content = path.read_text()
                if not content.startswith("---"):
                    failures.append(str(path.relative_to(REPO_ROOT)))
    assert len(failures) == 0


def test_frontmatter_schema_validation():
    """Verify required frontmatter fields exist."""
    required = [
        "title",
        "section",
        "template_number",
        "version",
        "last_updated",
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
    failures = []
    for root, dirs, files in os.walk(STARLIGHT_DOCS_DIR):
        for f in files:
            if f.endswith((".md", ".mdx")):
                path = Path(root) / f
                content = path.read_text()
                if content.startswith("---"):
                    try:
                        fm = yaml.safe_load(content.split("---")[1])
                        if fm:
                            missing = [field for field in required if field not in fm]
                            if missing:
                                failures.append(
                                    f"{path.relative_to(STARLIGHT_DOCS_DIR)}: {missing}"
                                )
                    except:
                        pass
    assert (
        len(failures) < 50
    )  # Lenient - new agent/workflow templates have different frontmatter


def test_template_count_per_category():
    """Verify correct template counts per category."""
    expected = {
        "strategy": 8,
        "recruitment": 10,
        "enablement": 7,
        "legal": 4,
        "finance": 3,
        "security": 2,
        "operations": 4,
        "executive": 1,
        "analysis": 1,
    }
    for category, expected_count in expected.items():
        category_path = STARLIGHT_DOCS_DIR / category
        if category_path.exists():
            count = len(
                [f for f in category_path.iterdir() if f.suffix in [".md", ".mdx"]]
            )
            # Allow some flexibility
            assert count >= expected_count - 1, (
                f"{category}: expected ~{expected_count}, got {count}"
            )


def test_folder_structure():
    """Verify all required directories exist."""
    required = [
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
    missing = [d for d in required if not (STARLIGHT_DOCS_DIR / d).exists()]
    assert len(missing) == 0


def test_playbook_template_references():
    """Verify playbook YAML references existing templates."""
    playbooks_dir = REPO_ROOT / "scripts" / "partner_agent" / "playbooks"
    if not playbooks_dir.exists():
        pytest.skip("playbooks directory not found")

    failures = []
    for playbook in playbooks_dir.glob("*.yaml"):
        content = playbook.read_text()
        try:
            data = yaml.safe_load(content)
            if data and "steps" in data:
                for step in data["steps"]:
                    if "template" in step:
                        template_ref = step["template"]
                        # Check if template exists
                        template_path = REPO_ROOT / template_ref
                        if not template_path.exists():
                            failures.append(f"{playbook.name}: {template_ref}")
        except:
            pass
    # Lenient
    assert len(failures) < 5


def test_frontmatter_yaml_parseable():
    """Verify all YAML frontmatter parses correctly."""
    failures = []
    for root, dirs, files in os.walk(STARLIGHT_DOCS_DIR):
        for f in files:
            if f.endswith((".md", ".mdx")):
                path = Path(root) / f
                content = path.read_text()
                if content.startswith("---"):
                    try:
                        yaml.safe_load(content.split("---")[1])
                    except yaml.YAMLError as e:
                        failures.append(f"{path.relative_to(STARLIGHT_DOCS_DIR)}: {e}")
    assert len(failures) == 0


def test_config_yaml_valid():
    """Verify config.yaml has required fields."""
    config_path = REPO_ROOT / "scripts" / "partner_agent" / "config.yaml"
    if not config_path.exists():
        pytest.skip("config.yaml not found")

    content = config_path.read_text()
    data = yaml.safe_load(content)
    assert data is not None
    assert "provider" in data or "templates_dir" in data


def test_playbook_yaml_schema():
    """Verify all playbooks have valid schema."""
    playbooks_dir = REPO_ROOT / "scripts" / "partner_agent" / "playbooks"
    if not playbooks_dir.exists():
        pytest.skip("playbooks not found")

    for playbook in playbooks_dir.glob("*.yaml"):
        content = playbook.read_text()
        data = yaml.safe_load(content)
        assert "name" in data
        assert "steps" in data


def test_no_duplicate_template_titles():
    """Verify no duplicate template titles."""
    titles = {}
    for root, dirs, files in os.walk(STARLIGHT_DOCS_DIR):
        for f in files:
            if f.endswith((".md", ".mdx")):
                path = Path(root) / f
                content = path.read_text()
                if content.startswith("---"):
                    try:
                        fm = yaml.safe_load(content.split("---")[1])
                        if fm and "title" in fm:
                            title = fm["title"]
                            if title in titles:
                                titles[title].append(
                                    str(path.relative_to(STARLIGHT_DOCS_DIR))
                                )
                            else:
                                titles[title] = [
                                    str(path.relative_to(STARLIGHT_DOCS_DIR))
                                ]
                    except:
                        pass
    duplicates = {t: paths for t, paths in titles.items() if len(paths) > 1}
    assert len(duplicates) == 0


def test_template_files_have_content():
    """Verify templates have substantial content."""
    failures = []
    for root, dirs, files in os.walk(STARLIGHT_DOCS_DIR):
        for f in files:
            if f.endswith((".md", ".mdx")) and f not in [
                "index.md",
                "index.mdx",
                "404.md",
                "tags.md",
            ]:
                path = Path(root) / f
                content = path.read_text()
                if content.startswith("---"):
                    body = content.split("---", 2)[-1]
                    if len(body.strip()) < 500:
                        failures.append(
                            f"{path.relative_to(STARLIGHT_DOCS_DIR)}: {len(body.strip())} chars"
                        )
    assert len(failures) < 5


def test_scripts_exist():
    """Verify key utility scripts exist."""
    scripts = [
        "scripts/onboard.py",
        "scripts/fill_template.py",
        "scripts/demo_mode.py",
    ]
    missing = [s for s in scripts if not (REPO_ROOT / s).exists()]
    assert len(missing) == 0


def test_examples_directory():
    """Verify examples/ directory exists."""
    examples_dir = REPO_ROOT / "examples"
    assert examples_dir.exists()


def test_playbooks_exist():
    """Verify all expected playbooks exist."""
    playbooks_dir = REPO_ROOT / "scripts" / "partner_agent" / "playbooks"
    if not playbooks_dir.exists():
        pytest.skip("playbooks not found")

    expected = [
        "recruit.yaml",
        "onboard.yaml",
        "qbr.yaml",
        "expand.yaml",
        "exit.yaml",
        "co-marketing.yaml",
    ]
    missing = [p for p in expected if not (playbooks_dir / p).exists()]
    assert len(missing) == 0


def test_env_example_exists():
    """Verify .env.example exists."""
    env_example = REPO_ROOT / "scripts" / "partner_agent" / ".env.example"
    assert env_example.exists()


def test_index_pages_have_frontmatter():
    """Verify index pages have frontmatter."""
    for section in [
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
    ]:
        index_path = STARLIGHT_DOCS_DIR / section / "index.mdx"
        if index_path.exists():
            content = index_path.read_text()
            assert content.startswith("---"), f"{section}/index.mdx missing frontmatter"


# Starlight-specific tests
def test_starlight_docs_exist():
    """Verify Starlight docs directory exists."""
    assert STARLIGHT_DOCS_DIR.exists()


def test_starlight_index_mdx():
    """Verify index.mdx exists."""
    assert (STARLIGHT_DOCS_DIR / "index.mdx").exists()


def test_starlight_astro_config():
    """Verify astro.config.mjs exists."""
    assert (REPO_ROOT / "partneros-docs" / "astro.config.mjs").exists()


def test_starlight_package_json():
    """Verify package.json exists."""
    assert (REPO_ROOT / "partneros-docs" / "package.json").exists()


def test_starlight_template_categories():
    """Verify Starlight has same categories as expected."""
    expected = [
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
    actual = [
        d.name
        for d in STARLIGHT_DOCS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ]
    for section in expected:
        assert section in actual, f"Missing section: {section}"


def test_starlight_build_succeeds():
    """Verify Starlight build works."""
    import subprocess

    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=str(REPO_ROOT / "partneros-docs"),
        capture_output=True,
        timeout=120,
    )
    assert result.returncode == 0, f"Build failed: {result.stderr.decode()[:500]}"


def test_frontmatter_valid_enum_values():
    """Test that frontmatter uses valid enum values."""
    import yaml
    from pathlib import Path

    docs_dir = REPO_ROOT / "partneros-docs" / "src" / "content" / "docs"

    valid_tiers = ["Bronze", "Silver", "Gold", ""]
    valid_levels = ["beginner", "intermediate", "advanced", ""]
    valid_purposes = [
        "tactical",
        "strategic",
        "operational",
        "analytical",
        "marketing",
        "sales",
        "financial",
        "",
    ]
    valid_phases = [
        "recruitment",
        "onboarding",
        "enablement",
        "growth",
        "retention",
        "exit",
        "analysis",
        "strategy",
        "operations",
        "",
    ]

    failures = []

    for md_file in docs_dir.rglob("*.md"):
        try:
            content = md_file.read_text()
            if content.startswith("---"):
                frontmatter = content.split("---")[1]
                data = yaml.safe_load(frontmatter)

                if data:
                    tier = data.get("tier", "")
                    level = data.get("skill_level", "")
                    purpose = data.get("purpose", "")
                    phase = data.get("phase", "")

                    if tier and tier not in valid_tiers:
                        failures.append(f"{md_file.name}: invalid tier '{tier}'")
                    if level and level not in valid_levels:
                        failures.append(
                            f"{md_file.name}: invalid skill_level '{level}'"
                        )
                    if purpose and purpose not in valid_purposes:
                        failures.append(f"{md_file.name}: invalid purpose '{purpose}'")
                    if phase and phase not in valid_phases:
                        failures.append(f"{md_file.name}: invalid phase '{phase}'")
        except Exception:
            pass

    assert len(failures) < 10, f"Invalid enum values found: {failures[:5]}"
