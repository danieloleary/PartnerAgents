# CLAUDE.md — PartnerAgents Codebase Guide

This file provides guidance for AI assistants working in this repository.

## Project Overview

**PartnerAgents** is a complete playbook system for building and scaling strategic partnerships, combining:

- **85+ Markdown documentation templates** across 15 categories (rendered via **Starlight/Astro**)
- **Multi-agent swarm** (`scripts/partner_agents/`) — 7 specialized AI drivers (DAN, ARCHITECT, STRATEGIST, ENGINE, SPARK, CHAMPION, BUILDER)
- **Legacy single agent** (`scripts/partner_agent/agent.py`) — standalone Ollama/Anthropic/OpenAI agent
- **Web UI** (`scripts/partner_agents/web.py`) — FastAPI chat interface with Obsidian dark theme
- **CLI** (`scripts/partner_agents/cli.py`) — interactive and one-shot terminal interface
- **7 automation playbooks** covering the full partner lifecycle
- **20+ utility scripts** for onboarding, templates, reporting, document parsing, and packaging
- **GitHub Actions** for doc deployment, markdown linting, releases, issue automation, and stale-bot
- **206 tests** across 20 test modules
- **Pre-commit hooks** for pyflakes, black, isort, markdownlint, YAML validation

**Requirements:**
- **Python 3.10+** (for union type syntax `type | None`)
- **Node.js 20+** (for Starlight docs build)

**Live site:** https://danieloleary.github.io/PartnerOS

---

## Repository Structure

