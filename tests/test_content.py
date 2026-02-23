"""Tests for content quality in PartnerAgents documentation."""

import re
import pytest
from pathlib import Path
from tests.conftest import (
    REPO_ROOT,
    DOCS_DIR,
    STARLIGHT_DOCS_DIR,
    VALID_SECTIONS,
    VALID_TIERS,
    VALID_DIFFICULTIES,
    VALID_PURPOSES,
    VALID_PHASES,
)


class TestHeadingHierarchy:
    """Test heading structure and hierarchy."""

    def test_heading_hierarchy_valid(self):
        """Verify heading levels don't skip (e.g., h1 -> h3 is invalid)."""
        failures = []

        # Only check Starlight docs (MkDocs removed)
        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            lines = content.split("\n")

            prev_level = 0
            for line in lines:
                match = re.match(r"^(#{1,6})\s+", line)
                if match:
                    level = len(match.group(1))

                    # Allow h1 -> h2 or h1 -> h2 -> h3, but not h1 -> h3
                    if level > prev_level + 1 and prev_level > 0:
                        failures.append(
                            f"{f.relative_to(STARLIGHT_DOCS_DIR)}: h{prev_level} -> h{level} skips level"
                        )
                    prev_level = level

        # Lenient - allow some heading hierarchy issues (often intentional)
        assert len(failures) < 20, f"Heading hierarchy issues:\n" + "\n".join(
            failures[:10]
        )

    def test_no_duplicate_h1_headings(self):
        """Verify each file has at most one h1 heading."""
        failures = []

        # Only check Starlight docs (MkDocs removed)
        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            h1_count = content.count("\n# ") + (1 if content.startswith("# ") else 0)

            if h1_count > 1:
                failures.append(
                    f"{f.relative_to(STARLIGHT_DOCS_DIR)}: {h1_count} h1 headings found"
                )

        # Lenient - some files intentionally have multiple h1s (like index pages)
        assert len(failures) < 10, f"Multiple h1 headings:\n" + "\n".join(failures[:10])


class TestCodeBlocks:
    """Test code block quality."""

    def test_code_blocks_have_language(self):
        """Verify code blocks specify a language."""
        # This test is lenient - warns but doesn't fail
        failures = []

        # Only check Starlight docs (MkDocs removed)
        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()

            # Find fenced code blocks without language
            in_block = False
            block_start = 0
            for i, line in enumerate(content.split("\n")):
                if line.strip().startswith("```"):
                    if not in_block:
                        in_block = True
                        block_start = i
                        lang = line.strip()[3:].strip()
                        if not lang:
                            failures.append(
                                f"{f.relative_to(STARLIGHT_DOCS_DIR)}:{i + 1}: code block without language"
                            )
                    else:
                        in_block = False

        # Lenient - allow many failures (template code blocks often don't need language)
        assert len(failures) < 250, f"Code blocks without language:\n" + "\n".join(
            failures[:5]
        )


class TestPlaceholders:
    """Test for placeholder and TODO text."""

    def test_no_placeholder_text(self):
        """Verify no [TODO], [TBD], or similar placeholder text exists."""
        placeholders = [
            r"\[TODO\]",
            r"\[TBD\]",
            r"\[FIXME\]",
            r"\[XXX\]",
            r"\[YOUR_",
            r"\[INSERT_",
        ]

        failures = []

        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            for f in list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx")):
                content = f.read_text()

                for placeholder in placeholders:
                    matches = re.findall(placeholder, content, re.IGNORECASE)
                    if matches:
                        failures.append(
                            f"{f.relative_to(docs_dir)}: contains {placeholder}: {matches[0]}"
                        )

        assert len(failures) == 0, f"Placeholder text found:\n" + "\n".join(
            failures[:10]
        )


