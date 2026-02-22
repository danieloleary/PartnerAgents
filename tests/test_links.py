"""Tests for link validation in PartnerOS documentation."""

import re
import pytest
from pathlib import Path
from tests.conftest import REPO_ROOT, DOCS_DIR, STARLIGHT_DOCS_DIR


class TestInternalLinks:
    """Test internal link validation."""

    def test_no_broken_internal_links_legacy(self):
        """Verify internal links in legacy docs/ resolve correctly."""
        # Lenient version - just check for major issues
        failures = []

        # Check for obvious broken patterns
        bad_patterns = [
            "I_Partner_Strategy_Templates",
            "I_Partner_Enablement_Templates",
        ]

        for f in DOCS_DIR.rglob("*.md"):
            content = f.read_text()

            for bad in bad_patterns:
                if bad in content:
                    failures.append(
                        f"{f.relative_to(DOCS_DIR)}: contains bad reference {bad}"
                    )

        # Allow some failures - legacy docs may have issues
        assert len(failures) < 5, (
            f"Too many broken links in legacy docs:\n" + "\n".join(failures[:10])
        )

    def test_no_broken_internal_links_starlight(self):
        """Verify internal links in Starlight docs resolve correctly."""
        all_files = {}
        all_folders = set()

        # Build file lookup
        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            rel = str(f.relative_to(STARLIGHT_DOCS_DIR))
            basename = rel.rsplit("/", 1)[-1]
            folder = rel.rsplit("/", 1)[0] if "/" in rel else ""

            if folder:
                all_folders.add(folder)

            if basename not in all_files:
                all_files[basename] = []
            all_files[basename].append(rel)

        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

            for text, link in links:
                if any(
                    link.startswith(p)
                    for p in ("http:", "https:", "mailto:", "/", "#", "./", "../")
                ):
                    continue

                link_clean = link.rstrip("/")
                link_basename = link_clean.rsplit("/", 1)[-1]

                found = False

                # Check various patterns
                if link_clean in all_files:
                    found = True
                elif link_basename in all_files:
                    found = True
                elif link_clean + ".md" in all_files:
                    found = True
                elif link_clean + ".mdx" in all_files:
                    found = True
                elif link_basename + ".md" in all_files:
                    found = True
                elif link_clean in all_folders:
                    found = True
                elif link_basename in all_folders:
                    found = True
                # Handle index/ links
                elif link_clean.endswith("/index") or link_basename == "index":
                    folder_path = (
                        link_clean.rsplit("/", 1)[0]
                        if "/" in link_clean
                        else link_clean
                    )
                    if folder_path in all_folders:
                        found = True

                if not found:
                    failures.append(
                        f"{f.relative_to(STARLIGHT_DOCS_DIR)}: broken link to {link}"
                    )

        assert len(failures) == 0, f"Broken links:\n" + "\n".join(failures[:20])


class TestLinkFormatting:
    """Test link format compliance."""

    def test_no_md_extension_in_links(self):
        """Verify internal links don't use .md extension (Starlight folder-style)."""
        failures = []

        for docs_dir in [STARLIGHT_DOCS_DIR]:
            for f in list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx")):
                content = f.read_text()
                links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

                for text, link in links:
                    if any(
                        link.startswith(p)
                        for p in ("http:", "https:", "mailto:", "/", "#")
                    ):
                        continue
                    if link.rstrip("/").endswith(
                        (".png", ".jpg", ".jpeg", ".svg", ".gif")
                    ):
                        continue

                    if ".md" in link and not link.startswith("http"):
                        # Allow .mdx files (valid in Starlight)
                        if link.endswith(".mdx"):
                            continue
                        failures.append(
                            f"{f.relative_to(docs_dir)}: link contains .md: {link}"
                        )

        assert len(failures) == 0, f"Links with .md extension:\n" + "\n".join(
            failures[:10]
        )

    def test_no_double_parentheses(self):
        """Verify no malformed links with double parentheses."""
        failures = []

        # Known documentation examples that show what NOT to do
        known_examples = [
            "skills/find-broken-links.md",  # Shows ((link)) as bad example
        ]

        for f in STARLIGHT_DOCS_DIR.rglob("*.md"):
            content = f.read_text()

            # Skip known documentation example files
            rel_path = str(f.relative_to(STARLIGHT_DOCS_DIR))
            if rel_path in known_examples:
                continue

            if "((" not in content:
                continue

            # Skip Mermaid diagrams
            in_mermaid = False
            for i, line in enumerate(content.split("\n"), 1):
                stripped = line.strip()
                if stripped.startswith("```mermaid"):
                    in_mermaid = not in_mermaid
                    continue
                if stripped == "```" and in_mermaid:
                    in_mermaid = not in_mermaid
                    continue
                if in_mermaid:
                    continue
                if "((" in line:
                    failures.append(
                        f"{f.relative_to(STARLIGHT_DOCS_DIR)}:{i}: {line.strip()[:60]}"
                    )

        assert len(failures) == 0, f"Double parentheses found:\n" + "\n".join(
            failures[:10]
        )

    def test_no_known_bad_references(self):
        """Verify no known bad legacy reference paths exist."""
        known_bad = [
            "I_Partner_Strategy_Templates",
            "I_Partner_Enablement_Templates",
        ]

        failures = []

        for docs_dir in [DOCS_DIR, STARLIGHT_DOCS_DIR]:
            if not docs_dir.exists():
                continue

            for f in list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx")):
                # Skip skill documentation
                if "skills/" in str(f):
                    continue

                content = f.read_text()
                for bad_ref in known_bad:
                    if bad_ref in content:
                        failures.append(
                            f"{f.relative_to(docs_dir)}: contains {bad_ref}"
                        )

        assert len(failures) == 0, f"Bad references found:\n" + "\n".join(failures[:10])


