---
title: Find and Fix Broken Links
section: Skills
category: operational
template_number: SK.1
version: 1.0.0
last_updated: 2026-02-21
author: PartnerOS Team
tier:
skill_level: intermediate
purpose: operational
phase: operations
time_required: 15-30 minutes
difficulty: easy
prerequisites: []
outcomes:
skills_gained:
description: How to find and fix broken internal links in PartnerOS documentation.
keywords: ["starlight documentation when", "fixed pages", "md file", "skill use", "use", "find"]
---
> **Find and fix broken internal links in Starlight documentation.**

## When to Use This Skill

Use this skill when:
- Users report 404 errors on documentation pages
- Running tests and seeing broken link failures
- After migrating content from other documentation systems
- Regular documentation maintenance

---

## Quick Start

### 1. Find Broken Links

Run the built-in test:

```bash
cd PartnerOS
python3 -m pytest tests/test_templates.py::test_no_broken_internal_links -v
```

### 2. Manual Link Audit

Search for common broken link patterns:

```bash
# Find links with .md extension (should use folder style)
grep -r "\]\(.*\.md" partneros-docs/src/content/docs/

# Find double parentheses
grep -r "\(\(" partneros-docs/src/content/docs/

# Find broken cross-folder references
grep -r "I_Partner_Strategy" partneros-docs/src/content/docs/
```

### 3. Auto-Fix Common Patterns

Run the link fixing script:

```bash
cd PartnerOS
python3 scripts/fix_all_links.py
```

---

## Link Format Rules

### Starlight (Current)

| Type | Format | Example |
|------|--------|---------|
| Same folder | `template-name/` | `[Email Sequence](01-email-sequence/)` |
| Cross folder | `../folder/template/` | `[Success Metrics](../enablement/06-success-metrics/)` |
| Index page | folder name only | `[Recruitment](recruitment/)` |

### Common Mistakes to Fix

| Wrong | Correct |
|-------|---------|
| `(01-template/)` | `(01-template/)` |
| `(../folder/01-template.md/)` | `(../folder/01-template/)` |
| `((link))` | `(link)` |

---

## Testing Your Fixes

### Run Link Tests

```bash
# Test only broken links
python3 -m pytest tests/test_templates.py::test_no_broken_internal_links -v

# Test all template tests
python3 -m pytest tests/test_templates.py -v
```

### Preview Locally

```bash
cd partneros-docs
npm run dev
```

Navigate to the fixed pages to verify.

---

## Common Fixes Script

Create `scripts/fix_all_links.py` with:

```python
#!/usr/bin/env python3
"""Fix all internal links for Starlight compatibility."""

import re
from pathlib import Path

DOCS_DIR = Path("partneros-docs/src/content/docs")

def fix_links(content):
    # Remove .md from links
    content = re.sub(r'\.md\/\)', '/)', content)
    return content

for md_file in DOCS_DIR.rglob("*.md"):
    content = md_file.read_text()
    new_content = fix_links(content)
    if new_content != content:
        md_file.write_text(new_content)
        print(f"Fixed: {md_file.name}")
```

---

## Metadata

| | |
|---|---|
| **Template #** | SK.1 |
| **Version** | 1.0.0 |
| **Time** | 15-30 minutes |
| **Difficulty** | Easy |