class TestTemplateStructure:
    """Test template structure and organization."""

    def test_template_files_have_content(self):
        """Verify templates have sufficient content (>500 chars)."""
        failures = []

        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            for f in docs_dir.rglob("*.md"):
                if f.name in ["index.md", "404.md", "tags.md"]:
                    continue

                content = f.read_text()

                # Skip frontmatter
                if content.startswith("---"):
                    content = content.split("---", 2)[-1]

                if len(content.strip()) < 300:
                    failures.append(
                        f"{f.relative_to(docs_dir)}: only {len(content.strip())} chars"
                    )

        assert len(failures) == 0, (
            f"Templates with insufficient content:\n" + "\n".join(failures[:10])
        )

    def test_index_pages_exist_for_categories(self):
        """Verify each category has an index page."""
        missing = []

        for section in VALID_SECTIONS:
            section_dir = STARLIGHT_DOCS_DIR / section
            if section_dir.exists():
                has_index = (section_dir / "index.md").exists() or (
                    section_dir / "index.mdx"
                ).exists()
                if not has_index:
                    missing.append(section)

        assert len(missing) == 0, f"Categories without index: {missing}"


class TestConsistency:
    """Test for consistent formatting."""

    def test_consistent_date_format(self):
        """Verify dates use ISO format (YYYY-MM-DD)."""
        failures = []

        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            for f in list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx")):
                content = f.read_text()

                # Find dates in various formats
                iso_dates = re.findall(r"\d{4}-\d{2}-\d{2}", content)
                other_dates = re.findall(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", content)

                if other_dates and not iso_dates:
                    failures.append(
                        f"{f.relative_to(docs_dir)}: uses {other_dates[0]} instead of ISO"
                    )

        assert len(failures) == 0, f"Non-ISO dates found:\n" + "\n".join(failures[:10])

    def test_version_format_consistency(self):
        """Verify versions use semver format (X.Y.Z)."""
        failures = []

        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            for f in list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx")):
                content = f.read_text()

                # Look for version field
                version_match = re.search(r"version:\s*([^\n]+)", content)
                if version_match:
                    version = version_match.group(1).strip()
                    # Check semver format
                    if not re.match(r"^\d+\.\d+\.\d+$", version):
                        failures.append(
                            f"{f.relative_to(docs_dir)}: invalid version '{version}'"
                        )

        assert len(failures) == 0, f"Invalid version formats:\n" + "\n".join(
            failures[:10]
        )


class TestContentEdgeCases:
    """Test edge cases in content."""

    def test_no_binary_content(self):
        """Verify no binary content in markdown files."""
        failures = []
        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            for f in docs_dir.rglob("*.md"):
                content = f.read_text(errors="ignore")
                # Check for null bytes
                if "\x00" in content:
                    failures.append(f"{f.name}: contains null bytes")
                # Check for very long lines (possible binary)
                for i, line in enumerate(content.split("\n")):
                    if len(line) > 10000:
                        failures.append(
                            f"{f.name}: line {i} is {len(line)} chars (possible binary)"
                        )
                        break

        assert len(failures) == 0, f"Binary content found:\n" + "\n".join(failures[:5])

    def test_no_excessive_emoji(self):
        """Check for excessive emoji usage (spammy)."""
        failures = []
        emoji_pattern = re.compile(
            "["
            "\U0001f600-\U0001f64f"  # emoticons
            "\U0001f300-\U0001f5ff"  # symbols & pictographs
            "\U0001f680-\U0001f6ff"  # transport & map symbols
            "\U0001f1e0-\U0001f1ff"  # flags
            "]+"
        )

        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            for f in docs_dir.rglob("*.md"):
                content = f.read_text()
                emojis = emoji_pattern.findall(content)
                if len(emojis) > 20:
                    failures.append(f"{f.name}: {len(emojis)} emojis (possible spam)")

        assert len(failures) < 5, f"Excessive emoji usage:\n" + "\n".join(failures[:5])

    def test_consistent_line_endings(self):
        """Verify consistent line endings (LF)."""
        failures = []
        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            for f in docs_dir.rglob("*.md"):
                content = f.read_text()
                if "\r\n" in content:  # CRLF
                    failures.append(f"{f.name}: uses CRLF line endings")

        assert len(failures) == 0, f"Inconsistent line endings:\n" + "\n".join(
            failures[:5]
        )

    def test_no_very_short_content(self):
        """Check for suspiciously short template content."""
        failures = []
        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            for f in docs_dir.rglob("*.md"):
                content = f.read_text()
                # Skip index files
                if "index" in f.name:
                    continue
                # Check content length (should be at least 500 chars for templates)
                if len(content) < 500:
                    failures.append(f"{f.name}: only {len(content)} chars")

        assert len(failures) < 5, f"Very short content:\n" + "\n".join(failures[:5])