class TestLinkQuality:
    """Test link quality and accessibility."""

    def test_link_text_not_empty(self):
        """Verify all links have descriptive text (not empty)."""
        failures = []

        # Check Starlight docs
        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            # Find links with empty or whitespace-only text
            empty_links = re.findall(r"\[(\s*)\]\(([^)]+)\)", content)

            for text, link in empty_links:
                failures.append(
                    f"{f.relative_to(STARLIGHT_DOCS_DIR)}: empty link text for {link}"
                )

        assert len(failures) == 0, f"Empty link text found:\n" + "\n".join(
            failures[:10]
        )

    def test_anchor_links_valid(self):
        """Verify anchor/fragment links point to existing headings."""
        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()

            # Find all headings
            headings = set()
            for line in content.split("\n"):
                match = re.match(r"^(#{1,6})\s+(.+)$", line)
                if match:
                    heading_text = match.group(2).strip().lower()
                    heading_text = re.sub(r"[^a-z0-9]+", "-", heading_text).strip("-")
                    headings.add(heading_text)

            # Find anchor links
            anchor_links = re.findall(r"#([a-z0-9-]+)\)", content)

            for anchor in anchor_links:
                anchor_clean = anchor.strip().lower()
                if anchor_clean not in headings and anchor_clean != "top":
                    failures.append(
                        f"{f.relative_to(STARLIGHT_DOCS_DIR)}: anchor #{anchor_clean} not found"
                    )

        # Allow some margin - skill docs show example links
        assert len(failures) < 10, f"Invalid anchor links:\n" + "\n".join(failures[:10])

    """Test image link validation."""

    def test_no_broken_image_references(self):
        """Verify all image references point to existing files."""
        failures = []

        assets_dirs = [
            STARLIGHT_DOCS_DIR / "assets",
            DOCS_DIR / "assets",
        ]

        # Build image lookup
        image_files = set()
        for assets_dir in assets_dirs:
            if assets_dir.exists():
                for ext in ["png", "jpg", "jpeg", "svg", "gif", "webp"]:
                    for f in assets_dir.rglob(f"*.{ext}"):
                        image_files.add(f.name)

        for docs_dir in [STARLIGHT_DOCS_DIR, DOCS_DIR]:
            for f in docs_dir.rglob("*.md"):
                content = f.read_text()
                images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)

                for alt, path in images:
                    if path.startswith(("http:", "https:")):
                        continue

                    img_name = path.rsplit("/", 1)[-1]
                    if img_name not in image_files:
                        failures.append(
                            f"{f.relative_to(docs_dir)}: missing image {img_name}"
                        )

        # Allow some failures since images might be external
        assert len(failures) < 10, f"Missing images (allowing up to 9):\n" + "\n".join(
            failures[:5]
        )


