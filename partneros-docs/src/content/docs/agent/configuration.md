---
title: Configuration
category: operational
version: 1.0.0
author: PartnerOS Team
tier:
skill_level: intermediate
purpose: operational
phase: operational
time_required: 1-2 hours
difficulty: easy
prerequisites:
description: Customize the Partner Agent for your organization
outcomes:
skills_gained:
keywords: ["configuration configuration customize", "workflow configuration file", "enterprise partnership consultant", "product value prop", "partner agent", "agent reads"]
---
# Configuration

Customize the Partner Agent to match your company and workflow.

---

## Configuration File

The agent reads from `config.yaml`:

```yaml
# AI Provider: anthropic or openai
provider: anthropic
model: claude-sonnet-4-20250514

# Template library location
templates_dir: ../docs

# State storage for partner progress
state_dir: ./state

# Your company context
company:
  name: "Your Company"
  product: "Your Product"
  value_prop: "Your Value Proposition"
  website: "https://yourcompany.com"

# Partner tier definitions
tiers:
  - name: Strategic
    revenue_threshold: 1000000
  - name: Gold
    revenue_threshold: 500000
  - name: Silver
    revenue_threshold: 100000
  - name: Registered
    revenue_threshold: 0
```

---

## Settings Reference

### AI Provider

| Setting | Options | Default |
|---------|---------|---------|
| `provider` | `anthropic`, `openai` | `anthropic` |
| `model` | Model ID | `claude-sonnet-4-20250514` |

=== "Anthropic"

    ```yaml
    provider: anthropic
    model: claude-sonnet-4-20250514
    ```

    Available models:
    - `claude-sonnet-4-20250514` (recommended)
    - `claude-opus-4-20250514` (more capable, slower)
    - `claude-3-5-haiku-20241022` (faster, cheaper)

=== "OpenAI"

    ```yaml
    provider: openai
    model: gpt-4-turbo-preview
    ```

    Available models:
    - `gpt-4-turbo-preview`
    - `gpt-4`
    - `gpt-3.5-turbo`

---

### Company Context

Pre-fill templates with your company information:

```yaml
company:
  name: "Acme Corp"
  product: "Acme Platform"
  value_prop: "Help businesses automate their workflows"
  website: "https://acme.com"
  industry: "Enterprise Software"
```

The agent uses this to:
- Pre-populate `[Your Company]` placeholders
- Provide context to the AI for better recommendations
- Customize prompts and suggestions

---

### Partner Tiers

Define your partner program tiers:

```yaml
tiers:
  - name: Strategic
    revenue_threshold: 1000000
    certification_required: true
    qbr_frequency: monthly
  - name: Gold
    revenue_threshold: 500000
    certification_required: true
    qbr_frequency: quarterly
  - name: Silver
    revenue_threshold: 100000
    certification_required: false
    qbr_frequency: semi-annually
  - name: Registered
    revenue_threshold: 0
    certification_required: false
    qbr_frequency: annually
```

---

### Custom Prompts

Override the default AI prompts:

```yaml
prompts:
  system: |
    You are a Partnership Expert Agent helping to run playbooks.
    Be concise and actionable. Ask clarifying questions when needed.

    Company context:
    - Name: {company.name}
    - Product: {company.product}

  template_intro: |
    Let's work through the {template_name} together.
    I'll ask you questions and fill in the template.

  step_complete: |
    Great progress! Ready for the next step?
```

---

### Storage

Configure where state is saved:

```yaml
# Local filesystem (default)
state_dir: ./state

# Templates location
templates_dir: ../docs
```

State structure:

```
state/
└── acme-corp/
    ├── metadata.json
    └── recruit/
        ├── progress.json
        └── filled_templates/
```

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API authentication |
| `OPENAI_API_KEY` | OpenAI API authentication |

```bash
export ANTHROPIC_API_KEY=sk-ant-api03-...
```

---

## Example Configurations

### Startup (Fast & Cheap)

```yaml
provider: anthropic
model: claude-3-5-haiku-20241022

company:
  name: "StartupCo"
  product: "Our MVP"

tiers:
  - name: Partner
    revenue_threshold: 0
```

### Enterprise (Full Featured)

```yaml
provider: anthropic
model: claude-sonnet-4-20250514

company:
  name: "Enterprise Corp"
  product: "Enterprise Platform"
  value_prop: "Digital transformation for the Fortune 500"

tiers:
  - name: Global Strategic
    revenue_threshold: 5000000
    certification_required: true
  - name: Strategic
    revenue_threshold: 1000000
    certification_required: true
  - name: Premier
    revenue_threshold: 500000
    certification_required: true
  - name: Select
    revenue_threshold: 100000
    certification_required: false
  - name: Registered
    revenue_threshold: 0
    certification_required: false

prompts:
  system: |
    You are an enterprise partnership consultant with 20 years
    of experience in Fortune 500 partner programs...
```

---

## Validation

Test your configuration:

```bash
python agent.py --status
```

If configured correctly, you'll see:

```
Partner Agent v1.0
==================
Provider: anthropic
Model: claude-sonnet-4-20250514
Company: Your Company

No partners tracked yet.
```
