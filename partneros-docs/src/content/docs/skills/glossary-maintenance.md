---
title: Glossary Maintenance Guide
description: >
section: Skills
category: operational
template_number: SK.3
version: 1.0.0
last_updated: 2026-02-21
author: PartnerOS Team
tier: 
skill_level: intermediate
purpose: operational
phase: operations
time_required: 15-30 minutes
difficulty: easy
prerequisites: 
outcomes: 
skills_gained: 
keywords: ["organized alphabetically find", "generating enough opportunities", "update last updated", "hyphenated words sort", "frontmatter run tests", "link related terms"]
---
> **"A glossary is only as good as its consistency. Every term should have a definition, a 'why it matters,' and a 'how to measure it.'"**
> — Dan O'Leary, PartnerOS

---

## Why Glossary Maintenance Matters

The Partner Program Glossary is the single source of truth for terminology across all PartnerOS templates. Keeping it accurate ensures:

- ✅ Consistent terminology across templates
- ✅ New users understand key concepts
- ✅ Business cases and strategies sound professional
- ✅ No confusion about metrics and KPIs

---

## Adding New Terms

### Step 1: Find the Right Section

The glossary is organized **alphabetically**. Find the letter section where your term belongs:

```
## A
### ACV (Annual Contract Value)

## B
### Bronze Tier

## C
### CAC (Customer Acquisition Cost)
```

### Step 2: Use the Template

Every term follows this structure:

```markdown
### Term Name (Abbreviation)

Full definition of the term.

**Why it matters:** [Explain business impact]

**How to measure:** [Formula or method]
```

### Step 3: Example - Adding a New Term

**Adding "Pipeline Coverage":**

```markdown
### Pipeline Coverage
The ratio of total partner pipeline value to revenue quota.

**Why it matters:** Indicates whether partners are generating enough
opportunities to meet revenue targets. Below 3x is a warning sign.

**How to measure:** Total partner pipeline value ÷ Sales quota
```

---

## Term Structure Requirements

Each term MUST have:

| Field | Required | Description |
|-------|----------|-------------|
| Term Name | ✅ | The term and abbreviation |
| Definition | ✅ | Clear, concise explanation |
| Why it matters | ✅ | Business impact |
| How to measure | ✅ | Formula or method |

### What NOT to Do

❌ Don't add terms without "why it matters"
❌ Don't add terms without "how to measure"
❌ Don't skip alphabetical order
❌ Don't use vague definitions like "relates to partners"

---

## Updating Existing Terms

When updating a term:

1. **Keep the abbreviation** - many templates reference it
2. **Update "last_updated"** in frontmatter
3. **Don't break links** - if renaming, add redirect note
4. **Test after updating** - run link tests

---

## Alphabetical Order Rules

The glossary MUST be in alphabetical order by letter, then by term:

```
## A
### ACV
### ACR
### ARR

## B
### Bronze Tier

## C
### CAC
### Channel Conflict
### Churn Rate
```

**Rules:**
- Numbers come before letters (e.g., "2B" comes before "A")
- Hyphenated words: sort by first word
- Abbreviations: sort by first letter

---

## Running Tests

### Link Tests

```bash
# Run link validation tests
python3 -m pytest tests/test_links.py -v

# Run all tests
python3 -m pytest tests/ -v
```

### What Tests Catch

| Test | What It Catches |
|------|----------------|
| `test_folder_links_have_trailing_slash` | Missing `/` on folder links |
| `test_links_point_to_existing_files` | Broken internal links |
| `test_no_broken_relative_links` | Invalid `../` links |
| `test_external_links_safe` | Non-HTTPS links |

### Build Test

```bash
cd partneros-docs
npm run build
```

This catches:
- YAML frontmatter errors
- Broken internal references
- Missing assets

---

## Glossary Integrity Checklist

Before submitting changes, verify:

- [ ] Term is in correct alphabetical position
- [ ] Definition is clear and concise
- [ ] "Why it matters" explains business impact
- [ ] "How to measure" provides actionable method
- [ ] No broken links to other templates
- [ ] All tests pass: `pytest tests/test_links.py -v`
- [ ] Build succeeds: `cd partneros-docs && npm run build`

---

## Common Tasks

### Task: Add a New Metric

1. Find appropriate letter section
2. Add term with definition, why it matters, how to measure
3. Update templates that use this metric to reference it
4. Run tests

### Task: Update a Definition

1. Edit the term section
2. Update "last_updated" in frontmatter
3. Run tests to ensure nothing broke

### Task: Add Cross-References

To link related terms in the glossary:

```markdown
**Related terms:**
- TAM (Total Addressable Market)
- SAM (Serviceable Addressable Market)
- SOM (Serviceable Obtainable Market)
```

For cross-references to other templates, use relative links:
```markdown
- [Partner Business Case Template](../strategy/01-partner-business-case/)
```

---

## Related Resources

- [Partner Program Glossary](../resources/glossary/)
- [Starlight Formatting Guide](./starlight-formatting/)
- [Template Quality Audit](./template-quality-audit/)
- [Find and Fix Broken Links](./find-broken-links/)
