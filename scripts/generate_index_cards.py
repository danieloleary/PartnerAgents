#!/usr/bin/env python3
"""Generate index.mdx files for all template categories with Starlight Cards."""

import yaml
import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "partneros-docs" / "src" / "content" / "docs"

# Icon mapping for Starlight
ICON_MAP = {
    "strategy": "rocket",
    "recruitment": "user-add",
    "enablement": "graduation-cap",
    "legal": "scale",
    "finance": "coin",
    "security": "shield",
    "operations": "settings",
    "executive": "briefcase",
    "analysis": "bar-chart",
    "agent": "puzzle",
    "getting-started": "book",
}

# Title and description overrides
CATEGORY_INFO = {
    "getting-started": {
        "title": "Getting Started",
        "description": "Start here! Quick guides to help you get up and running with PartnerAgents.",
    },
    "strategy": {
        "title": "Partner Strategy Templates",
        "description": "Define *why* you need partners and *who* you're looking for.\n\nStrategy templates help you build the foundation for a successful partner program before you start recruiting.",
    },
    "recruitment": {
        "title": "Partner Recruitment Templates",
        "description": "Find, qualify, and sign the right partners.\n\nRecruitment templates guide you from initial outreach through signed agreement.",
    },
    "enablement": {
        "title": "Partner Enablement Templates",
        "description": "Train, certify, and equip your partners for success.\n\nEnablement templates help you scale your partner program through effective training and resources.",
    },
    "legal": {
        "title": "Legal Templates",
        "description": "Protect your business with proper legal agreements.\n\nLegal templates cover NDA, MSA, DPA, and SLA for partner relationships.",
    },
    "finance": {
        "title": "Finance Templates",
        "description": "Design partner compensation and incentive programs.\n\nFinance templates cover commissions, rebates, and revenue sharing models.",
    },
    "security": {
        "title": "Security Templates",
        "description": "Ensure partner security and compliance.\n\nSecurity templates help assess and maintain partner security standards.",
    },
    "operations": {
        "title": "Operations Templates",
        "description": "Streamline day-to-day partner management.\n\nOperations templates cover deal registration, reporting, and portal guides.",
    },
    "executive": {
        "title": "Executive Templates",
        "description": "Board-level partner program updates.\n\nExecutive templates help communicate partner program value to leadership.",
    },
    "analysis": {
        "title": "Analysis Templates",
        "description": "Measure and optimize partner performance.\n\nAnalysis templates provide frameworks for partner health and metrics.",
    },
    "agent": {
        "title": "Partner Agent",
        "description": "AI-powered automation for partner management.\n\nThe Partner Agent uses AI to automate partner workflows and tasks.",
    },
}


def get_templates_for_category(category_dir):
    """Get all template files for a category."""
    category_path = DOCS_DIR / category_dir
    templates = []

    if not category_path.exists():
        return templates

    for f in sorted(category_path.glob("*.md")):
        if f.name == "index.md":
            continue
        content = f.read_text()

        # Extract frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 2:
                try:
                    fm = yaml.safe_load(parts[1])
                    if fm and fm.get("title"):
                        templates.append(
                            {
                                "filename": f.stem + "/",  # folder style
                                "title": fm.get("title", f.stem),
                                "description": fm.get("description", ""),
                                "tier": fm.get("tier", []),
                                "difficulty": fm.get("difficulty", ""),
                                "time_required": fm.get("time_required", ""),
                                "template_number": fm.get("template_number", ""),
                            }
                        )
                except:
                    pass

    return templates


def generate_index_mdx(category):
    """Generate index.mdx for a category."""
    icon = ICON_MAP.get(category, "document")
    info = CATEGORY_INFO.get(category, {"title": category.title(), "description": ""})

    templates = get_templates_for_category(category)

    # Build cards
    cards = []
    for t in templates:
        # Build badge line
        badges = []
        if t.get("tier"):
            tier_str = " · ".join(t["tier"])
            badges.append(f"**{tier_str}**")
        if t.get("difficulty"):
            badges.append(f"**{t['difficulty'].title()}**")
        if t.get("time_required"):
            badges.append(t["time_required"])

        badge_line = " · ".join(badges) if badges else ""

        card = f'''\t<Card title="{t["title"]}" icon="{icon}">
\t\t{t["description"] or "Template for " + t["title"].lower()}
\t\t
\t\t:::tip
\t\t{badge_line}
\t\t:::
\t\t
\t\t**[View Template →]({t["filename"]})**
\t</Card>'''
        cards.append(card)

    # Build the file
    content = f"""---
title: {info["title"].replace("Partner ", "").replace(" Templates", "")} Templates
description: {info["description"].split(chr(10))[0] if info["description"] else ""}
---

import {{ Card, CardGrid }} from '@astrojs/starlight/components';

# {info["title"]}

{info["description"]}

---

<CardGrid stagger>
{chr(10).join(cards)}
</CardGrid>
"""

    return content


def main():
    for category in ICON_MAP.keys():
        category_path = DOCS_DIR / category
        if not category_path.exists():
            print(f"Skipping {category} - directory not found")
            continue

        content = generate_index_mdx(category)
        output_path = category_path / "index.mdx"

        # Check if we should overwrite
        old_index_md = category_path / "index.md"
        if old_index_md.exists():
            old_index_md.unlink()
            print(f"Removed: {old_index_md}")

        output_path.write_text(content)
        print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
