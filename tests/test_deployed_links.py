"""Tests for deployed site link correctness."""

import re
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = REPO_ROOT / "partneros-docs" / "dist"
DOCS_DIR = REPO_ROOT / "partneros-docs" / "src" / "content" / "docs"


class TestDeployedLinks:
    """Verify links work correctly in deployed site."""

    def test_dist_directory_exists(self):
        """Verify dist directory exists (run build first)."""
        if not DIST_DIR.exists():
            pytest.skip("Run 'npm run build' first")

    def test_no_absolute_partneros_links_in_source(self):
        """Verify source docs don't use hardcoded /PartnerAgents/ links."""
        failures = []

        # Skip example/documentation files that intentionally show links
        skip_files = [
            "skills/find-broken-links.md",  # Shows example links as documentation
        ]

        for f in DOCS_DIR.rglob("*.md"):
            rel_path = str(f.relative_to(DOCS_DIR))
            if any(skip in rel_path for skip in skip_files):
                continue

            content = f.read_text()
            matches = re.findall(r"\]\(/PartnerAgents/[^)]+\)", content)
            if matches:
                failures.append(f"{rel_path}: {matches}")

        for f in DOCS_DIR.rglob("*.mdx"):
            rel_path = str(f.relative_to(DOCS_DIR))
            if any(skip in rel_path for skip in skip_files):
                continue

            content = f.read_text()
            matches = re.findall(r"\]\(/PartnerAgents/[^)]+\)", content)
            if matches:
                failures.append(f"{rel_path}: {matches}")

        assert len(failures) == 0, (
            f"Found absolute /PartnerAgents links in source (use relative links instead):\n"
            + "\n".join(failures)
        )

    def test_no_absolute_root_links_in_source(self):
        """Verify source docs don't use absolute / links (breaks deployed site).

        Links like [foo](/foo/) will work locally but 404 on deployed site
        because base is /PartnerAgents. Use relative links (../foo/) instead.
        """
        failures = []

        # Patterns that indicate broken absolute links
        # Exclude Starlight hero action 'link:' which uses absolute paths
        for f in DOCS_DIR.rglob("*.md"):
            content = f.read_text()
            # Find markdown links starting with / but not in code blocks
            in_code_block = False
            for i, line in enumerate(content.split("\n"), 1):
                stripped = line.strip()
                if stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue
                # Match markdown links like [text](/some-path/)
                matches = re.findall(r"\]\(/[a-z][^)]*\)", line)
                if matches:
                    rel_path = f.relative_to(DOCS_DIR)
                    failures.append(f"{rel_path}:{i} - {matches}")

        for f in DOCS_DIR.rglob("*.mdx"):
            content = f.read_text()
            in_code_block = False
            for i, line in enumerate(content.split("\n"), 1):
                stripped = line.strip()
                if stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue
                # Skip Starlight hero action links (they use 'link:' YAML)
                if "link:" in line:
                    continue
                matches = re.findall(r"\]\(/[a-z][^)]*\)", line)
                if matches:
                    rel_path = f.relative_to(DOCS_DIR)
                    failures.append(f"{rel_path}:{i} - {matches}")

        assert len(failures) == 0, (
            f"Found absolute / links in source - these will 404 on deployed site!\n"
            f"Use relative links (../folder/) instead.\n" + "\n".join(failures[:20])
        )

    def test_relative_links_in_built_site(self):
        """Verify built site uses correct links for navigation.

        Starlight auto-handles the base URL. Hero actions should have
        /PartnerAgents/ prefix (configured in index.mdx).
        """
        index_html = DIST_DIR / "index.html"
        if not index_html.exists():
            pytest.skip("Build required")

        content = index_html.read_text()

        # Hero actions SHOULD have /PartnerAgents/ prefix now (fixed in index.mdx)
        assert 'href="/PartnerAgents/getting-started/' in content, (
            "Hero links should have /PartnerAgents/ prefix in built HTML"
        )
        assert 'href="/PartnerAgents/strategy/' in content, (
            "Hero links should have /PartnerAgents/ prefix in built HTML"
        )

    def test_base_url_config_present(self):
        """Verify astro.config.mjs has correct site and base configuration."""
        config_path = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
        content = config_path.read_text()

        assert "base:" in content, "Missing base URL config"
        assert "site:" in content, "Missing site URL config"
        assert "/PartnerAgents" in content, "base should be set to /PartnerAgents"

    def test_build_produces_valid_html(self):
        """Verify build produces valid HTML with correct base."""
        index_html = DIST_DIR / "index.html"
        if not index_html.exists():
            pytest.skip("Build required")

        content = index_html.read_text()

        # Should have correct base path in assets
        assert "/PartnerAgents/_astro/" in content, (
            "Assets should reference /PartnerAgents/_astro/"
        )

    def test_assets_use_base_url(self):
        """Verify CSS/JS assets use the base URL."""
        index_html = DIST_DIR / "index.html"
        if not index_html.exists():
            pytest.skip("Build required")

        content = index_html.read_text()

        # Find asset references
        astro_assets = re.findall(r'href="(/PartnerAgents/_astro/[^"]+)"', content)
        assert len(astro_assets) > 0, "Should have Astro assets with base URL"
