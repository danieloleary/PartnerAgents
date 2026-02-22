#!/usr/bin/env python3
"""Fix all internal links for Starlight compatibility.

Rules:
- Same folder: 06-template.md -> 06-template/ (no ../)
- Cross folder: ../folder/06-template.md -> ../folder/06-template/
- Never use .md in links for Starlight

This script:
1. Removes .md extension from all internal links
2. Adds trailing slash for folder-style routing
3. Preserves ../ relative paths
"""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "partneros-docs" / "src" / "content" / "docs"


def fix_links(content, filepath):
    """Fix all internal links in a file."""
    original = content

    def replace_link(match):
        text = match.group(1)
        link = match.group(2)

        # Skip external links
        if link.startswith(("http:", "https:", "mailto:", "#", "/")):
            return match.group(0)

        # Skip image links
        link_clean = link.rstrip("/")
        if link_clean.endswith((".png", ".jpg", ".jpeg", ".svg", ".gif")):
            return match.group(0)

        # Clean up the link
        link = link.strip()

        # Skip empty links
        if not link:
            return match.group(0)

        # Ensure .md extension for better tool compatibility (Lychee, etc.)
        # Starlight handles .md extensions automatically during build.
        if not link.endswith((".md", ".mdx", "/")):
            # Check if .md file exists
            if (filepath.parent / (link + ".md")).exists():
                link = link + ".md"
            elif (filepath.parent / (link + ".mdx")).exists():
                link = link + ".mdx"

        return f"]({link})"

    # Match markdown links: [text](link) where link contains .md
    pattern = r"(\[([^\]]+)\]\(([^)]+)\)"

    def replacer(m):
        link = m.group(2)
        text = m.group(1)

        # Skip external links
        if any(link.startswith(p) for p in ("http:", "https:", "mailto:", "#", "/")):
            return m.group(0)

        # Skip image links
        link_clean = link.rstrip("/")
        if link_clean.endswith((".png", ".jpg", ".jpeg", ".svg", ".gif")):
            return m.group(0)

        # Ensure extension
        if not link.endswith((".md", ".mdx", "/")):
            if (filepath.parent / (link + ".md")).exists():
                link = link + ".md"
            elif (filepath.parent / (link + ".mdx")).exists():
                link = link + ".mdx"

        return f"]({link})"

    # Find all links and process them
    links = re.findall(r"(\[([^\]]+)\]\(([^)]+)\))", content)

    for full_match, text, link in links:
        # Skip external
        if any(link.startswith(p) for p in ("http:", "https:", "mailto:", "#", "/")):
            continue

        # Skip images
        link_clean = link.rstrip("/")
        if link_clean.endswith((".png", ".jpg", ".jpeg", ".svg", ".gif")):
            continue

        # Fix the link
        new_link = link
        if not new_link.endswith((".md", ".mdx", "/")):
            if (filepath.parent / (new_link + ".md")).exists():
                new_link = new_link + ".md"
            elif (filepath.parent / (new_link + ".mdx")).exists():
                new_link = new_link + ".mdx"

        # Replace
        old_link = f"]({link})"
        new_link_full = f"]({new_link})"
        content = content.replace(old_link, new_link_full)

    return content


def process_file(filepath):
    """Process a single file."""
    content = filepath.read_text()
    new_content = fix_links(content, filepath)

    if new_content != content:
        filepath.write_text(new_content)
        return True
    return False


def main():
    count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if process_file(md_file):
            print(f"Fixed: {md_file.relative_to(DOCS_DIR)}")
            count += 1

    print(f"\nTotal files updated: {count}")


if __name__ == "__main__":
    main()
