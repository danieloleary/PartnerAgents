#!/usr/bin/env python3
"""
Template Generator
Creates new templates with standardized frontmatter from CLI prompts.

Usage:
    python scripts/generate_template.py --category legal --name "nda"
    python scripts/generate_template.py --category finance --name "commission" --interactive
"""

import os
import argparse
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"

CATEGORIES = {
    "strategy": {"section": "Strategy", "category": "strategic", "phase": "strategy"},
    "recruitment": {
        "section": "Recruitment",
        "category": "operational",
        "phase": "recruitment",
    },
    "enablement": {
        "section": "Enablement",
        "category": "tactical",
        "phase": "enablement",
    },
    "getting-started": {
        "section": "Getting Started",
        "category": "operational",
        "phase": "onboarding",
    },
    "legal": {"section": "Legal", "category": "legal", "phase": "recruitment"},
    "finance": {"section": "Finance", "category": "financial", "phase": "operational"},
    "security": {
        "section": "Security",
        "category": "compliance",
        "phase": "recruitment",
    },
}

DEFAULT_SKILL_LEVEL = "intermediate"
DEFAULT_PURPOSE = "operational"
DEFAULT_DIFFICULTY = "medium"
DEFAULT_TIER = ["Bronze", "Silver", "Gold"]


def get_next_template_number(category):
    """Get the next template number for a category."""
    category_dir = DOCS_DIR / category

    if not category_dir.exists():
        return 1

    existing = list(category_dir.glob("*.md"))
    existing = [f for f in existing if f.name not in ["index.md", "404.md"]]

    if not existing:
        return 1

    numbers = []
    for f in existing:
        try:
            num = int(f.stem.split("-")[0])
            numbers.append(num)
        except (ValueError, IndexError):
            pass

    return max(numbers) + 1 if numbers else 1


def generate_frontmatter(category, title, template_num):
    """Generate frontmatter for a new template."""
    cat_info = CATEGORIES.get(category, CATEGORIES["strategy"])

    section = cat_info["section"]
    cat = cat_info["category"]
    phase = cat_info["phase"]

    if category in ["legal", "finance", "security"]:
        prefix = {"legal": "L", "finance": "F", "security": "S"}[category]
    else:
        prefix = {"strategy": "I", "recruitment": "II", "enablement": "III"}.get(
            category, "I"
        )

    frontmatter = f"""---
title: {title}
section: {section}
category: {cat}
template_number: {prefix}.{template_num}
version: 1.0.0
last_updated: {datetime.now().strftime("%Y-%m-%d")}
author: PartnerAgents Team

tier:
  - Bronze
  - Silver
  - Gold
skill_level: {DEFAULT_SKILL_LEVEL}
purpose: {DEFAULT_PURPOSE}
phase: {phase}
time_required: 1-2 hours
difficulty: {DEFAULT_DIFFICULTY}
prerequisites: []

description: >
  Brief description of this template's purpose.

purpose_detailed: >
  When and why to use this template.

outcomes:
  - Outcome 1
  - Outcome 2

skills_gained:
  - Skill 1
  - Skill 2
---

## How to Use This Template

**Purpose:**
[Explain what this template is for]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## Template Content

[Add your template content here]

---

## Checklist

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

---

## Related Templates

- [Related Template 1](../category/template-name.md)
- [Related Template 2](../category/template-name.md)
"""
    return frontmatter


def create_template(category, name, title=None):
    """Create a new template file."""
    if category not in CATEGORIES:
        print(f"Error: Unknown category '{category}'")
        print(f"Available categories: {', '.join(CATEGORIES.keys())}")
        return False

    category_dir = DOCS_DIR / category
    category_dir.mkdir(exist_ok=True)

    template_num = get_next_template_number(category)

    filename = f"{template_num:02d}-{name.lower()}.md"
    filepath = category_dir / filename

    if filepath.exists():
        print(f"Error: File already exists: {filepath}")
        return False

    if title is None:
        title = name.replace("-", " ").title()

    content = generate_frontmatter(category, title, template_num)

    with open(filepath, "w") as f:
        f.write(content)

    print(f"Created: {filepath}")
    print(f"Template number: {CATEGORIES[category].get('section', '?')}.{template_num}")
    return True


def interactive_mode():
    """Interactive template creation."""
    print("\n=== PartnerAgents Template Generator ===\n")

    print("Available categories:")
    for i, cat in enumerate(CATEGORIES.keys(), 1):
        print(f"  {i}. {cat}")

    while True:
        try:
            choice = int(input("\nSelect category number: "))
            if 1 <= choice <= len(CATEGORIES):
                category = list(CATEGORIES.keys())[choice - 1]
                break
        except ValueError:
            pass
        print("Invalid choice. Try again.")

    name = input("Template filename (e.g., 'my-template'): ").strip()
    if not name:
        print("Error: Name required")
        return

    name = name.lower().replace(" ", "-")

    title = input("Template title (press Enter for auto): ").strip()

    create_template(category, name, title if title else None)


def main():
    parser = argparse.ArgumentParser(description="Generate new PartnerAgents template")
    parser.add_argument(
        "--category", "-c", choices=list(CATEGORIES.keys()), help="Template category"
    )
    parser.add_argument("--name", "-n", help="Template filename (without .md)")
    parser.add_argument("--title", "-t", help="Template title")
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode"
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.category and args.name:
        create_template(args.category, args.name, args.title)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python scripts/generate_template.py --category legal --name 'nda'")
        print("  python scripts/generate_template.py --interactive")
        print("  python scripts/generate_template.py -c finance -n commission")


if __name__ == "__main__":
    main()
