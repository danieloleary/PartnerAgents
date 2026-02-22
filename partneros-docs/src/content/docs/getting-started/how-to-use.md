---
title: How to Use Templates
category: operational
version: 1.0.0
author: PartnerOS Team
tier: 
skill_level: intermediate
purpose: operational
phase: onboarding
time_required: 1-2 hours
difficulty: easy
prerequisites: 
description: Tips for customizing templates for your organization
outcomes: 
skills_gained: 
keywords: ["information placeholder what", "startup pitch differs", "enterprise pitch keep", "first main content", "one workflow integration", "branding correct dates"]
---
# How to Use Templates

Every template in PartnerOS is designed to be customized for your specific situation. Here's how to get the most out of them.

---

## Understanding Placeholders

Templates use placeholders that you'll replace with your information:

| Placeholder | What to Replace With |
|-------------|---------------------|
| `[Your Company]` | Your company name |
| `[Partner Name]` | The partner's company name |
| `[Product]` | Your product or solution name |
| `$X` or `$[Amount]` | Specific dollar amounts |
| `[Date]` | Relevant dates |
| `[Name]` | Person's name |
| `[X]%` | Percentage values |

!!! example "Before & After"

    **Before:**
    ```markdown
    [Your Company] and [Partner Name] will collaborate to achieve $[X]
    in joint revenue by [Date].
    ```

    **After:**
    ```markdown
    Acme Corp and TechPartners Inc will collaborate to achieve $500,000
    in joint revenue by Q4 2025.
    ```

---

## Customization Levels

### Level 1: Quick Fill

Just replace the placeholders and use as-is.

**Best for:** Urgent needs, testing templates, small deals

### Level 2: Adapt Sections

Keep the structure but modify sections for your context:

- Remove sections that don't apply
- Add company-specific sections
- Adjust language to match your brand voice

**Best for:** Most use cases

### Level 3: Deep Customization

Use the template as inspiration to build your own:

- Reorganize the structure
- Add your frameworks and methodologies
- Integrate with your existing documents

**Best for:** Mature programs with established processes

---

## Best Practices

### :material-check-circle: Do

- **Read the "How to Use" section** at the top of each template
- **Customize for your audience** - A startup pitch differs from an enterprise pitch
- **Keep it concise** - Remove sections you don't need
- **Use your brand voice** - Adjust the tone to match your company
- **Version control** - Keep your customized templates in Git

### :material-close-circle: Don't

- **Don't use verbatim** - Templates are starting points, not final documents
- **Don't over-engineer** - Start simple, iterate based on feedback
- **Don't skip sections blindly** - Understand why each section exists before removing
- **Don't forget to update** - Revisit templates quarterly

---

## Template Sections Explained

Most templates follow this structure:

### YAML Frontmatter

```yaml
---
title: Template Name
description: What this template does
keywords: [search, terms]
---
```

Used for search and organization. You can remove this in your customized version.

### How to Use This Template

Step-by-step instructions specific to the template. Read this first!

### Main Content

The actual template with sections, tables, and placeholders.

### Related Templates

Links to templates that complement this one.

---

## Workflow Integration

### With Google Docs

1. Copy template content
2. Paste into a new Google Doc
3. Use **Find & Replace** (Ctrl/Cmd + H) for placeholders
4. Share with your team

### With Notion

1. Create a new page
2. Paste template content (Notion converts markdown automatically)
3. Create a template database for reuse

### With Partner Agent

```bash
# Let AI help fill templates
python agent.py --playbook recruit --partner "Acme Corp"
```

The agent guides you through each template with intelligent prompts.

---

## Template Quality Checklist

Before using a customized template, verify:

- [ ] All placeholders replaced
- [ ] Company names and branding correct
- [ ] Dates and numbers accurate
- [ ] Removed irrelevant sections
- [ ] Tone matches your brand
- [ ] Links and references updated
- [ ] Reviewed by a colleague

---

## Getting Help

- **Questions about templates?** Open a [GitHub Issue](https://github.com/danieloleary/PartnerOS/issues)
- **Want to contribute?** See the contribution guidelines
- **Need custom templates?** Fork the repo and build your own!
