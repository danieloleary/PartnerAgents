---
title: PartnerAgents Architecture
keywords: ["own create new", "specific playbooks train", "clone run locally", "scaling strategic partnerships", "key templates option", "company training how"]
---
# PartnerAgents Architecture
*Last Updated: February 24, 2026*

---

## Core Philosophy

**"Give them the playbook + the coach"**

- **Templates** = The playbook (what to do)
- **Agent** = The coach (guides them through it)
- **You** = The advisor (help customize and implement)

PartnerAgents is designed to be dropped into any company and immediately provide a world-class partner program - templates, processes, and AI guidance.

---

## Target Use Cases

1. **Internal Use** - Your company manages partners using PartnerAgents
2. **Sell to Others** - Companies license/use PartnerAgents for their partner programs
3. **Hybrid** - Use internally AND sell to select partners

**Target Companies:** All sizes (SMB to Enterprise)
**Target Partners:** Mixed (Reseller, Referral, SI, ISV)

---

## Directory Structure

```
PartnerAgents/
├── partneros-docs/                # Starlight/Astro docs site (PRIMARY)
│   ├── src/content/docs/         # 85+ templates across 15 categories
│   │   ├── strategy/             # 10 templates
│   │   ├── recruitment/          # 10 templates
│   │   ├── enablement/           # 10 templates
│   │   ├── legal/                # 5 templates
│   │   ├── finance/              # 4 templates
│   │   ├── security/             # 2 templates
│   │   ├── operations/           # 8 templates
│   │   ├── executive/            # 1 template
│   │   ├── analysis/             # 3 templates
│   │   ├── agent/                # 12 agent docs
│   │   ├── workflows/            # 7 workflow templates
│   │   ├── skills/               # 4 skill docs
│   │   ├── resources/            # 2 reference docs
│   │   └── getting-started/      # 4 onboarding docs
│   └── astro.config.mjs          # Starlight configuration
├── docs/                         # Symlink → partneros-docs/src/content/docs
├── scripts/
│   ├── partner_agents/           # Multi-agent swarm (ACTIVE — v2.x)
│   │   ├── drivers/              # 7 specialized agents (DAN, ARCHITECT, etc.)
│   │   ├── orchestrator.py       # Intent routing + RaceStrategy
│   │   ├── chat_orchestrator.py  # Conversation memory
│   │   ├── router.py             # LLM-based intent detection
│   │   ├── document_generator.py # NDA/MSA/DPA generation (the right pattern)
│   │   ├── web.py                # FastAPI web UI
│   │   └── cli.py                # Terminal interface
│   ├── partner_agent/            # Legacy single-agent (v1.x — LEGACY)
│   │   ├── agent.py              # Main agent (~1092 lines)
│   │   ├── config.yaml           # Agent configuration
│   │   └── playbooks/            # 7 YAML playbook definitions (not connected to swarm)
│   ├── fastapi/                  # Lightweight FastAPI shim for testing
│   └── [20+ utility scripts]     # fill_template.py, generate_report.py, etc.
├── examples/                     # Example fills (what good looks like)
│   ├── complete-examples/
│   ├── demo-company/
│   └── test-partner/             # TechStart Inc test case
├── tests/                        # 206 collected tests across 20 modules
└── README.md
```

---

## Two Active Systems (Known Tension)

As of Feb 2026, there are two parallel agent systems with incompatible state and LLM backends:

| | Legacy (`partner_agent/`) | Swarm (`partner_agents/`) |
|---|---|---|
| Status | Stable, feature-complete | Active development |
| LLM | Anthropic / OpenAI / Ollama | OpenRouter |
| State | `state/<slug>/metadata.json` | `partners/<name>.json` |
| Playbooks | Connected (7 YAML playbooks) | **Not connected** |
| Templates | Used as LLM prompts | Mostly unused |
| Interface | CLI (`--playbook`, `--partner`) | Chat CLI + Web UI |

**The critical gap:** The YAML playbooks — the best domain model — are wired only to the legacy agent. The swarm doesn't run playbooks. This means the better architecture (swarm) is disconnected from the better domain model (playbooks).

**The path forward:** Connect swarm orchestration to the YAML playbook engine, and unify state storage. See `BACKLOG.md` items 9.1 and P3 (Interactive Web Playbooks).

**The `document_generator.py` pattern is the right model** — it generates real, filled documents (NDA/MSA/DPA) rather than template strings. This should be extended to all 85 templates.

---

## What's Fixed (By PartnerAgents)

These elements are owned by PartnerAgents and should not be modified by using companies:

