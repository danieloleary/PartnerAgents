---
title: CLAUDE.md — PartnerAgents Codebase Guide
keywords: ["docs must start", "step kpis checklist", "agent py points", "length character set", "main partneros docs", "root linting runs"]
---
# CLAUDE.md — PartnerAgents Codebase Guide

This file provides guidance for AI assistants working in this repository.

## Project Overview

**PartnerAgents** is a complete playbook system for building and scaling strategic partnerships, combining:

- 67 Markdown documentation templates across 9 categories (rendered via **Starlight/Astro**)
- 14 Agent-First Templates (7 skill cards + 7 workflow templates)
- An AI-powered Partner Agent (`scripts/partner_agent/agent.py`) supporting local Ollama, Anthropic, OpenAI, and OpenRouter
- 7 automation playbooks covering the full partner lifecycle
- 14 utility scripts for onboarding, templates, reporting, document parsing, and packaging
- GitHub Actions for doc deployment, markdown linting, releases, and issue management
- **163 tests** (all passing)
- Beautiful Web UI with chat interface, Markdown rendering, and Settings modal

**Requirements:**
- **Python 3.10+** (for union type syntax `type | None`)
- **Node.js 20+** (for Starlight docs build)

**Live site:** https://danieloleary.github.io/PartnerAgents

---

## Repository Structure

```
PartnerAgents/
├── partneros-docs/                  # Starlight/Astro docs site
│   ├── src/content/docs/           # Documentation source (~65 .md/.mdx files)
│   ├── astro.config.mjs            # Starlight configuration
│   └── dist/                       # Built static site
├── docs/                           # Symlink → partneros-docs/src/content/docs
├── scripts/
│   ├── partner_agent/             # AI Partner Agent
│   │   ├── agent.py               # Main agent (~985 lines)
│   │   ├── config.yaml            # Agent configuration
│   │   ├── .env.example           # Environment variable template
│   │   ├── requirements.txt       # Python dependencies
│   │   ├── playbooks/             # 7 YAML playbook definitions
│   │   │   ├── recruit.yaml
│   │   │   ├── onboard.yaml
│   │   │   ├── qbr.yaml
│   │   │   ├── expand.yaml
│   │   │   ├── exit.yaml
│   │   │   ├── co-marketing.yaml
│   │   │   └── support-escalation.yaml
│   │   ├── partner_agent/         # Python package wrapper
│   │   │   └── __init__.py        # Re-exports PartnerAgent from agent.py
│   │   └── state/                 # Partner session state (gitignored)
│   ├── onboard.py                 # Company onboarding setup
│   ├── fill_template.py           # Replace {{variables}} in templates
│   ├── generate_template.py       # CLI template generator
│   ├── generate_report.py         # Partner report generation
│   ├── generate_file_list.py      # Template inventory generator
│   ├── standardize_templates.py   # Bulk frontmatter standardization
│   ├── manage_templates.py        # Template management utilities
│   ├── update_keywords.py         # YAML frontmatter keyword updater
│   ├── lint_markdown.py           # Custom markdown linter
│   ├── demo_mode.py               # Pre-filled demo company data
│   ├── export_pdf.py              # Markdown to PDF conversion
│   ├── parse_document.py         # Docling document parser (PDF, DOCX, PPTX)
│   └── package_zip.py             # Package repo as distributable .zip
├── examples/                      # Example fills and test data
│   ├── complete-examples/         # Fully filled template examples
│   ├── demo-company/              # Fake company data for demos
│   └── test-partner/              # TechStart Inc test case
├── tests/
│   ├── test_templates.py          # Template structure/frontmatter tests (35 tests)
│   ├── test_agent.py              # Agent unit tests (14 tests)
│   ├── test_onboarding.py         # Onboarding flow tests (6 tests)
│   ├── test_deployed_links.py     # Link validation tests (6 tests)
│   └── requirements.txt           # Test dependencies (pytest, pyyaml)
├── .github/workflows/
│   ├── deploy-docs.yml            # Deploys docs to GitHub Pages on push to main
│   ├── markdown_lint.yml          # Runs markdown linter on all *.md changes
│   └── run_partner_agent.yml      # Manual workflow to run a playbook via Actions
├── package.json                   # Node.js: npm run lint:md → python lint script
├── CHANGELOG.md                   # Version history
├── BACKLOG.md                     # Prioritized feature backlog
├── ARCHITECTURE.md                # Architecture decisions and philosophy
├── README.md                      # Project overview
├── Example_Partner_Plan.md        # Sample partner plan document
└── PartnerAgents_Assistant_Agent_Design.md  # Agent architecture design doc
```