```
PartnerAgents/
├── partneros-docs/                  # Starlight/Astro docs site
│   ├── src/content/docs/           # Documentation source (85+ .md/.mdx files)
│   │   ├── strategy/               # 10 templates
│   │   ├── recruitment/            # 10 templates
│   │   ├── enablement/             # 10 templates
│   │   ├── legal/                  # 5 templates
│   │   ├── finance/                # 4 templates
│   │   ├── security/               # 2 templates
│   │   ├── operations/             # 8 templates
│   │   ├── executive/              # 1 template
│   │   ├── analysis/               # 3 templates
│   │   ├── agent/                  # 12 agent docs
│   │   ├── workflows/              # 7 workflow templates
│   │   ├── skills/                 # 4 skill docs
│   │   ├── resources/              # 2 reference docs
│   │   └── getting-started/        # 4 onboarding docs
│   ├── astro.config.mjs            # Starlight configuration
│   └── dist/                       # Built static site (gitignored)
├── docs/                           # Symlink → partneros-docs/src/content/docs
├── scripts/
│   ├── partner_agents/            # Multi-agent swarm (PRIMARY active system)
│   │   ├── __init__.py            # Package exports
│   │   ├── base.py                # BaseAgent, AgentPriority, AgentStatus, AgentSkill
│   │   ├── orchestrator.py        # Orchestrator + RaceStrategy
│   │   ├── chat_orchestrator.py   # Conversation memory + agent coordination
│   │   ├── router.py              # Intent detection + entity extraction
│   │   ├── cli.py                 # Terminal chat interface (interactive + one-shot)
│   │   ├── web.py                 # FastAPI web UI with chat + REST API
│   │   ├── skills.py              # Shared skill handlers (status, email, etc.)
│   │   ├── document_generator.py  # NDA/MSA/DPA generation
│   │   ├── partner_state.py       # Partner state persistence
│   │   ├── state.py               # Telemetry, ProgramMetrics
│   │   ├── messages.py            # TeamRadio/TeamMessage system
│   │   ├── config.py              # TeamConfig (YAML-backed team config)
│   │   ├── partners.json          # Sample partner data
│   │   └── drivers/               # 7 specialized agent drivers
│   │       ├── dan.py             # DAN — The Owner (decisions, approvals)
│   │       ├── architect.py       # ARCHITECT — Partner Program Manager
│   │       ├── strategist.py      # STRATEGIST — ICP, tiers, competitive analysis
│   │       ├── engine.py          # ENGINE — deals, commissions, compliance
│   │       ├── spark.py           # SPARK — campaigns, email, pitch decks
│   │       ├── champion.py        # CHAMPION — board decks, ROI, exec comms
│   │       └── builder.py         # BUILDER — integrations, API docs, support
│   ├── partner_agent/             # Legacy single-agent (standalone)
│   │   ├── agent.py               # Main agent (~1092 lines)
│   │   ├── config.yaml            # Agent configuration
│   │   ├── .env.example           # Environment variable template
│   │   ├── requirements.txt       # Python dependencies
│   │   ├── partner_state.py       # Session state management
│   │   ├── parse_document.py      # Docling document parser (PDF, DOCX, PPTX)
│   │   ├── playbooks/             # 7 YAML playbook definitions
│   │   │   ├── recruit.yaml
│   │   │   ├── onboard.yaml
│   │   │   ├── qbr.yaml
│   │   │   ├── expand.yaml
│   │   │   ├── exit.yaml
│   │   │   ├── co-marketing.yaml
│   │   │   └── support-escalation.yaml
│   │   └── partner_agent/         # Python package wrapper
│   │       └── __init__.py        # Re-exports PartnerAgent from agent.py
│   ├── fastapi/                   # FastAPI test shim (no real FastAPI needed)
│   │   ├── __init__.py            # Lightweight FastAPI mock
│   │   ├── responses.py           # HTMLResponse, JSONResponse mocks
│   │   └── middleware/cors.py     # CORSMiddleware mock
│   ├── uvicorn.py                 # Lightweight uvicorn test shim
│   ├── onboard.py                 # Company onboarding setup
│   ├── fill_template.py           # Replace {{variables}} in templates
│   ├── generate_template.py       # CLI template generator
│   ├── generate_report.py         # Partner report generation
│   ├── generate_file_list.py      # Template inventory generator
│   ├── generate_index_cards.py    # Index card generation
│   ├── generate_pptx.py           # PowerPoint generation
│   ├── standardize_templates.py   # Bulk frontmatter standardization
│   ├── manage_templates.py        # Template management utilities
│   ├── update_keywords.py         # YAML frontmatter keyword updater
│   ├── lint_markdown.py           # Custom markdown linter
│   ├── demo_mode.py               # Pre-filled demo company data
│   ├── export_pdf.py              # Markdown to PDF conversion
│   ├── package_zip.py             # Package repo as distributable .zip
│   ├── fix_links.py               # Fix broken links in a file
│   ├── fix_all_links.py           # Bulk link fixer across all docs
│   ├── add_template_fields.py     # Add missing fields to template frontmatter
│   ├── add_template_metadata.py   # Bulk metadata addition
│   ├── move_metadata_to_footer.py # Restructure template metadata layout
│   └── optimize_template_ux.py    # Template UX optimization
├── examples/                      # Example fills and test data
│   ├── complete-examples/         # Fully filled template examples
│   ├── demo-company/              # Fake company data for demos
│   └── test-partner/              # TechStart Inc test case
├── tests/
│   ├── conftest.py                # Shared fixtures, constants (REPO_ROOT, dirs, field lists)
│   ├── helpers.py                 # Test utility functions
│   ├── test_templates.py          # Template structure/frontmatter tests
│   ├── test_agent.py              # Legacy agent unit tests
│   ├── test_agents_comprehensive.py  # Multi-agent swarm tests (32 tests)
│   ├── test_build.py              # Starlight build verification
│   ├── test_chat_orchestrator.py  # Chat orchestrator tests
│   ├── test_cli.py                # CLI tests (~60 tests)
│   ├── test_content.py            # Content quality tests (headings, placeholders, etc.)
│   ├── test_deployed_links.py     # Built site link validation
│   ├── test_links.py              # Internal link tests
│   ├── test_onboarding.py         # Onboarding flow tests
│   ├── test_roi_calculator.py     # ROI calculation tests
│   ├── test_scripts.py            # Script import/compilation tests
│   ├── test_security_audit.py     # Security audit tests
│   ├── test_sentinel_security.py  # Security sentinel tests
│   ├── test_starlight.py          # Starlight-specific tests
│   ├── test_web_api.py            # Web API tests
│   ├── test_web_comprehensive.py  # Web UI comprehensive tests
│   └── requirements.txt           # Test dependencies (pytest, pyyaml)
├── .github/workflows/
│   ├── deploy-docs.yml            # Deploys docs to GitHub Pages on push to main
│   ├── markdown_lint.yml          # Runs markdown linter on all *.md changes
│   ├── run_partner_agent.yml      # Manual workflow to run a playbook via Actions
│   ├── release.yml                # Manual version bump and release workflow
│   ├── issue-automation.yml       # Auto-closes linked issues when PR merges
│   └── stale-bot.yml              # Closes stale issues (60d) and PRs (30d)
├── .Jules/                        # AI agent configuration (uppercase)
│   ├── config.md                  # Jules config
│   └── palette.md                 # Palette config
├── .jules/                        # AI agent configuration (lowercase)
│   ├── bolt.md                    # Bolt config
│   └── sentinel.md                # Sentinel security config
├── .pre-commit-config.yaml        # Pre-commit hooks (pyflakes, black, isort, markdownlint)
├── pytest.ini                     # Pytest configuration (asyncio_mode=auto)
├── package.json                   # Node.js: npm run lint:md → python lint script
├── CHANGELOG.md                   # Version history
├── BACKLOG.md                     # Prioritized feature backlog
├── ARCHITECTURE.md                # Architecture decisions and philosophy
├── SPRINT_PLAN.md                 # Active sprint plan
├── CHAT-ORCHESTRATOR-STATUS.md    # Chat orchestrator build status
├── TEMPLATE_INVENTORY.md          # Template inventory reference
├── FIXES.md                       # Bug fix tracking
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

# Deploys to https://danieloleary.github.io/PartnerOS/ on push to main
```

