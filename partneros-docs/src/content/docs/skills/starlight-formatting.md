---
title: Starlight Formatting Guide
description: >
section: Skills
category: operational
template_number: SK.2
version: 1.0.0
last_updated: 2026-02-21
author: PartnerOS Team
tier:
skill_level: intermediate
purpose: operational
phase: operations
time_required: 30 minutes
difficulty: easy
prerequisites:
outcomes:
skills_gained:
keywords: ["starlight formatting guide", "standard markdown following", "frontmatter title start", "important information caution", "roi when presenting", "email note md"]
---
> **"The difference between a template that looks amateur and one that looks professional is in the formatting details."**
> — Dan O'Leary, PartnerOS

---

## Why Starlight Formatting Matters

Starlight has specific requirements that differ from standard Markdown. Following these rules ensures:

- ✅ Links work both locally and on deployed site
- ✅ Tables render correctly with context
- ✅ Navigation (TOC) is clean and usable
- ✅ No broken links or 404 errors

---

## Critical Rules

### 1. Start with Paragraphs, NOT Headings

Starlight automatically adds an H1 from the frontmatter title. Start your page with 2-3 sentences of intro, then use H2 (`##`) for sections.

**WRONG:**
```markdown
---
title: My Page
---

# Main Heading

Content here...
```

**RIGHT:**
```markdown
---
title: My Page
---

This is the intro paragraph that explains what this page is about.

## Section One

Content for section one...

## Section Two

Content for section two...
```

---

### 2. Each Major Section Needs Context

Tables should NEVER stand alone. Always add:

1. **BEFORE the table**: Explain what the table shows and why it matters
2. **AFTER the table**: Interpret the data, explain what the numbers mean

**WRONG (AI slop):**
```
| Metric | Value |
|--------|-------|
| TAM | $48B |
```

**RIGHT (Expert):**
```
Here's what each market level means:
- TAM is the ceiling—the total market opportunity
- SAM is what you can reach with your go-to-market
- SOM is what you can realistically capture

| Level | Definition | Amount |
|-------|------------|--------|
| TAM | Total Addressable Market | $48B |
| SAM | Serviceable Addressable Market | $12B |

This means your realistic opportunity is $180M (1.5% of SAM).
```

---

### 3. Use Starlight Asides for Callouts

Starlight supports custom asides for important information:

```markdown
:::tip[Custom Title]
Your insider tip here
:::

:::note
For important information
:::

:::caution
For warnings
:::

:::danger
For critical warnings
:::
```

**Example:**
:::tip
Always start with the ROI when presenting to CFOs.
:::

---

### 4. Glossary Cross-References

When using industry terms, reference the Partner Program Glossary:

**WRONG:**
```
The TAM is $48B.
```

**RIGHT:**
```
The TAM (Total Addressable Market) is $48B.

See the [Partner Program Glossary](../resources/glossary/) for definitions.
```

**Note:** Don't link to individual anchor terms like `(#tam)` - these break. Just use plain text for terms and link to the glossary page.

---

## Link Format Rules

### Same Folder Links
```markdown
[Email Sequence](01-email-sequence/)
```
Points to `01-email-note.md` in the same folder.

### Cross-Folder Links (Relative)
```markdown
[Success Metrics](../enablement/06-success-metrics/)
```
Goes up one level (`..`), then into `enablement/`.

### Folder Links (Must Have Trailing Slash!)
```markdown
[Getting Started](getting-started/)
```
⚠️ **CRITICAL:** Always add trailing `/` - without it, the link will 404 on the deployed site!

### Common Mistakes to Fix

| Wrong | Correct |
|-------|---------|
| `(01-template.md)` | `(01-template/)` |
| `(../folder/01-template.md)` | `(../folder/01-template/)` |
| `(folder)` | `(folder/)` |

Avoid absolute paths like `/absolute/path` - use relative paths instead.

---

## Heading Hierarchy

Starlight expects this structure:

```markdown
---
title: My Page Title
---

Intro paragraph goes here...

## Section 1 (H2)
### Subsection (H3)

## Section 2 (H2)
### Subsection (H3)
```

- **H1** comes from frontmatter title - don't add manually
- **H2** (`##`) appears in the table of contents
- **H3** (`###`) appears in TOC for long pages

---

## Testing Your Template

### Run Link Tests

```bash
# Test only link tests
python3 -m pytest tests/test_links.py -v

# Test folder links specifically
python3 -m pytest tests/test_links.py::TestLinkRobustness::test_folder_links_have_trailing_slash -v

# Run ALL tests
python3 -m pytest tests/ -v
```

### Preview Locally

```bash
cd partneros-docs
npm run dev
```

Navigate to the page and verify:
- [ ] Links work correctly
- [ ] Tables have context paragraphs
- [ ] Asides render properly
- [ ] No console errors

---

## Common AI Slop Patterns to Avoid

| Bad Pattern | Why It's Bad | Fix |
|-------------|--------------|-----|
| Tables without context | Confusing, no interpretation | Add paragraph before AND after |
| Headings without intro | Cluttered TOC | Start with paragraph |
| Placeholder brackets `[ ]` | Looks unfinished | Use real examples |
| Generic examples | Not actionable | Use specific company names |
| Missing trailing slashes | Causes 404s | Always add `/` at end |
| Absolute `/` links | Breaks on deployed site | Use relative `../` links |

---

## Quick Checklist

Before submitting a template, verify:

- [ ] Page starts with paragraph (not heading)
- [ ] Every table has context before AND after
- [ ] Folder links end with `/`
- [ ] Cross-folder links use `../folder/`
- [ ] No absolute `/` links
- [ ] Starlight asides used for tips/notes/warnings
- [ ] Terms referenced consistently (plain text, not broken anchor links)
- [ ] All tests pass: `pytest tests/test_links.py -v`

---

## Related Resources

- [Template Quality Audit Skill](./template-quality-audit/)
- [Find and Fix Broken Links Skill](./find-broken-links/)
- [Partner Program Glossary](../resources/glossary/)