---

## Development Commands

### Documentation (Starlight/Astro - PRIMARY)

```bash
# Install docs dependencies
cd partneros-docs
npm install

# Preview locally (hot reload at http://localhost:4321)
npm run dev

# Build static site to dist/
npm run build

# Deploys to https://danieloleary.github.io/PartnerAgents/ on push to main
```

### Partner Agent

```bash
cd scripts/partner_agent

# Install agent dependencies
pip install -r requirements.txt

# Run interactively (default: interactive mode)
python agent.py

# Run specific playbook for a partner
python agent.py --playbook recruit --partner "Acme Corp"

# Resume saved session
python agent.py --resume acme-corp

# Show all partner statuses
python agent.py --status

# Reload config without restart
python agent.py --reload

# Enable debug logging
python agent.py --verbose
```

### Environment Setup (Agent)

```bash
# Local Ollama (free, offline, recommended)
export OLLAMA_ENDPOINT=http://localhost:11434
export OLLAMA_MODEL=llama3.2:3b
export PROVIDER=ollama

# Anthropic (cloud)
export ANTHROPIC_API_KEY=sk-ant-...
export PROVIDER=anthropic

# OpenAI (cloud)
export OPENAI_API_KEY=sk-...
export PROVIDER=openai
```

### Testing

```bash
# Run all tests (recommended)
pytest tests/ -v

# Run only template tests
pytest tests/test_templates.py -v

# Run only agent tests
pytest tests/test_agent.py -v

# Or with Python directly
python3 tests/test_templates.py
python3 tests/test_agent.py
```

### Test Suite (163 tests)

**Template Tests (`test_templates.py` — 61 tests):**

- `test_templates_exist` - At least 1 template exists
- `test_templates_have_frontmatter` - All .md files have YAML frontmatter
- `test_frontmatter_schema_validation` - 17 required fields present
- `test_template_count_per_category` - Correct counts per folder
- `test_folder_structure` - All directories exist
- `test_playbook_template_references` - Playbooks reference existing templates
- `test_frontmatter_yaml_parseable` - No YAML syntax errors
- `test_config_yaml_valid` - config.yaml has required fields
- `test_playbook_yaml_schema` - All playbooks valid schema
- `test_no_duplicate_template_titles` - No duplicate titles
- `test_template_files_have_content` - Templates not empty
- `test_starlight_docs_exist` - Starlight docs directory exists
- `test_scripts_exist` - Utility scripts present
- `test_onboard_script_valid` - onboard.py compiles
- `test_fill_template_script_valid` - fill_template.py compiles
- `test_demo_mode_script_valid` - demo_mode.py compiles
- `test_export_pdf_script_valid` - export_pdf.py compiles
- `test_package_zip_script_valid` - package_zip.py compiles
- `test_package_zip_produces_output` - ZIP packaging works
- `test_examples_directory` - examples/ structure exists
- `test_starlight_index_mdx` - Starlight index.mdx exists
- `test_playbooks_exist` - All 7 playbooks present
- `test_env_example_exists` - .env.example has required vars

**Agent Tests (`test_agent.py` — 14 tests):**

- `test_agent_import` - Agent.py compiles without errors
- `test_partner_sanitization` - Partner name validation works
- `test_path_validation` - Path traversal prevented
- `test_slugify` - URL slug generation works
- Plus 10 agent superpower tests (memory, recommendations, tier guidance, email, reporting)

**Onboarding Tests (`test_onboarding.py` — 6 tests):**