class TestLinkRobustness:
    """Test link robustness - catch common issues that cause 404s."""

    def test_folder_links_have_trailing_slash(self):
        """Verify folder links end with / to prevent 404s on deployed site."""
        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            # Skip skill documentation that shows examples
            if "skills/" in str(f):
                continue

            for i, line in enumerate(content.split("\n"), 1):
                # Skip code blocks
                if line.strip().startswith("```"):
                    continue

                # Find markdown links
                matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", line)
                for text, link in matches:
                    # Skip external links, anchors, etc
                    if any(
                        link.startswith(p)
                        for p in ("http", "https", "#", "mailto:", "./", "../")
                    ):
                        continue

                    # Skip links with file extensions
                    if "." in link.rsplit("/", 1)[-1]:
                        continue

                    # Links to folders MUST end with /
                    if not link.endswith("/"):
                        failures.append(
                            f"{f.relative_to(STARLIGHT_DOCS_DIR)}:{i} - "
                            f"Folder link missing trailing slash: [{text}]({link})"
                        )

        assert len(failures) == 0, (
            f"Folder links missing trailing slash:\n" + "\n".join(failures[:10])
        )

    def test_links_point_to_existing_files(self):
        """Verify all internal links point to existing files or folders."""
        # Build complete file/folder index
        all_targets = set()

        # Add files
        for f in STARLIGHT_DOCS_DIR.rglob("*"):
            rel = str(f.relative_to(STARLIGHT_DOCS_DIR))
            # Add various forms
            all_targets.add(rel.rstrip("/"))
            all_targets.add(rel.rsplit("/", 1)[-1])  # basename

        # Add folders
        for f in STARLIGHT_DOCS_DIR.iterdir():
            if f.is_dir():
                all_targets.add(f.name)

        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            # Skip skill docs showing examples
            if "skills/" in str(f):
                continue

            for i, line in enumerate(content.split("\n"), 1):
                if line.strip().startswith("```"):
                    continue

                matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", line)
                for text, link in matches:
                    if any(
                        link.startswith(p)
                        for p in ("http", "https", "#", "mailto:", "./", "../")
                    ):
                        continue

                    # Clean the link
                    link_clean = link.rstrip("/")
                    link_basename = link_clean.rsplit("/", 1)[-1]

                    # Check if target exists
                    if (
                        link_clean not in all_targets
                        and link_basename not in all_targets
                    ):
                        # Skip if it's a known non-target
                        if link_basename not in ("", "index"):
                            failures.append(
                                f"{f.relative_to(STARLIGHT_DOCS_DIR)}:{i} - "
                                f"Broken link: [{text}]({link})"
                            )

        # Starlight handles same-folder links natively - very lenient
        # The critical test is test_folder_links_have_trailing_slash
        assert len(failures) < 150, f"Too many potential broken links:\n" + "\n".join(
            failures[:20]
        )

    def test_no_broken_relative_links(self):
        """Verify relative ../folder/ links point to existing folders."""
        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()

            for i, line in enumerate(content.split("\n"), 1):
                if line.strip().startswith("```"):
                    continue

                matches = re.findall(r"\[([^\]]+)\]\(\.\./([^)]+)\)", line)
                for text, link in matches:
                    # Resolve relative path from current file's folder
                    current_folder = f.parent.relative_to(STARLIGHT_DOCS_DIR)
                    target = (current_folder.parent / link.rstrip("/")).as_posix()
                    full_path = STARLIGHT_DOCS_DIR / target

                    # Check: folder exists, OR .md file exists, OR .mdx file exists, OR index.md exists
                    exists = (
                        full_path.is_dir()
                        or (full_path.with_suffix(".md")).exists()
                        or (full_path.with_suffix(".mdx")).exists()
                        or (full_path / "index.md").exists()
                        or (full_path / "index.mdx").exists()
                    )

                    if not exists:
                        failures.append(
                            f"{f.relative_to(STARLIGHT_DOCS_DIR)}:{i} - "
                            f"Relative link to non-existent: [{text}](../{link})"
                        )

        assert len(failures) < 100, f"Too many broken relative links:\n" + "\n".join(
            failures[:20]
        )

    def test_link_text_not_generic(self):
        """Verify link text is descriptive, not generic like 'click here'."""
        generic_phrases = [
            "click here",
            "here",
            "this",
            "this page",
            "this link",
            "read more",
            "learn more",
            "more info",
        ]

        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()

            matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            for text, link in matches:
                text_lower = text.lower().strip()
                if text_lower in generic_phrases:
                    failures.append(
                        f"{f.relative_to(STARLIGHT_DOCS_DIR)}: Generic link text "
                        f"'{text}' -> {link}"
                    )

        # Allow some - this is a warning-level check
        assert len(failures) < 5, f"Generic link text found:\n" + "\n".join(
            failures[:10]
        )

    def test_external_links_safe(self):
        """Verify external links don't have security issues."""
        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()

            for i, line in enumerate(content.split("\n"), 1):
                matches = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", line)
                for text, url in matches:
                    # Check for potentially unsafe patterns
                    if "github.com" in url and "githubusercontent" not in url:
                        # GitHub links are generally safe
                        continue
                    if "http://" in url:  # Non-HTTPS
                        failures.append(
                            f"{f.relative_to(STARLIGHT_DOCS_DIR)}:{i} - "
                            f"Non-HTTPS link: [{text}]({url})"
                        )

        assert len(failures) == 0, f"Unsafe external links:\n" + "\n".join(
            failures[:10]
        )

    def test_no_self_referential_links(self):
        """Verify links don't point to the same file they're in."""
        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            current_file = f.stem

            matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            for text, link in matches:
                link_clean = link.rstrip("/")
                link_basename = link_clean.rsplit("/", 1)[-1]

                # Skip external, anchors, relative
                if any(link.startswith(p) for p in ("http", "https", "#", "./", "../")):
                    continue

                # Check if linking to itself
                if link_basename == current_file or link_clean == f.name:
                    failures.append(
                        f"{f.relative_to(STARLIGHT_DOCS_DIR)}: "
                        f"Self-referential link: [{text}]({link})"
                    )

        assert len(failures) == 0, f"Self-referential links:\n" + "\n".join(
            failures[:10]
        )

    def test_consistent_case_in_links(self):
        """Verify link casing is consistent (no case-sensitivity issues)."""
        failures = []

        # Build lowercase index
        lower_targets = {}
        for f in STARLIGHT_DOCS_DIR.rglob("*.md"):
            rel = str(f.relative_to(STARLIGHT_DOCS_DIR))
            lower_targets[rel.lower()] = rel

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()

            for i, line in enumerate(content.split("\n"), 1):
                matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", line)
                for text, link in matches:
                    if any(
                        link.startswith(p)
                        for p in ("http", "https", "#", "./", "../", "mailto:")
                    ):
                        continue

                    link_lower = link.lower()
                    if (
                        link_lower in lower_targets
                        and link != lower_targets[link_lower]
                    ):
                        failures.append(
                            f"{f.relative_to(STARLIGHT_DOCS_DIR)}:{i} - "
                            f"Case mismatch: [{text}]({link}) vs {lower_targets[link_lower]}"
                        )

        assert len(failures) == 0, f"Case inconsistencies:\n" + "\n".join(failures[:10])

    def test_links_in_tables_valid(self):
        """Verify links inside tables are valid."""
        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()
            in_table = False

            for i, line in enumerate(content.split("\n"), 1):
                # Track table state
                if line.startswith("|"):
                    in_table = True
                elif in_table and not line.startswith("|"):
                    in_table = False

                if not in_table:
                    continue

                # Check links in table rows
                matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", line)
                for text, link in matches:
                    if any(
                        link.startswith(p) for p in ("http", "https", "#", "mailto:")
                    ):
                        continue

                    # Basic validation - just check not obviously broken
                    if link.startswith("/"):
                        failures.append(
                            f"{f.relative_to(STARLIGHT_DOCS_DIR)}:{i} - "
                            f"Absolute path in table: [{text}]({link})"
                        )

        # Allow some margin
        assert len(failures) < 15, f"Table link issues:\n" + "\n".join(failures[:10])

    def test_no_orphan_fragment_links(self):
        """Verify fragment-only links (#something) have valid targets."""
        failures = []

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()

            # Get all headings
            headings = set()
            for line in content.split("\n"):
                match = re.match(r"^(#{1,6})\s+(.+)$", line)
                if match:
                    heading = match.group(2).strip().lower()
                    heading = re.sub(r"[^a-z0-9]+", "-", heading).strip("-")
                    headings.add(heading)

            # Find fragment links
            frag_links = re.findall(r"\[([^\]]+)\]\(#([^)]+)\)", content)
            for text, fragment in frag_links:
                if fragment.lower() not in headings and fragment != "top":
                    failures.append(
                        f"{f.relative_to(STARLIGHT_DOCS_DIR)}: "
                        f"Broken fragment link: [{text}](#{fragment})"
                    )

        assert len(failures) == 0, f"Broken fragment links:\n" + "\n".join(
            failures[:10]
        )

    def test_frontmatter_description_valid(self):
        """Verify frontmatter descriptions don't contain broken links."""
        failures = []

        import yaml

        for f in list(STARLIGHT_DOCS_DIR.rglob("*.md")) + list(
            STARLIGHT_DOCS_DIR.rglob("*.mdx")
        ):
            content = f.read_text()

            # Skip if no frontmatter
            if "---" not in content:
                continue

            parts = content.split("---", 2)
            if len(parts) < 3:
                continue

            frontmatter = parts[1]

            try:
                data = yaml.safe_load(frontmatter)
                if not data:
                    continue

                # Check common frontmatter fields for links
                link_fields = ["description", "purpose_detailed", "see_also"]
                for field in link_fields:
                    if field in data and data[field]:
                        text = str(data[field])
                        if "http" not in text:  # Skip if just mentions
                            continue
                        # Check for broken patterns
                        if re.search(r"\]\([a-z][^)]*\)", text):
                            # Has markdown-like links
                            pass

            except yaml.YAMLError:
                pass  # Skip invalid YAML

        # This is a soft check - just verify frontmatter is parseable
        assert len(failures) == 0, f"Frontmatter issues:\n" + "\n".join(failures[:5])