| Item | Description |
|------|-------------|
| Template Schema | 17-field frontmatter structure |
| Agent Playbooks | 7 core playbooks (recruit, onboard, QBR, etc.) |
| Best Practices | Proven processes and frameworks |
| Agent Instructions | How the AI guides users |
| Test Suite | 43 automated quality tests |

---

## What's Customizable (By Them)

| Item | Description | How |
|------|-------------|-----|
| Company Name | Their company in templates | `.company-config` or variables |
| Logo/Branding | Their logo in templates | Replace in assets/ |
| Colors | Theme colors | `customize.yaml` |
| Specific Language | Industry terms | Edit templates directly |
| Custom Templates | Add their own | Create new in docs/ |
| Agent Behavior | Custom prompts | Modify playbooks/ |

---

## Company Onboarding Flow

### Option 1: Quick Start (5 minutes)
1. Download .zip or clone repo
2. Edit `.company-config/customize.yaml` (name, logo, colors)
3. Browse templates → Copy what you need

### Option 2: Full Setup (30 minutes)
1. Run: `python scripts/onboard.py`
2. Interactive prompts for company info
3. Auto-generates config files
4. Walkthrough of key templates

### Option 3: With Advisor (You)
1. You help customize
2. Set up their specific playbooks
3. Train their team

---

## Template Variable System

Templates use variables that auto-replace with company info:

```
{{company_name}}      → "Acme Corp"
{{company_website}}   → "acmecorp.com"
{{contact_name}}     → "John Smith"
{{contact_email}}     → "john@acmecorp.com"
{{logo_url}}         → "/assets/logo.png"
```

**Usage:**
```bash
# Generate filled template
python scripts/fill_template.py --template docs/recruitment/01-email-sequence.md
```

---

## Agent Capabilities

### Current Features
- Load and explain any template
- Guide through playbook steps
- Answer partnership questions
- Generate custom content

### Completed Features (v1.2)
- **Partner Memory** - Tier, health_score, notes, milestones persisted per partner
- **Template Recommendations** - `recommend_templates()` suggests next playbooks by stage + tier
- **Tier-Based Guidance** - Tier config (Gold/Silver/Bronze) wired into every LLM system prompt
- **Email Generation** - `generate_email()` + interactive menu option
- **Report Generation** - `scripts/generate_report.py` for markdown partner reports

---

## Deployment Options

### Phase 1: Self-Hosted (Current)
- Download .zip or clone
- Run locally with Python
- Use Ollama for local AI

### Phase 2: Container (Future)
- Docker container for easy deploy
- One-command startup

### Phase 3: Cloud (Future)
- SaaS option for companies who don't want self-host

---

## Extension Points

### Adding Custom Templates
1. Create `.md` file in appropriate `docs/` subfolder
2. Add required frontmatter (17 fields)
3. Agent automatically can use it

### Custom Playbooks
1. Create `.yaml` in `scripts/partner_agent/playbooks/`
2. Define steps referencing templates
3. Agent can run custom playbooks

### Custom Integrations (Future)
- CRM webhooks
- Slack notifications
- Calendar scheduling

---

## Quality Assurance

### Test Suite (206 collected tests across 20 modules)
- CLI behavior, slash commands, partner lifecycle (~60 tests)
- Multi-agent swarm — all 7 drivers, orchestrator (32 tests)
- Content quality — headings, placeholders, code blocks (~14 tests)
- Internal link integrity (~17 tests)
- Built-site link validation (~7 tests)
- ROI formula and edge cases (10 tests)
- Legacy agent: sanitization, path validation, state (18 tests)
- Starlight build verification (5 tests)
- Script imports and compilation (~8 tests)

**Note (Feb 24, 2026):** Five modules fail to collect:
`test_chat_orchestrator.py`, `test_security_audit.py`, `test_sentinel_security.py`,
`test_templates.py`, `test_web_api.py`. See `BACKLOG.md` items T.1–T.6.

### CI/CD
- Tests run on every push
- Markdown linting
- Auto-deploy to GitHub Pages

---

## Licensing & Distribution

### Base Product (This Repo)
- Open source (MIT)
- Use freely

### Commercial Offerings
- **Template Packs** - Additional vertical-specific templates
- **Implementation** - Time spent customizing for their company
- **Training** - How to use PartnerAgents effectively
- **Support** - Ongoing advisor access

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/danieloleary/PartnerAgents.git
cd PartnerAgents

# Quick start
python scripts/onboard.py

# Or just browse docs/
# Start with docs/getting-started/quick-start.md
```

---

## Roadmap

See [BACKLOG.md](BACKLOG.md) for prioritized feature list.

---

*PartnerAgents - The complete playbook for building and scaling strategic partnerships.*
