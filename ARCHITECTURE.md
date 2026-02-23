---
title: PartnerOS Architecture
keywords: ["own create new", "specific playbooks train", "clone run locally", "scaling strategic partnerships", "key templates option", "company training how"]
---
# PartnerOS Architecture
*Last Updated: February 21, 2026*

---

## Core Philosophy

**"Give them the playbook + the coach"**

- **Templates** = The playbook (what to do)
- **Agent** = The coach (guides them through it)
- **You** = The advisor (help customize and implement)

PartnerOS is designed to be dropped into any company and immediately provide a world-class partner program - templates, processes, and AI guidance.

---

## Target Use Cases

1. **Internal Use** - Your company manages partners using PartnerOS
2. **Sell to Others** - Companies license/use PartnerOS for their partner programs
3. **Hybrid** - Use internally AND sell to select partners

**Target Companies:** All sizes (SMB to Enterprise)
**Target Partners:** Mixed (Reseller, Referral, SI, ISV)

---

## Directory Structure

```
PartnerOS/
├── docs/                          # Templates (the core product) — 47 templates, 72 .md files
│   ├── strategy/                  # Strategy templates (8) + index
│   ├── recruitment/               # Recruitment templates (10) + index
│   ├── enablement/                # Enablement templates (7) + index
│   ├── legal/                     # Legal templates (4) + index
│   ├── finance/                   # Finance templates (3) + index
│   ├── security/                  # Security templates (2) + index
│   ├── operations/                # Operations templates (4) + index
│   ├── executive/                 # Executive templates (1) + index
│   ├── analysis/                  # Analysis templates (1) + index
│   ├── getting-started/           # Onboarding docs (4)
│   ├── agent/                     # Agent docs (5) + index
│   └── resources/                 # Reference docs (4)
├── examples/                      # Example fills (what good looks like)
│   ├── complete-examples/         # Fully filled templates
│   ├── demo-company/              # Fake company data for demos
│   └── test-partner/              # TechStart Inc test case
├── scripts/
│   ├── partner_agent/             # The AI agent
│   │   ├── agent.py               # Main agent (~985 lines)
│   │   ├── config.yaml            # Agent configuration
│   │   └── playbooks/             # 7 playbook definitions
│   ├── onboard.py                 # Company onboarding script
│   ├── fill_template.py           # Template variable replacement
│   ├── generate_template.py       # Create new templates
│   ├── generate_report.py         # Partner report generation
│   ├── standardize_templates.py   # Fix frontmatter
│   ├── demo_mode.py               # Demo mode with fake data
│   ├── export_pdf.py              # Markdown to PDF conversion
│   └── package_zip.py             # Package as distributable .zip
├── .company-config/               # Company customization (gitignored)
│   └── customize.yaml             # Their company name, logo, colors
├── tests/                         # Quality gates (163 tests)
├── partneros-docs/                  # Starlight/Astro docs site
│   ├── src/content/docs/           # Documentation source
│   └── astro.config.mjs           # Starlight configuration
└── README.md                      # Entry point
```

---

## What's Fixed (By PartnerOS)

These elements are owned by PartnerOS and should not be modified by using companies:

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

### Test Suite (144 tests)
- Template structure and frontmatter validation (63 tests)
- Multi-agent skill and driver tests (32 tests)
- Web interface and fallback tests (18 tests)
- CLI agent unit tests (14 tests)
- Onboarding and lifecycle tests (11 tests)
- Playbook schema and references
- Script compilation checks

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
- **Training** - How to use PartnerOS effectively
- **Support** - Ongoing advisor access

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/danieloleary/PartnerAgents.git
cd PartnerOS

# Quick start
python scripts/onboard.py

# Or just browse docs/
# Start with docs/getting-started/quick-start.md
```

---

## Roadmap

See [BACKLOG.md](BACKLOG.md) for prioritized feature list.

---

*PartnerOS - The complete playbook for building and scaling strategic partnerships.*