### Multi-Agent Web UI (NEW)

```bash
# Start the FastAPI web server
cd scripts/partner_agents
uvicorn web:app --reload

# Or via the shim entry point
python ../../scripts/uvicorn.py
```

**Web API Endpoints:**
- `GET /` — Serve HTML UI (Obsidian dark theme, three-column layout)
- `POST /chat` — Process chat message through agent swarm
- `GET /api/partners` — List all partners
- `POST /api/partners` — Create a partner
- `GET /api/partners/{name}` — Get partner details
- `DELETE /api/partners/{name}` — Delete partner
- `GET /api/memory` — Get conversation memory
- `DELETE /api/memory` — Clear conversation memory

**Rate limit:** 20 requests/minute. API key stored in localStorage.

### Multi-Agent CLI (NEW)

```bash
# Interactive mode
python scripts/partner_agents/cli.py

# One-shot mode
python scripts/partner_agents/cli.py "onboard Acme Corp"
python scripts/partner_agents/cli.py "status of Acme"
python scripts/partner_agents/cli.py "register deal for Acme, $50k"

# Slash commands (Gemini CLI-style)
/help          # Show available commands
/partners      # List all partners
/roi           # Calculate ROI
/models        # Show available models
/status <name> # Partner status
/quit          # Exit
```

**Environment:**
```bash
export OPENROUTER_API_KEY=sk-or-...
export OPENROUTER_MODEL=qwen/qwen3.5-plus-02-15  # default
```

### Legacy Partner Agent

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

### Environment Setup (Legacy Agent)

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

# Run specific test modules
pytest tests/test_templates.py -v
pytest tests/test_agent.py -v
pytest tests/test_agents_comprehensive.py -v
pytest tests/test_cli.py -v
pytest tests/test_content.py -v

# Run tests excluding known-broken modules
pytest tests/ -v --ignore=tests/test_chat_orchestrator.py \
  --ignore=tests/test_security_audit.py \
  --ignore=tests/test_sentinel_security.py \
  --ignore=tests/test_web_api.py
