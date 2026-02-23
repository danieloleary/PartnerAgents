---
title: PartnerOS
keywords: ["partner program automation", "chat with partner program", "AI partner management", "natural language partner ops", "partner CLI", "partner chat agent"]
---

# PartnerOS — Chat With Your Partner Program

**Tell PartnerOS what you need. Watch it happen.**

[![Deploy Docs](https://github.com/danieloleary/PartnerOS/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/danieloleary/PartnerOS/actions/workflows/deploy-docs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Chat CLI — The Killer Feature

```bash
# One-shot: tell PartnerOS what you need
$ python scripts/partner_agents/cli.py "onboard Acme"
✅ Created partner: Acme Corp (Silver tier)
✅ Generated NDA, MSA, DPA from templates
✅ Created onboarding checklist

$ python scripts/partner_agents/cli.py "register deal for Acme, $50,000"
✅ Deal registered: Acme Corp - $50,000 (90-day protection)

$ python scripts/partner_agents/cli.py "show status for Acme"
📊 Acme Corp Status:
   Tier: Silver | Deals: 3 | Revenue: $125,000 | Health: 85%

# Interactive: chat session with memory
$ python scripts/partner_agents/cli.py
🤖 PartnerOS > email Acme about QBR
📧 Generated QBR invitation email for Acme Corp
   Subject: QBR Schedule - Acme Corp Q4 2025
```

---

## 5 AI Skills Ready to Go

| Skill | Command Example | What It Does |
|-------|-----------------|--------------|
| **status** | `status Acme` | Partner health, deal count, revenue, health score |
| **email** | `email Acme about renewal` | Generates personalized outreach emails |
| **commission** | `commission for Acme Q4` | Calculates payouts, structures deals |
| **qbr** | `qbr for Acme` | Builds quarterly business review deck |
| **roi** | `roi for partner program` | Analyzes partner program ROI & metrics |

---

## The Problem
Building a world-class partner program is hard. Most companies:

- **Start from scratch** — Reinventing the wheel with every new partnership
- **Lack consistency** — No standardized processes for recruitment, onboarding, or enablement
- **Struggle to scale** — Manual workflows that break as partner count grows
- **Miss revenue** — No systematic approach to partner-driven growth

**PartnerOS solves this.**

---

## Why PartnerOS?

| Benefit | Description |
|---------|-------------|
| **Chat CLI** | Natural language commands: `onboard Acme`, `register deal for X, $50k` |
| **5 Ready Skills** | status, email, commission, qbr, roi — all tested and working |
| **Interactive + One-Shot** | Chat sessions or single commands |
| **67 Ready-to-Use Templates** | Strategy (10), recruitment (10), enablement (9), legal (5), finance (4), security (2), operations (8), executive (1), analysis (2) |
| **7 Automation Playbooks** | recruit, onboard, qbr, expand, exit, co-marketing, support-escalation |
| **Enterprise-Ready** | Three-tier partner framework (Bronze/Silver/Gold) with clear progression paths |
| **78 Tests Passing** | Every skill verified — run `pytest tests/test_chat_organizer.py -v` |
| **Beautiful Web UI** | Chat interface at http://localhost:8000 |

---

## The PartnerOS AI Team

PartnerOS includes a multi-agent system with 7 specialized AI agents that collaborate on partner work:

| Agent | Role | Skills | Templates |
|-------|------|--------|-----------|
| **The Owner** | Executive | 6 | 6 |
| **Partner Manager** | Relationships | 6 | 9 |
| **Strategy** | ICP & Tiers | 5 | 6 |
| **Operations** | Deals & Comms | 5 | 9 |
| **Marketing** | Campaigns | 5 | 7 |
| **Leader** | Board & ROI | 5 | 6 |
| **Technical** | Integrations | 4 | 4 |

**Total: 7 agents | 36 skills | 67 templates | 14 agent-first templates**

Each agent has distinct skills and can collaborate with others. The system is company-customizable with drop-in backgrounds.

### Web Interface

Run the beautiful web UI:

```bash
python scripts/partner_agents/web.py
```

Then open http://localhost:8000

```python
from scripts.partner_agents.drivers import ArchitectAgent, EngineAgent, etc

# Instantiate the team
agents = {
    'partner_manager': ArchitectAgent(),
    'operations': EngineAgent(),
    # ...
}

# Call skills
result = agents['partner_manager'].call_skill('architect_onboard', {
    'partner_id': 'Acme',
    'tier': 'Gold'
})
```

---

## Who Is This For?

- **Startup founders** building their first partner program
- **Partner managers** at mid-market companies scaling partnerships
- **Channel directors** at enterprises managing 100+ partners
- **Revenue leaders** looking to unlock partner-driven growth
- **Anyone** building strategic partnerships from scratch

---

## Live Demo

**👉 [danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS)**

Browse the full documentation, explore templates, and see the AI Agent in action.

---

## Quick Start

### Option 1: Try the Chat CLI (Recommended)

```bash
# Clone the repo
git clone https://github.com/danieloleary/PartnerOS.git
cd PartnerOS

# One-shot: tell PartnerOS what you need
python scripts/partner_agents/cli.py "onboard Acme Corp"

# Interactive: start a chat session
python scripts/partner_agents/cli.py
```

### Option 2: Web UI

```bash
# Run the web UI
python scripts/partner_agents/web.py

# Open http://localhost:8000
```

### Option 3: Browse Online

**[danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS)** — Full documentation with all templates.

---

## Playbooks

| Playbook | Steps | Description |
|----------|-------|-------------|
| **recruit** | 5 | Find, qualify, and sign new partners |
| **onboard** | 5 | Activate and enable signed partners |
| **qbr** | 4 | Quarterly business reviews |
| **expand** | 5 | Grow existing partnerships |
| **exit** | 5 | End partnerships gracefully |
| **co-marketing** | 5 | Joint marketing campaigns |
| **support-escalation** | 5 | Handle partner issues |

---

## Enterprise Partner Framework

PartnerOS implements a three-tier partner model:

### Bronze (Registered)
- Self-service enablement portal
- Basic sales materials
- Deal registration
- **Annual Revenue Target:** <$100K

### Silver (Certified)
- Technical certification
- Co-marketing access
- Priority lead distribution
- Dedicated partner manager
- **Annual Revenue Target:** $100K-$500K

### Gold (Strategic)
- Executive sponsorship
- Custom enablement
- Joint GTM planning
- Quarterly business reviews
- **Annual Revenue Target:** $500K+

---

## Project Structure

```
PartnerOS/
├── docs/                      # 40 templates & documentation (single source of truth)
│   ├── strategy/              # Strategy templates (8)
│   ├── recruitment/           # Recruitment templates (10)
│   ├── enablement/            # Enablement templates (7)
│   ├── legal/                 # Legal templates (4) — NDA, MSA, DPA, SLA
│   ├── finance/               # Finance templates (3) — commission, rebate, revenue share
│   ├── security/              # Security templates (2) — questionnaire, SOC2
│   ├── operations/            # Operations templates (4) — deal reg, standup, report, portal
│   ├── executive/             # Executive templates (1) — board deck
│   ├── analysis/              # Analysis templates (1) — health scorecard
│   ├── getting-started/       # Quick start guides
│   ├── resources/             # Glossary, maturity model, licensing, one-pager
│   └── agent/                 # Partner Agent docs
├── scripts/
│   ├── partner_agent/         # AI Partner Agent
│   │   ├── agent.py           # Main agent (Ollama, Anthropic, OpenAI)
│   │   ├── config.yaml        # Agent & company configuration
│   │   ├── playbooks/         # Playbook definitions (7 total)
│   │   └── .env.example       # Environment config
│   ├── onboard.py             # Company onboarding setup
│   ├── fill_template.py       # Template variable replacement
│   ├── generate_template.py   # CLI template generator
│   ├── generate_report.py     # Partner report generation
│   ├── demo_mode.py           # Demo mode with fake data
│   ├── export_pdf.py          # Markdown to PDF conversion
│   └── package_zip.py         # Package as distributable .zip
├── examples/                  # Example fills and test data
│   ├── complete-examples/     # Fully filled template examples
│   ├── demo-company/          # Fake company data for demos
│   └── test-partner/          # TechStart Inc test case
├── tests/                     # 124 automated tests
├── partneros-docs/            # Starlight/Astro docs site
│   ├── src/content/docs/    # Documentation source
│   └── astro.config.mjs    # Starlight configuration
├── BACKLOG.md                 # Prioritized feature backlog
├── ARCHITECTURE.md            # Architecture decisions
└── README.md                  # This file
```

---

## Testing

```bash
# Run all 124 tests
pytest tests/ -v

# Run by test file
pytest tests/test_templates.py -v   # 35 template/structure tests
pytest tests/test_agents_comprehensive.py -v # 40 agent tests
pytest tests/test_web_comprehensive.py -v    # 15 web interface tests
pytest tests/test_starlight.py -v           # 14 Starlight-specific tests
```

---

## Recent Updates

### v1.3 (February 2026)
- Full test suite + UI/UX site audit
- Updated all meta-documentation (CLAUDE.md, README, BACKLOG, CHANGELOG, ARCHITECTURE)
- Identified and documented next steps: 4 missing section index pages, 3 orphaned nav files, test coverage gaps

### v1.2 (February 2026)
- 40 templates across 9 categories (added legal, finance, security, operations, executive, analysis)
- 43 automated tests (up from 20)
- Agent superpowers: partner memory, tier guidance, template recommendations, email generation, report generation
- New scripts: demo_mode.py, export_pdf.py, package_zip.py, generate_report.py
- Examples directory with complete-examples, demo-company, test-partner
- Standardized 17-field frontmatter schema across all templates

### v1.1 (February 2026)
- Fixed incomplete `_continue_playbook_interactive` method
- Added partner name sanitization & path traversal protection
- Added API retry with exponential backoff
- Added structured logging (--verbose flag)
- Added config reload support (--reload flag)

### v1.0 (January 2026)
- 7 automation playbooks
- Local Ollama support (no API keys required)
- Enterprise partner framework (three-tier model)
- Automated testing framework

---

## Contributing

We welcome contributions! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Add** templates to `docs/` with YAML frontmatter
4. **Update** playbooks in `scripts/partner_agent/playbooks/`
5. **Test** your changes (`python3 tests/test_templates.py`)
6. **Commit** your changes (`git commit -m 'Add amazing feature'`)
7. **Push** to the branch (`git push origin feature/amazing-feature`)
8. **Open** a Pull Request

### Adding New Templates

- Add Markdown files to appropriate `docs/` subdirectories
- Include YAML frontmatter with `title`, `description`, and `tags`
- Follow existing template patterns

### Adding New Playbooks

- Define in `scripts/partner_agent/playbooks/`
- Include step definitions, criteria, KPIs, and checklists
- Test with `python3 tests/test_agent.py`

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

## Resources

- **Documentation:** [danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS)
- **GitHub:** [github.com/danieloleary/PartnerOS](https://github.com/danieloleary/PartnerOS)
- **Issues:** Report bugs and feature requests on GitHub
