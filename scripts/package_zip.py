#!/usr/bin/env python3
"""
package_zip.py - Package PartnerOS as a self-contained .zip for distribution.

Creates a zip that works without git — just unzip and go.

Usage:
    python scripts/package_zip.py                          # Full package
    python scripts/package_zip.py --templates-only         # Docs/templates only
    python scripts/package_zip.py --output dist/           # Custom output dir
    python scripts/package_zip.py --version 1.3.0          # Tag the release
"""

import argparse
import json
import os
import zipfile
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# Files and directories to always include
ALWAYS_INCLUDE = [
    "README.md",
    "BACKLOG.md",
    "ARCHITECTURE.md",
    "CHANGELOG.md",
    "TEMPLATE_INVENTORY.md",
]

ALWAYS_INCLUDE_DIRS = [
    "partneros-docs/",
    "examples/",
]

# Additional files for the full package (not templates-only)
FULL_PACKAGE_DIRS = [
    "scripts/",
    "tests/",
]

FULL_PACKAGE_FILES = [
    "package.json",
    ".pre-commit-config.yaml",
]

# Never include these patterns
EXCLUDE_PATTERNS = [
    ".git/",
    ".github/",
    "__pycache__/",
    "*.pyc",
    ".pytest_cache/",
    "site/",
    ".cache/",
    "node_modules/",
    "*.egg-info/",
    ".env",
    ".company-config/",
    "scripts/partner_agent/state/",
    "exports/",
    "dist/",
]


def should_exclude(path: Path) -> bool:
    """Return True if this path should be excluded from the zip."""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern.endswith("/"):
            if f"/{pattern[:-1]}/" in f"/{path_str}/" or path_str.startswith(
                pattern[:-1]
            ):
                return True
        elif path.match(pattern):
            return True
    return False


def collect_files(templates_only: bool) -> list:
    """Return list of (abs_path, zip_path) tuples."""
    files = []
    prefix = "PartnerOS/"

    # Always-include individual files
    for fname in ALWAYS_INCLUDE:
        p = REPO_ROOT / fname
        if p.exists():
            files.append((p, prefix + fname))

    # Always-include directories
    for d in ALWAYS_INCLUDE_DIRS:
        dir_path = REPO_ROOT / d.rstrip("/")
        if dir_path.exists():
            for f in dir_path.rglob("*"):
                if f.is_file() and not should_exclude(f.relative_to(REPO_ROOT)):
                    rel = f.relative_to(REPO_ROOT)
                    files.append((f, prefix + str(rel)))

    if not templates_only:
        # Full package extras
        for d in FULL_PACKAGE_DIRS:
            dir_path = REPO_ROOT / d.rstrip("/")
            if dir_path.exists():
                for f in dir_path.rglob("*"):
                    if f.is_file() and not should_exclude(f.relative_to(REPO_ROOT)):
                        rel = f.relative_to(REPO_ROOT)
                        files.append((f, prefix + str(rel)))

        for fname in FULL_PACKAGE_FILES:
            p = REPO_ROOT / fname
            if p.exists():
                files.append((p, prefix + fname))

    # Deduplicate preserving order
    seen = set()
    deduped = []
    for item in files:
        if item[1] not in seen:
            seen.add(item[1])
            deduped.append(item)

    return deduped


def build_manifest(files: list, version: str, templates_only: bool) -> dict:
    """Build a manifest dict describing the package contents."""
    categories = {}
    for _, zip_path in files:
        parts = zip_path.split("/")
        if len(parts) >= 3 and parts[1] == "docs":
            cat = parts[2] if len(parts) > 3 else "root"
            categories[cat] = categories.get(cat, 0) + 1

    return {
        "name": "PartnerOS",
        "version": version,
        "packaged_at": datetime.now().isoformat(),
        "package_type": "templates-only" if templates_only else "full",
        "file_count": len(files),
        "template_categories": categories,
        "source": "https://github.com/danieloleary/PartnerAgents",
        "docs": "https://danieloleary.github.io/PartnerAgents",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Package PartnerOS as a distributable zip"
    )
    parser.add_argument(
        "--templates-only",
        action="store_true",
        help="Include only docs/ and essential files (no scripts/tests)",
    )
    parser.add_argument(
        "--output", "-o", default="dist", help="Output directory (default: dist/)"
    )
    parser.add_argument(
        "--version",
        "-v",
        default=datetime.now().strftime("%Y.%m.%d"),
        help="Version string for the zip filename",
    )
    args = parser.parse_args()

    out_dir = REPO_ROOT / args.output
    out_dir.mkdir(parents=True, exist_ok=True)

    suffix = "-templates-only" if args.templates_only else ""
    zip_name = f"PartnerOS-{args.version}{suffix}.zip"
    zip_path = out_dir / zip_name

    print(f"Collecting files...")
    files = collect_files(templates_only=args.templates_only)
    print(f"  {len(files)} files to package")

    manifest = build_manifest(files, args.version, args.templates_only)
    manifest_json = json.dumps(manifest, indent=2)

    print(f"Building {zip_name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        # Write manifest
        zf.writestr("PartnerOS/PACKAGE_MANIFEST.json", manifest_json)

        # Write a getting-started README at the root of the zip
        root_readme = (
            "# PartnerOS\n\n"
            "The complete playbook for building and scaling strategic partnerships.\n\n"
            "## Quick Start\n\n"
            "1. Open `docs/getting-started/quick-start.md`\n"
            "2. Follow the setup guide\n"
            "3. Run `python scripts/onboard.py` to customize for your company\n\n"
            "## Documentation\n\n"
            "- Online: https://danieloleary.github.io/PartnerAgents\n"
            "- GitHub: https://github.com/danieloleary/PartnerAgents\n\n"
            f"Package version: {args.version}\n"
            f"Packaged: {manifest['packaged_at'][:10]}\n"
        )
        zf.writestr("PartnerOS/GETTING_STARTED.md", root_readme)

        # Write all collected files
        for abs_path, zip_entry in files:
            zf.write(abs_path, zip_entry)

    size_kb = zip_path.stat().st_size // 1024
    print(f"\n✓  Package created: {zip_path}")
    print(f"   Size: {size_kb} KB")
    print(f"   Files: {len(files)} + manifest")
    if args.templates_only:
        print(f"   Type: Templates only (no scripts/tests)")
    else:
        print(f"   Type: Full package")

    # Print category breakdown
    print("\nTemplate categories included:")
    for cat, count in sorted(manifest["template_categories"].items()):
        print(f"  {cat}: {count} files")


if __name__ == "__main__":
    main()