```

**Note:** As of 2026-02-24, five test modules have collection errors:
`test_chat_orchestrator.py`, `test_security_audit.py`, `test_sentinel_security.py`,
`test_templates.py`, and `test_web_api.py`. The remaining 206 tests are collected.

### Markdown Linting

```bash
# Via npm (calls Python linter)
npm run lint:md

# Or directly
python3 scripts/lint_markdown.py
```

### Pre-Commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

Hooks configured: pyflakes, black, isort, check-yaml, end-of-file-fixer,
trailing-whitespace, check-added-large-files, markdownlint, eslint, check-merge-conflict.

---

## Test Suite Overview

**Total collected:** 206 tests across 20 test modules.

| Test Module | Tests | Coverage |
|---|---|---|
| `test_cli.py` | ~60 | CLI behavior, slash commands, partner lifecycle |
| `test_agents_comprehensive.py` | 32 | All 7 agent drivers, orchestrator |
| `test_content.py` | ~14 | Heading hierarchy, code blocks, placeholders |
| `test_links.py` | ~17 | Internal link integrity |
| `test_deployed_links.py` | ~7 | Built-site link validation |
| `test_roi_calculator.py` | 10 | ROI formula, scenarios, edge cases |
| `test_build.py` | 5 | Starlight build, astro config |
| `test_agent.py` | 18 | Legacy agent: sanitization, path validation, state |
| `test_onboarding.py` | 6 | Onboarding path docs, examples structure |
| `test_scripts.py` | ~8 | Script imports and compilation |
| `test_starlight.py` | varies | Starlight-specific rendering |
| `test_web_comprehensive.py` | varies | Web UI integration |

**Key test fixtures** (in `tests/conftest.py`):
- `repo_root` — absolute path to repo root
- `starlight_docs_dir` — path to `partneros-docs/src/content/docs`
- `valid_sections` — list of 11 valid doc sections
- `REQUIRED_FIELDS` — 17 required frontmatter fields

---

## Key Conventions

### Markdown Templates (docs/)

Every `.md` file in `partneros-docs/src/content/docs/` **must** start with YAML frontmatter. The standardized schema includes 17 required fields:

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
phase: recruitment         # recruitment, onboarding, enablement, growth, retention, exit, strategy, operations, analysis
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
   - `[Getting Started](getting-started/)` — correct
   - `[Getting Started](getting-started)` — will 404!

3. **Cross-folder links use relative paths**
   - `[Success Metrics](../enablement/06-success-metrics/)` — correct
   - `[Success Metrics](/enablement/06-success-metrics/)` — breaks on deployed site!

4. **Do NOT include `.md` extension in links**
   - `[My Doc](../strategy/01-business-case/)` — correct
   - `[My Doc](../strategy/01-business-case.md)` — incorrect

5. **Every table needs context**
   - Add paragraph BEFORE table: explain what it shows
   - Add paragraph AFTER table: interpret the data

6. **Use Starlight asides**
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

success_criteria:
  - Measurable outcome 1
  - Measurable outcome 2

next_playbook: onboard   # optional — which playbook to run next
```

Template paths in playbooks are relative to the repo root (e.g., `docs/recruitment/01-foo.md`).

### Partner State Storage

**Legacy agent:** State saved to `scripts/partner_agent/state/<slug>/metadata.json` (gitignored).

**Multi-agent system:** State in `scripts/partner_agents/partners/` (gitignored). Conversation memory in `scripts/partner_agents/partners/.memory/<conv_id>.json`.

