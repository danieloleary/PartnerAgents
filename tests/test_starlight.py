"""Tests for Starlight (Astro) documentation configuration and structure."""

import pytest
from pathlib import Path
from tests.conftest import REPO_ROOT, STARLIGHT_DOCS_DIR, VALID_SECTIONS


class TestStarlightStructure:
    """Test Starlight directory and file structure."""

    def test_starlight_docs_directory_exists(self):
        """Verify Starlight docs directory exists."""
        assert STARLIGHT_DOCS_DIR.exists(), "partneros-docs/src/content/docs/ not found"

    def test_starlight_index_mdx_exists(self):
        """Verify homepage index.mdx exists."""
        index_path = STARLIGHT_DOCS_DIR / "index.mdx"
        assert index_path.exists(), "index.mdx not found"

    def test_starlight_astro_config_exists(self):
        """Verify astro.config.mjs exists."""
        config_path = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
        assert config_path.exists(), "astro.config.mjs not found"

    def test_starlight_package_json_exists(self):
        """Verify package.json exists."""
        package_path = REPO_ROOT / "partneros-docs" / "package.json"
        assert package_path.exists(), "package.json not found"

    def test_starlight_categories_exist(self):
        """Verify all expected category directories exist."""
        missing = []
        for section in VALID_SECTIONS:
            section_dir = STARLIGHT_DOCS_DIR / section
            if not section_dir.exists():
                missing.append(section)
        assert len(missing) == 0, f"Missing directories: {missing}"

    def test_starlight_index_mdx_all_categories(self):
        """Verify every category has an index.mdx file."""
        missing = []
        for section in VALID_SECTIONS:
            section_dir = STARLIGHT_DOCS_DIR / section
            if section_dir.exists():
                index_file = section_dir / "index.mdx"
                if not index_file.exists():
                    missing.append(f"{section}/index.mdx")
        assert len(missing) == 0, f"Missing index.mdx files: {missing}"


class TestStarlightFrontmatter:
    """Test Starlight-specific frontmatter fields."""

    def test_starlight_index_has_hero(self):
        """Verify homepage has Starlight hero configuration."""
        index_path = STARLIGHT_DOCS_DIR / "index.mdx"
        content = index_path.read_text()

        assert "hero:" in content or "template: splash" in content, (
            "Homepage missing Starlight hero configuration"
        )

    def test_starlight_index_has_card_import(self):
        """Verify homepage imports Starlight Card components."""
        index_path = STARLIGHT_DOCS_DIR / "index.mdx"
        content = index_path.read_text()

        assert "import { Card" in content or "import { CardGrid" in content, (
            "Homepage should import Starlight Card components"
        )


class TestStarlightConfiguration:
    """Test Starlight configuration files."""

    def test_astro_config_has_base_url(self):
        """Verify astro.config.mjs has base URL configured."""
        config_path = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
        content = config_path.read_text()

        assert "base:" in content, "astro.config.mjs should have base URL"
        assert "/PartnerAgents" in content, "Base URL should be /PartnerAgents"

    def test_astro_config_has_sidebar(self):
        """Verify astro.config.mjs has sidebar configuration."""
        config_path = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
        content = config_path.read_text()

        assert "sidebar:" in content, "astro.config.mjs should have sidebar config"

    def test_astro_config_has_custom_css(self):
        """Verify custom CSS is configured."""
        config_path = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
        content = config_path.read_text()

        assert "customCss:" in content or "extra.css" in content, (
            "Custom CSS should be configured"
        )

    def test_astro_config_has_title(self):
        """Verify site title is configured."""
        config_path = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
        content = config_path.read_text()

        assert "title:" in content, "Site title should be configured"


class TestStarlightComponents:
    """Test Starlight component usage in MDX files."""

    def test_category_indexes_use_card_grid(self):
        """Verify category index pages use CardGrid component."""
        cards_used = 0
        missing_imports = []

        for section in VALID_SECTIONS:
            index_path = STARLIGHT_DOCS_DIR / section / "index.mdx"
            if index_path.exists():
                content = index_path.read_text()
                if "<CardGrid" in content:
                    cards_used += 1
                    if "import" not in content or "CardGrid" not in content:
                        missing_imports.append(f"{section}/index.mdx")

        assert cards_used > 0, "No CardGrid components found"
        assert len(missing_imports) == 0, f"Missing CardGrid imports: {missing_imports}"

    def test_mdx_files_have_frontmatter(self):
        """Verify all MDX files have YAML frontmatter."""
        failures = []

        for mdx_file in STARLIGHT_DOCS_DIR.rglob("*.mdx"):
            content = mdx_file.read_text()
            if not content.startswith("---"):
                failures.append(str(mdx_file.relative_to(STARLIGHT_DOCS_DIR)))

        assert len(failures) == 0, f"MDX files without frontmatter: {failures}"
