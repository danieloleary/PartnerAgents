---
title: Partner Agent
keywords: ["ai powered assistant", "running partnership playbooks", "partner lifecycle overview", "new yaml file", "partnership expert helping", "agent programmatically python"]
---
# Partner Agent

An AI-powered assistant for running partnership playbooks and managing the partner lifecycle.

## Overview

The Partner Agent helps partnership teams by:
- **Running Playbooks** - Guided workflows for common partnership scenarios
- **Filling Templates** - AI-assisted completion of partnership documents
- **Tracking Progress** - Monitor partners through lifecycle stages
- **Generating Insights** - Analyze partnership health and recommend actions

## Playbooks

Pre-defined sequences of templates for specific scenarios:

| Playbook | Templates | Use Case |
|----------|-----------|----------|
| `recruit` | IPP → Qualification → Discovery → Pitch → Proposal | Signing a new partner |
| `onboard` | Agreement → Onboarding Checklist → Enablement Roadmap | Activating a signed partner |
| `qbr` | Success Metrics → QBR Template → ICP Tracker | Quarterly partner reviews |
| `expand` | Business Case → Strategy Plan → Co-Marketing | Growing an existing partnership |
| `exit` | Exit Checklist | Gracefully ending a partnership |

## Quick Start

```bash
# Set your API key (supports OpenAI or Anthropic)
export OPENAI_API_KEY=sk-...
# or
export ANTHROPIC_API_KEY=sk-ant-...

# Run the agent interactively
python agent.py

# Run a specific playbook
python agent.py --playbook recruit --partner "Acme Corp"

# Continue from saved state
python agent.py --resume acme-corp-recruit
```

## Usage Examples

### Interactive Mode

```
$ python agent.py

Partner Agent v1.0
==================

What would you like to do?
1. Start a new playbook
2. Continue existing playbook
3. View partner status
4. Generate report

> 1

Available playbooks:
- recruit: New Partner Recruitment
- onboard: Partner Onboarding
- qbr: Quarterly Business Review
- expand: Partner Expansion
- exit: Partner Exit

Select playbook: recruit
Partner name: Acme Corp

Starting 'New Partner Recruitment' playbook for Acme Corp...

Step 1/5: Ideal Partner Profile
-------------------------------
I'll help you evaluate if Acme Corp fits your ideal partner profile.

What industry is Acme Corp in?
> Enterprise Software

What's their primary go-to-market motion?
> Direct sales with some channel

[Agent fills template and saves progress...]

Step 2/5: Partner Qualification Framework
-----------------------------------------
...
```

### Playbook Mode

```bash
# Start recruitment playbook
python agent.py --playbook recruit --partner "Acme Corp"

# Resume where you left off
python agent.py --resume acme-corp-recruit

# Skip to specific step
python agent.py --resume acme-corp-recruit --step 3
```

### Status & Reporting

```bash
# View all active partnerships
python agent.py --status

# Generate QBR prep report
python agent.py --report qbr --partner "Acme Corp"

# Export partnership summary
python agent.py --export --partner "Acme Corp" --format pdf
```

## Configuration

Create `config.yaml` to customize behavior:

```yaml
# AI Provider (openai or anthropic)
provider: anthropic
model: claude-sonnet-4-20250514

# Template paths
templates_dir: ../../docs

# State storage
state_dir: ./state

# Company context (used to pre-fill templates)
company:
  name: "Your Company"
  product: "Your Product"
  value_prop: "What you help customers achieve"

# Default partner tiers
tiers:
  - Strategic
  - Gold
  - Silver
  - Registered
```

## State Management

Partner progress is saved in `./state/{partner-slug}/`:

```
state/
└── acme-corp/
    ├── metadata.json      # Partner info, current stage
    ├── recruit/
    │   ├── progress.json  # Playbook progress
    │   ├── 01_ipp.md      # Filled Ideal Partner Profile
    │   ├── 02_qual.md     # Filled Qualification Framework
    │   └── ...
    └── qbr/
        ├── 2025-Q1/
        └── 2025-Q2/
```

## Architecture

```
partner_agent/
├── agent.py           # Main entry point & CLI
├── config.yaml        # Configuration
├── playbooks/         # Playbook definitions
│   ├── recruit.yaml
│   ├── onboard.yaml
│   ├── qbr.yaml
│   ├── expand.yaml
│   └── exit.yaml
├── core/
│   ├── llm.py         # LLM integration (OpenAI/Anthropic)
│   ├── templates.py   # Template loading & parsing
│   ├── state.py       # State management
│   └── prompts.py     # System prompts
└── state/             # Saved partner states
```

## Extending

### Custom Playbooks

Create a new YAML file in `playbooks/`:

```yaml
name: Partner Renewal
description: Annual partnership renewal process
steps:
  - template: enablement/06-success-metrics.md
    name: Review Metrics
    prompt: |
      Review the partner's performance over the past year.
      Highlight achievements and areas for improvement.

  - template: enablement/07-qbr-template.md
    name: Renewal Discussion
    prompt: |
      Prepare talking points for the renewal conversation.
      Include pricing considerations and new commitments.
```

### Custom Prompts

Override system prompts in `config.yaml`:

```yaml
prompts:
  system: |
    You are a partnership expert helping to fill out templates.
    Be concise and actionable. Ask clarifying questions when needed.

  template_intro: |
    Let's work through the {template_name} together.
    I'll ask you questions and fill in the template as we go.
```

## API Integration

Use the agent programmatically:

```python
from partner_agent import PartnerAgent

agent = PartnerAgent(config_path="config.yaml")

# Start a playbook
session = agent.start_playbook("recruit", partner="Acme Corp")

# Process a step
result = session.process_step(
    user_input="They're in enterprise software, B2B SaaS"
)

# Get current state
state = session.get_state()

# Export filled templates
agent.export(partner="Acme Corp", format="pdf")
```

## Requirements

```
anthropic>=0.18.0
openai>=1.0.0
pyyaml>=6.0
rich>=13.0.0
typer>=0.9.0
docling>=1.0.0
```

## Document Processing (Docling)

PartnerAgents includes Docling integration for parsing partner documents:

```bash
# Install with document processing support
pip install docling

# Parse a PDF to Markdown
python parse_document.py --input partner_contract.pdf --output contract.md

# Parse to JSON for structured data
python parse_document.py --input proposal.docx --output proposal.json --format json
```

**Supported formats:** PDF, DOCX, PPTX, HTML, images

**Use cases:**
- Parse partner contracts/NDAs into editable Markdown
- Extract data from security questionnaires
- Convert proposals to structured JSON
- Process partner-provided documentation

Install:
```bash
pip install -r requirements.txt
```