The slug is derived from `_sanitize_partner_name()` → `slugify()`:
- Alphanumeric, dashes, underscores only
- Max 100 characters
- No path traversal characters (`.`, `/`, `\`)

### Legacy Agent Configuration (`config.yaml`)

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

## Architecture: Multi-Agent Swarm (`scripts/partner_agents/`)

### Agent Drivers

The swarm uses an F1 racing metaphor. Each driver inherits from `BaseAgent`:

| Driver | Role | Key Skills |
|---|---|---|
| `DanAgent` | The Owner — ultimate authority | decide, approve, escalate |
| `ArchitectAgent` | Partner Program Manager | onboard, qualify, QBR |
| `StrategistAgent` | Partner Strategy | ICP, tier structure, competitive scoring |
| `EngineAgent` | Partner Operations | deal registration, commissions, compliance |
| `SparkAgent` | Partner Marketing | campaigns, email sequences, pitch decks, leads |
| `ChampionAgent` | Partner Leader | board decks, ROI analysis, exec briefs, budget |
| `BuilderAgent` | Partner Technical | integrations, API docs, technical support |

### Class Structure

| Class/Component | Location | Responsibility |
|---|---|---|
| `BaseAgent` | `base.py` | Abstract base; `AgentPriority`, `AgentStatus`, `AgentSkill`, `HandoffRequest` |
| `Orchestrator` | `orchestrator.py` | Routes intents to agents; `RaceStrategy` |
| `ChatOrchestrator` | `chat_orchestrator.py` | Conversation memory + agent swarm coordination |
| `Router` / `Intent` | `router.py` | LLM-based intent detection + keyword fallback |
| `TeamConfig` | `config.py` | YAML-backed team configuration |
| `TeamRadio` | `messages.py` | Inter-agent messaging system |
| `PartnerState` | `partner_state.py` | Partner data persistence |
| `Telemetry` | `state.py` | Program metrics and telemetry |

### Intent Routing

The router detects these intents and routes to appropriate agents:
- `onboard X` → ARCHITECT
- `NDA/MSA/DPA for X` → BUILDER (document generation)
- `campaign for X` → SPARK
- `deal for X, $amount` → ENGINE
- `board deck` / `ROI` → CHAMPION
- `decide` / `approve` / `escalate` → DAN
- fallback → LLM chat via all agents

### Web UI Features

- Three-column Obsidian dark theme (`#09090b`)
- Command Palette (Cmd+K)
- API key stored in localStorage
- Rate limiting: 20 requests/minute
- CORS enabled for development

---

## Architecture: Legacy Partner Agent (`scripts/partner_agent/agent.py`)

### Class Structure

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

**Do not remove or weaken these controls.**

### Output Formatting

All agent output goes through `_print()`, `_print_error()`, `_print_success()`, `_print_warning()`. These gracefully degrade when `rich` is not installed.

---

## CI/CD Workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy-docs.yml` | Push to `main` (any file) | Builds Starlight site, deploys to GitHub Pages |
| `markdown_lint.yml` | Push/PR touching `*.md` | Runs `scripts/lint_markdown.py` via `npm run lint:md` |
| `run_partner_agent.yml` | Manual (`workflow_dispatch`) | Runs a specific playbook + partner via Actions |
| `release.yml` | Manual (`workflow_dispatch`) | Version bump and release creation |
| `issue-automation.yml` | PR merged | Auto-closes issues linked in PR body |
| `stale-bot.yml` | Daily cron | Marks issues stale after 60d, closes after 30d |

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

## Template Categories (85+ templates across 15 categories)

### Strategy (`docs/strategy/`) — 10 templates

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
| I.9 | Partner Charter | Formal program charter |
| I.10 | Channel Conflict Policy | Conflict resolution framework |

### Recruitment (`docs/recruitment/`) — 10 templates

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

### Enablement (`docs/enablement/`) — 10 templates

| # | Template | Purpose |
|---|---|---|
| III.1 | Enablement Roadmap | Training timeline |
| III.2 | Training Deck | Partner training materials |
| III.3 | Certification Program | Partner certification structure |
| III.4 | Co-Marketing Playbook | Joint marketing campaigns |
| III.5 | Technical Integration Guide | Integration documentation |
| III.6 | Partner Success Metrics | KPI tracking framework |
| III.7 | QBR Template | Quarterly business review |
| III.8 | Testimonials & Case Studies | Social proof templates |
| III.9 | Kickoff Deck | Partner kickoff presentation |
| III.10 | Launch Checklist | Partner launch checklist |

### Legal (`docs/legal/`) — 5 templates

| # | Template | Purpose |
|---|---|---|
| L.1 | Mutual NDA | Non-disclosure agreement |
| L.2 | Master Service Agreement | Service contract framework |
| L.3 | Data Processing Agreement | Data handling and GDPR compliance |
| L.4 | SLA Template | Service level agreement |
| L.5 | Referral Agreement | Referral partner contract |

### Finance (`docs/finance/`) — 4 templates

| # | Template | Purpose |
|---|---|---|
| F.1 | Commission Structure | Partner commission tiers and payouts |
| F.2 | Rebate Program | Volume-based partner incentives |
| F.3 | Revenue Sharing Model | Joint revenue partnership models |
| F.4 | Compensation Plan | Full comp plan template |

### Security (`docs/security/`) — 2 templates

| # | Template | Purpose |
|---|---|---|
| S.1 | Security Questionnaire | Partner security assessment |
| S.2 | SOC 2 Compliance Guide | Compliance requirements and checklist |

### Operations (`docs/operations/`) — 8 templates

| # | Template | Purpose |
|---|---|---|
| O.1 | Deal Registration Policy | Rules, eligibility, conflict resolution |
| O.2 | Weekly Partner Standup | Weekly team sync agenda |
| O.3 | Monthly Partner Report | Roll-up metrics and dashboard |
| O.4 | Partner Portal Guide | PRM system setup and usage |
| O.5 | Territory Plan | Geographic/vertical territory planning |
| O.6 | Annual Review | Year-end partner program review |
| O.7 | Support Tiers | Partner support tier definitions |
| O.8 | Co-Sell Playbook | Joint selling motion |

### Executive (`docs/executive/`) — 1 template

| # | Template | Purpose |
|---|---|---|
| X.1 | Board Deck | Quarterly board update on partner program |

### Analysis (`docs/analysis/`) — 3 templates

| # | Template | Purpose |
|---|---|---|
| A.1 | Partner Health Scorecard | Quarterly partner assessment and scoring |
| A.2 | ROI Calculator | Interactive ROI calculation (MDX) |
| A.3 | Analytics Dashboard | Partner program analytics |

### Workflows (`docs/workflows/`) — 7 templates

Agent-first workflow templates for automated execution.

### Skills (`docs/skills/`) — 4 docs

AI skill cards: find-broken-links, glossary-maintenance, template-quality-audit, starlight-formatting.

### Agent Docs (`docs/agent/`) — 12 docs

Architecture, configuration, setup, playbooks, enterprise framework, and 7 persona docs (one per agent driver).

---

## Partner Tier Model

The enterprise framework uses three tiers:

| Tier | Revenue Target | Key Benefits |
|---|---|---|
| Bronze (Registered) | < $100K/year | Self-service portal, deal registration, basic materials |
| Silver (Certified) | $100K–$500K/year | Co-marketing, priority leads, dedicated partner manager |
| Gold (Strategic) | $500K+/year | Executive sponsor, joint GTM, custom enablement, QBRs |

**Commission rates:** Bronze 10%, Silver 15%, Gold 20%.

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

### Adding a New Agent Driver

1. Create `scripts/partner_agents/drivers/<name>.py` inheriting from `BaseAgent`
2. Implement `get_persona()` and register skills in `__init__`
3. Export from `scripts/partner_agents/drivers/__init__.py`
4. Register in the orchestrator's routing logic
5. Add tests to `tests/test_agents_comprehensive.py`

---

## What Not to Do

- Do not commit `.env` files — use `.env.example` as the template
- Do not commit `scripts/partner_agent/state/` or `scripts/partner_agents/partners/` — they contain partner data and are gitignored
- Do not commit to `main` directly — use pull requests
- Do not skip YAML frontmatter in `docs/` Markdown files — CI enforces it
- Do not weaken `_validate_path` or `_sanitize_partner_name` — these prevent path traversal attacks
- Do not use the `dist/` directory as a source — it is build output only
- Do not add `.md` extension to internal doc links — Starlight requires extension-less links
- Do not use absolute paths (`/strategy/...`) for cross-doc links — use relative paths (`../strategy/...`)
