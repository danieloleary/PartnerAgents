#!/usr/bin/env python3
"""
Template Schema Standardizer
Applies the new PartnerAgents frontmatter schema to all templates.

Schema fields added:
- category: legal, operational, strategic, tactical, financial
- version: semantic versioning
- tier: [Bronze, Silver, Gold] (which tiers can use this)
- skill_level: beginner, intermediate, advanced
- purpose: tactical, strategic, operational
- phase: recruitment, onboarding, enablement, growth, retention, exit
- time_required: estimated time
- difficulty: easy, medium, hard
- outcomes: list of expected outcomes
- skills_gained: list of skills this template teaches

Usage:
    python scripts/standardize_templates.py [--dry-run] [--verbose]
"""

import os
import re
import yaml
import argparse
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"

SECTION_TO_PHASE = {
    "strategy": "strategy",
    "recruitment": "recruitment",
    "enablement": "enablement",
    "getting-started": "onboarding",
    "resources": "operational",
    "agent": "operational",
    "legal": "recruitment",
    "finance": "operational",
    "security": "recruitment",
}

SECTION_TO_CATEGORY = {
    "strategy": "strategic",
    "recruitment": "operational",
    "enablement": "tactical",
    "getting-started": "operational",
    "resources": "operational",
    "agent": "operational",
    "legal": "legal",
    "finance": "financial",
    "security": "compliance",
}

DEFAULT_TIER = ["Bronze", "Silver", "Gold"]
DEFAULT_SKILL_LEVEL = "intermediate"
DEFAULT_PURPOSE = "operational"
DEFAULT_DIFFICULTY = "medium"


def get_phase_from_section(section):
    return SECTION_TO_PHASE.get(section.lower(), "operational")


def get_category_from_section(section):
    return SECTION_TO_CATEGORY.get(section.lower(), "operational")


def estimate_time_required(section, filename):
    filename_lower = filename.lower()

    if section.lower() == "legal":
        if "nda" in filename_lower or "sla" in filename_lower:
            return "1-2 hours"
        elif "msa" in filename_lower or "dpa" in filename_lower:
            return "4-8 hours"
        return "2-4 hours"

    if section.lower() == "finance":
        if "commission" in filename_lower or "revenue" in filename_lower:
            return "2-4 hours"
        return "1-2 hours"

    if section.lower() == "security":
        if "questionnaire" in filename_lower or "compliance" in filename_lower:
            return "2-4 hours"
        return "1-2 hours"

    if "email" in filename_lower or "sequence" in filename_lower:
        return "1-2 hours"
    elif "agreement" in filename_lower or "contract" in filename_lower:
        return "4-8 hours"
    elif "business-case" in filename_lower or "strategy" in filename_lower:
        return "8-16 hours"
    elif "onboarding" in filename_lower or "roadmap" in filename_lower:
        return "2-4 hours"
    elif "certification" in filename_lower or "training" in filename_lower:
        return "4-8 hours"
    elif "qbr" in filename_lower or "review" in filename_lower:
        return "2-4 hours"
    elif "pitch" in filename_lower or "proposal" in filename_lower:
        return "2-4 hours"
    else:
        return "1-2 hours"


def estimate_difficulty(section, filename):
    filename_lower = filename.lower()

    if section.lower() == "legal":
        return "hard"

    if section.lower() == "finance":
        return "medium"

    if section.lower() == "security":
        return "medium"

    if "business-case" in filename_lower or "strategy" in filename_lower:
        return "hard"
    elif "agreement" in filename_lower or "contract" in filename_lower:
        return "hard"
    elif "technical" in filename_lower or "integration" in filename_lower:
        return "hard"
    elif "certification" in filename_lower:
        return "medium"
    else:
        return "easy"


def parse_frontmatter(content):
    """Extract frontmatter from markdown content."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)

    if match:
        frontmatter_text = match.group(1)
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            body = content[match.end() :]
            return frontmatter, body
        except yaml.YAMLError:
            pass

    return {}, content


def format_frontmatter(frontmatter):
    """Format frontmatter as YAML with proper ordering."""
    ordered_fields = [
        "title",
        "section",
        "category",
        "template_number",
        "version",
        "last_updated",
        "author",
        "tier",
        "skill_level",
        "purpose",
        "phase",
        "time_required",
        "difficulty",
        "prerequisites",
        "description",
        "purpose_detailed",
        "tags",
        "related_templates",
        "outcomes",
        "skills_gained",
    ]

    lines = ["---"]
    for field in ordered_fields:
        if field in frontmatter:
            value = frontmatter[field]
            if isinstance(value, list):
                if all(isinstance(item, str) for item in value):
                    lines.append(f"{field}:")
                    for item in value:
                        lines.append(f"  - {item}")
                else:
                    lines.append(f"{field}: {value}")
            elif value is None:
                continue
            elif isinstance(value, str) and "\n" in value:
                lines.append(f"{field}: |")
                for line in value.split("\n"):
                    lines.append(f"  {line}")
            else:
                lines.append(f"{field}: {value}")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def process_template(filepath, dry_run=False, verbose=False):
    """Process a single template file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    if not isinstance(frontmatter, dict):
        frontmatter = {}

    section = frontmatter.get("section", filepath.parent.name.capitalize())
    filename = filepath.stem

    frontmatter["category"] = frontmatter.get("category") or get_category_from_section(
        section
    )
    frontmatter["phase"] = frontmatter.get("phase") or get_phase_from_section(section)
    frontmatter["tier"] = frontmatter.get("tier") or DEFAULT_TIER
    frontmatter["skill_level"] = frontmatter.get("skill_level") or DEFAULT_SKILL_LEVEL
    frontmatter["purpose"] = frontmatter.get("purpose") or DEFAULT_PURPOSE
    frontmatter["time_required"] = frontmatter.get(
        "time_required"
    ) or estimate_time_required(section, filename)
    frontmatter["difficulty"] = frontmatter.get("difficulty") or estimate_difficulty(
        section, filename
    )

    if "version" not in frontmatter:
        frontmatter["version"] = "1.0.0"

    if "author" not in frontmatter:
        frontmatter["author"] = "PartnerAgents Team"

    if "prerequisites" not in frontmatter:
        frontmatter["prerequisites"] = []

    if "outcomes" not in frontmatter:
        frontmatter["outcomes"] = [f"Completed {frontmatter.get('title', 'template')}"]

    if "skills_gained" not in frontmatter:
        frontmatter["skills_gained"] = []

    if "related_templates" in frontmatter:
        if not frontmatter["related_templates"]:
            del frontmatter["related_templates"]

    new_content = format_frontmatter(frontmatter) + body

    if dry_run:
        if verbose:
            print(f"[DRY RUN] Would update: {filepath}")
        return False
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        if verbose:
            print(f"Updated: {filepath}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Standardize PartnerAgents template frontmatter"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    args = parser.parse_args()

    template_files = list(DOCS_DIR.rglob("*.md"))
    template_files = [
        f for f in template_files if f.name not in ["index.md", "404.md", "tags.md"]
    ]

    print(f"Found {len(template_files)} template files")
    print("[DRY RUN MODE - No files will be modified]\n")

    updated = 0
    for filepath in template_files:
        process_template(filepath, dry_run=args.dry_run, verbose=args.verbose)
        updated += 1

    print(f"\nProcessed {len(template_files)} templates")
    if not args.dry_run:
        print(f"Updated {updated} templates")
    else:
        print(f"Would update {updated} templates")


if __name__ == "__main__":
    main()
