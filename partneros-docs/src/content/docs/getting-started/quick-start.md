---
title: Quick Start
category: operational
version: 1.1.0
last_updated: 2026-02-22
author: PartnerOS Team
tier: Bronze
skill_level: beginner
purpose: operational
phase: onboarding
time_required: 10 minutes
difficulty: easy
prerequisites: [Web browser]
description: Get up and running with PartnerOS in 10 minutes—no install required.
outcomes: [Browse templates, Understand structure, Launch quickly]
skills_gained: [Platform navigation, Template discovery, Quick start]
keywords: ["quick start", "getting started", "fast", "minutes", "browse"]
---
# PartnerOS Quick Start

*From zero to your first partner in 10 minutes — no install required*

---

## Step 1: Browse Online (2 minutes)

**No install needed.** Just explore at [danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS/)

Browse the template categories:

| What You Need | Start Here |
|--------------|------------|
| Don't know where to start | [Strategy Templates](../strategy/index.mdx) |
| Need to find partners | [Recruitment Templates](../recruitment/index.mdx) |
| Need to train partners | [Enablement Templates](../enablement/index.mdx) |
| Need contracts | [Legal Templates](../legal/index.mdx) |
| Need commission structure | [Finance Templates](../finance/index.mdx) |

---

## Step 2: Pick a Template (5 minutes)

Find the template that fits your need. Each template includes:

- **What it is** - Purpose and use case
- **How to use it** - Step-by-step instructions
- **What to fill in** - Brackets like `[Your Company]` where you add your info
- **Related templates** - Other templates that pair well

### Most Popular Starting Points

For new partner programs:

1. [Ideal Partner Profile](../strategy/02-ideal-partner-profile/) — Who do you want as partners?
2. [Partner Business Case](../strategy/01-partner-business-case/) — Justify the investment
3. [Program Architecture](../strategy/06-program-architecture/) — Design your tiers and benefits

---

## Step 3: Copy & Customize (10 minutes)

### Option A: Copy Directly (Easiest)

1. Open any template
2. Click "Copy" on the code block
3. Paste into your document
4. Replace `[bracketed text]` with your info

### Option B: Use Variables (If You Clone the Repo)

```bash
# See all variables in a template
python scripts/fill_template.py --list-vars

# Fill a template with your company info
python scripts/fill_template.py --template partneros-docs/src/content/docs/recruitment/01-email-sequence.md
```

**Common variables:** `{{company_name}}`, `{{contact_name}}`, `{{contact_email}}`, `{{today_date}}`

---

## Step 4: Optional Full Setup

Want more power? Clone the repo:

```bash
# Clone the repo
git clone https://github.com/danieloleary/PartnerOS.git
cd PartnerOS

# Set up your company info
python scripts/onboard.py

# Run the AI Partner Agent
cd scripts/partner_agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python agent.py --playbook recruit --partner "Acme Corp"
```

---

## Choose Your Path

=== ":globe_with_meridians: Browse Only"

    **Best for:** Just need a few templates, no setup.

    1. Browse [danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS/)
    2. Find templates that fit your needs
    3. Copy and customize

    **Time:** 5 minutes

=== ":computer: Full Setup"

    **Best for:** Want to use the AI agent and automation.

    1. Clone the repo
    2. Run `python scripts/onboard.py`
    3. Use `python scripts/fill_template.py` to fill templates
    4. Run AI agent with `python agent.py`

    **Time:** 30 minutes

=== ":robot: AI Partner Agent"

    **Best for:** Want AI to help execute playbooks.

    ```bash
    cd PartnerOS/scripts/partner_agent
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python agent.py --playbook recruit --partner "Your Partner"
    ```

    **Time:** 15 minutes

---

## What's Next?

### For New Partner Programs

1. [Define your Ideal Partner](../strategy/02-ideal-partner-profile/) — Who do you want?
2. [Build the Business Case](../strategy/01-partner-business-case/) — Why is this worth it?
3. [Design Your Program](../strategy/06-program-architecture/) — Tiers and benefits

### For Signing a Specific Partner

1. [Qualify them](../recruitment/03-qualification-framework/) — Are they a good fit?
2. [Discovery Call](../recruitment/04-discovery-call/) — Learn about them
3. [Send Proposal](../recruitment/07-proposal/) — Make it official

### For Ongoing Management

- [QBR Template](../enablement/07-qbr-template/) — Quarterly reviews
- [Success Metrics](../enablement/06-success-metrics/) — Track performance

---

## Need Help?

- **Questions?** Open an issue on [GitHub](https://github.com/danieloleary/PartnerOS/issues)
- **Want a specific template?** Suggest it on GitHub
- **Found an issue?** Fix it and PR!

---

## Template Structure

Every template follows this pattern:

```markdown
---
title: Template Name
description: What this template is for
---

## How to Use This Template
Step-by-step instructions...

---

# Template Name

## Section 1
[Content with placeholders like [Your Company]]

## Section 2
[More content...]
```

**Tip:** Look for text in `[brackets]` — that's where you add your specific info.
