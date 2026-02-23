#!/usr/bin/env python3
"""Simple Markdown linter for PartnerAgents repository."""

import sys
from pathlib import Path


def lint_file(path: Path) -> int:
    """Return number of lint errors for the given file."""
    errors = 0
    raw = path.read_text()
    content = raw.splitlines()
    for idx, line in enumerate(content, 1):
        if line.rstrip() != line:
            print(f"{path}:{idx}: trailing whitespace")
            errors += 1
        if line.startswith("##") and not line.startswith("###"):
            # allow '##', '###', etc. - ensure space after '#'
            if len(line) > 2 and line[2] != " ":
                print(f"{path}:{idx}: missing space after heading hashes")
                errors += 1
    if raw and not raw.endswith("\n"):
        print(f"{path}: EOF missing newline")
        errors += 1
    # check for shell prompt text
    if content and content[-1].startswith("root@"):
        print(f"{path}:{len(content)}: extraneous shell prompt line")
        errors += 1
    return errors


def main(paths):
    errors = 0
    for path in paths:
        errors += lint_file(path)
    if errors:
        print(f"\n{errors} lint errors found")
    else:
        print("All markdown files pass linting")
    return 1 if errors else 0


if __name__ == "__main__":
    # Target only Starlight docs (partneros-docs/src/content/docs/)
    md_files = list(Path("partneros-docs/src/content/docs/").rglob("*.md"))
    md_files += list(Path("partneros-docs/src/content/docs/").rglob("*.mdx"))
    sys.exit(main(md_files))