- `test_onboarding_path_document_exists` - First partner path doc exists
- `test_test_partner_directory_exists` - Test partner data exists
- `test_onboarding_templates_have_frontmatter` - Onboarding docs have frontmatter
- `test_getting_started_folder_structure` - Getting started folder valid
- `test_examples_directory_structure` - Examples directory structure valid

### Markdown Linting

```bash
# Via npm (calls Python linter)
npm run lint:md

# Or directly
python3 scripts/lint_markdown.py
```

---

## Key Conventions

### Markdown Templates (docs/)

Every `.md` file in `docs/` **must** start with YAML frontmatter. The standardized schema includes 17 fields:

```yaml
---
title: Template Title
description: Brief description of this template's purpose.
section: Strategy          # Strategy, Recruitment, Enablement, Legal, Finance, Security, Operations, Executive, Analysis
category: strategic        # strategic, operational, tactical, legal, financial, security, executive, analytical
template_number: I.1       # Roman numeral section + number
version: "1.0.0"
author: PartnerAgents Team
last_updated: 2026-02-20
tier: Silver               # Bronze, Silver, Gold
skill_level: intermediate  # beginner, intermediate, advanced
purpose: strategic         # tactical, strategic, operational
phase: recruitment         # recruitment, onboarding, enablement, growth, retention, exit
time_required: "2-3 hours"
difficulty: medium         # easy, medium, hard
prerequisites: []
outcomes: [Expected outcome 1, Expected outcome 2]
skills_gained: [Skill 1, Skill 2]
tags: [strategy, business-case]
---
```

The `test_templates_have_frontmatter` test enforces this — any file missing `---` at the start will fail CI.

### Starlight Formatting Requirements

Templates are rendered using **Astro Starlight**. Follow these rules to avoid 404s and rendering issues:

**Critical Rules:**

1. **Start with paragraphs, NOT headings**
   - Starlight adds H1 from frontmatter automatically
   - Start with 2-3 sentences of intro, then use H2 (`##`)

2. **Folder links MUST have trailing slash**
   - `[Getting Started](getting-started/)` - correct
   - `[Getting Started](getting-started)` - will 404!

3. **Cross-folder links use relative paths**
   - `[Success Metrics](../enablement/06-success-metrics/)` - correct
   - `[Success Metrics](/enablement/06-success-metrics/)` - breaks on deployed site!

4. **Every table needs context**
   - Add paragraph BEFORE table: explain what it shows
   - Add paragraph AFTER table: interpret the data

5. **Use Starlight asides**
   - `:::tip[Insider Tip]` for tips
   - `:::note` for information
   - `:::caution` for warnings

**See also:** [Starlight Formatting Guide](./partneros-docs/src/content/docs/skills/starlight-formatting/)

### Playbook YAML Format

Playbooks in `scripts/partner_agent/playbooks/` follow this schema:

```yaml
name: Human-readable playbook name
description: What this playbook accomplishes
tags: [tag1, tag2]

steps:
  - name: Step Name
    template: docs/recruitment/01-foo.md  # relative to repo root
    prompt: |
      Instruction to the AI for this step.
    # KPIs, checklist, and automation hints as comments

success_criteria:
  - Measurable outcome 1
  - Measurable outcome 2

next_playbook: onboard   # optional — which playbook to run next
```

Template paths in playbooks are relative to the repo root (e.g., `docs/recruitment/01-foo.md`).

### Partner State Storage

Partner state is saved to `scripts/partner_agent/state/<slug>/metadata.json` (gitignored). The slug is derived from `_sanitize_partner_name()` → `slugify()`:

- Alphanumeric, dashes, underscores only
- Max 100 characters
- No path traversal characters (`.`, `/`, `\`)

### Agent Configuration (`config.yaml`)

```yaml
provider: anthropic        # anthropic | openai | ollama | auto
model: sonnet-4-20250514   # model identifier

templates_dir: ../../docs   # relative to agent.py - points to docs/
state_dir: ./state

company:
  name: "[Your Company]"
  product: "[Your Product]"
  value_prop: "[Your Value Proposition]"
  website: "[Your Website]"
```

The `config.yaml` is committed; `.env` is gitignored (use `.env.example` as a starting point).

---

## Architecture: Partner Agent

### Class Structure (`agent.py`)

| Class/Component | Responsibility |
|---|---|
| `PartnerAgent` | Main orchestrator; loads config, LLM, playbooks, templates |
| `OllamaClient` | Local Ollama HTTP client with exponential backoff retry |
| `RetryConfig` | Configures retry behavior (max attempts, delays) |

### LLM Provider Priority

1. If `provider=ollama` or `provider=auto` and Ollama health check passes → use Ollama
2. If `provider=anthropic` → use `anthropic.Anthropic` SDK
3. If `provider=openai` → use `openai.OpenAI` SDK (v1.x syntax)

### Security Considerations

The agent enforces two key security controls:

1. **Path traversal prevention** (`_validate_path`): template and playbook paths are resolved and checked to remain within their base directories
2. **Input sanitization** (`_sanitize_partner_name`): partner names are validated for length, character set, and path traversal sequences

Do not remove or weaken these controls.

### Output Formatting

All agent output goes through `_print()`, `_print_error()`, `_print_success()`, `_print_warning()`. These gracefully degrade when `rich` is not installed.

---

## CI/CD Workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy-docs.yml` | Push to `main` (partneros-docs/** or astro.config.mjs) | Builds Starlight site, deploys to GitHub Pages |
| `markdown_lint.yml` | Push/PR touching `*.md` | Runs `scripts/lint_markdown.py` via `npm run lint:md` |
| `run_partner_agent.yml` | Manual (`workflow_dispatch`) | Runs a specific playbook + partner via GitHub Actions |

### Deploy Docs Requirements

- Node.js 20+
- Python 3.11
- Pushes to `main` only; requires `contents: read`, `pages: write`, `id-token: write` permissions

### Manual Agent Workflow Inputs

- `playbook`: one of recruit / onboard / qbr / expand / exit / co-marketing / support-escalation
- `partner`: partner name string
- `provider`: anthropic / openai / ollama
- Requires `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` secrets in the repository

---

## Markdown Linting Rules

`scripts/lint_markdown.py` enforces:

- No trailing whitespace on any line
- Space after `##` heading hashes (e.g., `## Title` not `##Title`)
- Newline at end of file
- No extraneous shell prompt lines (lines starting with `root@`)

Linting runs on every `*.md` push via `markdown_lint.yml`.

---

## Template Categories (40 templates across 9 categories)

### Strategy Templates (`docs/strategy/`) — 8 templates

| # | Template | Purpose |
|---|---|---|
| I.1 | Partner Business Case | Business justification for a partnership |
| I.2 | Ideal Partner Profile | Define target partner characteristics |
| I.3 | 3C/4C Evaluation Framework | Structured partner scoring |
| I.4 | Competitive Differentiation | Position vs. competitors |
| I.5 | Partner Strategy Plan | Full GTM strategy |
| I.6 | Program Architecture | Bronze/Silver/Gold tier design |
| I.7 | Internal Alignment Playbook | Stakeholder buy-in |
| I.8 | Partner Exit Checklist | Graceful partner offboarding |

### Recruitment Templates (`docs/recruitment/`) — 10 templates

| # | Template | Purpose |
|---|---|---|
| II.1 | Email Sequence | Cold outreach cadence |
| II.2 | Outreach/Engagement Sequence | Multi-touch engagement |
| II.3 | Qualification Framework | Scoring potential partners |
| II.4 | Discovery Call Script | First-call structure |
| II.5 | Partner Pitch Deck | Slide deck outline |
| II.6 | Partnership One-Pager | Executive summary leave-behind |
| II.7 | Proposal Template | Formal partnership proposal |
| II.8 | Agreement Template | Contract structure |
| II.9 | Onboarding Checklist | New partner activation steps |
| II.10 | ICP Alignment Tracker | Ideal customer profile tracking |

### Enablement Templates (`docs/enablement/`) — 7 templates

| # | Template | Purpose |
|---|---|---|
| III.1 | Enablement Roadmap | Training timeline |
| III.2 | Training Deck | Partner training materials |
| III.3 | Certification Program | Partner certification structure |
| III.4 | Co-Marketing Playbook | Joint marketing campaigns |
| III.5 | Technical Integration Guide | Integration documentation |
| III.6 | Partner Success Metrics | KPI tracking framework |
| III.7 | QBR Template | Quarterly business review |

### Legal Templates (`docs/legal/`) — 4 templates

| # | Template | Purpose |
|---|---|---|
| L.1 | Mutual NDA | Non-disclosure agreement |
| L.2 | Master Service Agreement | Service contract framework |
| L.3 | Data Processing Agreement | Data handling and GDPR compliance |
| L.4 | SLA Template | Service level agreement |

### Finance Templates (`docs/finance/`) — 3 templates

| # | Template | Purpose |
|---|---|---|
| F.1 | Commission Structure | Partner commission tiers and payouts |
| F.2 | Rebate Program | Volume-based partner incentives |
| F.3 | Revenue Sharing Model | Joint revenue partnership models |

### Security Templates (`docs/security/`) — 2 templates

| # | Template | Purpose |
|---|---|---|
| S.1 | Security Questionnaire | Partner security assessment |
| S.2 | SOC 2 Compliance Guide | Compliance requirements and checklist |

### Operations Templates (`docs/operations/`) — 4 templates

| # | Template | Purpose |
|---|---|---|
| O.1 | Deal Registration Policy | Rules, eligibility, conflict resolution |
| O.2 | Weekly Partner Standup | Weekly team sync agenda |
| O.3 | Monthly Partner Report | Roll-up metrics and dashboard |
| O.4 | Partner Portal Guide | PRM system setup and usage |

### Executive Templates (`docs/executive/`) — 1 template

| # | Template | Purpose |
|---|---|---|
| X.1 | Board Deck | Quarterly board update on partner program |

### Analysis Templates (`docs/analysis/`) — 1 template

| # | Template | Purpose |
|---|---|---|
| A.1 | Partner Health Scorecard | Quarterly partner assessment and scoring |

---

## Partner Tier Model

The enterprise framework uses three tiers:

| Tier | Revenue Target | Key Benefits |
|---|---|---|
| Bronze (Registered) | < $100K/year | Self-service portal, deal registration, basic materials |
| Silver (Certified) | $100K–$500K/year | Co-marketing, priority leads, dedicated partner manager |
| Gold (Strategic) | $500K+/year | Executive sponsor, joint GTM, custom enablement, QBRs |

QBR frequency by tier: Gold → quarterly, Silver → semi-annually, Bronze → annually.

---

## Adding New Content

### Adding a New Documentation Template

1. Create a `.md` file in the appropriate `partneros-docs/src/content/docs/` subdirectory
2. Add YAML frontmatter at the top (required — CI will fail without it)
3. Starlight automatically includes it in the sidebar via `autogenerate` in `astro.config.mjs`
4. Run `cd partneros-docs && npm run dev` locally to verify rendering

### Adding a New Playbook

1. Create `scripts/partner_agent/playbooks/<name>.yaml`
2. Follow the playbook YAML schema above
3. Add the playbook name to `run_partner_agent.yml` options list
4. Add it to `test_playbooks_exist` in `tests/test_templates.py`
5. Test with: `python agent.py --playbook <name> --partner "Test Partner"`

### Adding a New Source Template

1. Add the `.md` file to the relevant `partneros-docs/src/content/docs/` subdirectory (strategy, recruitment, enablement, legal, finance, security, operations, executive, analysis)
2. Reference it in a playbook step's `template` field if applicable
3. Ensure the file has YAML frontmatter

---

## What Not to Do

- Do not commit `.env` files — use `.env.example` as the template
- Do not commit `scripts/partner_agent/state/` — it contains partner data and is gitignored
- Do not commit to `main` directly — use pull requests
- Do not skip YAML frontmatter in `docs/` Markdown files — CI enforces it
- Do not weaken `_validate_path` or `_sanitize_partner_name` — these prevent path traversal attacks
- Do not use the `site/` directory as a source — it is build output only
