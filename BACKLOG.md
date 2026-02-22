# PartnerOS Backlog - Prioritized Roadmap

*Generated: February 19, 2026*
*Updated: February 21, 2026*
*Based on: ARCHITECTURE.md + Full Audit (Feb 21)*

---

## Vision

**"Give them the playbook + the coach"**

- Templates = The playbook (what to do)
- Agent = The coach (guides them through it)
- You = The advisor (help customize and implement)

**Target:** Companies that can drop in PartnerOS and immediately have a world-class partner program.

---

## Phase 1: Foundation (Drop-Ready) ⚡

*Goal: A company can download and get started in 30 minutes*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 1.1 | **Company Config Script** | `python scripts/onboard.py` - prompts for company info, generates config | 2 hrs | DONE |
| 1.2 | **Template Variable System** | Replace `{{company_name}}` etc with their company | 2 hrs | DONE |
| 1.3 | **Quick Start Guide** | "From zero to first partner in 30 minutes" | 3 hrs | DONE |
| 1.4 | **Example Fills** | 3-5 completed templates showing format | 4 hrs | DONE |

---

## Phase 2: Sales Ready 📦

*Goal: Something to show prospects, easy to demo*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 2.1 | **Demo Mode** | Pre-filled fake company data for demos | 2 hrs | DONE |
| 2.2 | **One-Pager** | Product sheet to give prospects | 1 hr | DONE |
| 2.3 | **Pricing Sheet** | How to license/subscribe | 1 hr | DONE |
| 2.4 | **Testimonials/Case Study Template** | Social proof | 2 hrs | PENDING |

---

## Phase 3: Onboarding Flow 🎯

*Goal: Clear "first partner" path that actually works*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 3.1 | **First Partner Onboarding Path** | Documented sequence: which templates in what order | 3 hrs | DONE |
| 3.2 | **Test Partner Design** | "TechStart Inc" - realistic test case for validation | 2 hrs | DONE |
| 3.3 | **Onboarding Test Cases** | Automated tests simulating partner lifecycle | 4 hrs | DONE |
| 3.4 | **End-to-End Validation** | Run full onboarding flow, fix gaps | 3 hrs | DONE |

---

## Phase 4: Agent Superpowers 🤖

*Goal: The agent becomes a real "coach"*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 4.1 | **Partner Memory** | tier, health_score, notes, milestones persisted per partner | 4 hrs | DONE |
| 4.2 | **Template Recommendations** | `recommend_templates()` suggests next playbooks by stage + tier | 3 hrs | DONE |
| 4.3 | **Tier Guidance** | Tier config (Gold/Silver/Registered) wired into every LLM system prompt | 2 hrs | DONE |
| 4.4 | **Email Generation** | `generate_email()` + interactive menu option 6 | 2 hrs | DONE |
| 4.5 | **Report Generation** | `scripts/generate_report.py` — markdown report for all or one partner | 3 hrs | DONE |

---

## Phase 4b: Template Completion 📋

*Goal: Complete the template library*

| # | Item | Category | Purpose | Effort | Status |
|---|------|----------|---------|--------|--------|
| 4b.1 | Revenue Sharing Model | Finance | Joint venture partnerships | 2 hrs | DONE |
| 4b.2 | Partner Rebate Program | Finance | Volume-based incentives | 2 hrs | DONE |
| 4b.3 | SOC2 Compliance Guide | Security | Compliance requirements | 2 hrs | DONE |
| 4b.4 | Deal Registration Policy | Operations | Rules and eligibility | 2 hrs | DONE |
| 4b.5 | Weekly Partner Standup | Operations | Weekly team sync | 1 hr | DONE |
| 4b.6 | Monthly Partner Report | Operations | Roll-up metrics | 2 hrs | DONE |
| 4b.7 | Partner Portal Guide | Operations | PRM system guide | 2 hrs | DONE |
| 4b.8 | Board Deck - Partner Program | Executive | Quarterly board update | 3 hrs | DONE |
| 4b.9 | Partner Health Scorecard | Analysis | Quarterly assessment | 2 hrs | DONE |

---

## Phase 5: Documentation Refresh 📝

*Goal: All meta-documentation accurately reflects the codebase*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 5.1 | **Full Audit** | Test suite + UI/UX site audit | 2 hrs | DONE |
| 5.2 | **Update IMPROVEMENT_PLAN.md** | Comprehensive findings and roadmap | 1 hr | DONE |
| 5.3 | **Update BACKLOG.md** | Mark completed items, add new findings | 30 min | DONE |
| 5.4 | **Update CLAUDE.md** | Accurate file tree, counts, test list | 1 hr | DONE |
| 5.5 | **Update README.md** | Fix counts, structure, typo | 30 min | DONE |
| 5.6 | **Update CHANGELOG.md** | Add v1.3 entry | 15 min | DONE |
| 5.7 | **Update ARCHITECTURE.md** | Current state, completed features | 30 min | DONE |

---

## Phase 6: Navigation & Index Pages 🧭

*Goal: Every section has a landing page, no orphaned files*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 6.1 | **Create `docs/security/index.md`** | Security section landing page with template grid | 30 min | DONE |
| 6.2 | **Create `docs/operations/index.md`** | Operations section landing page with template grid | 30 min | DONE |
| 6.3 | **Create `docs/executive/index.md`** | Executive section landing page | 20 min | DONE |
| 6.4 | **Create `docs/analysis/index.md`** | Analysis section landing page | 20 min | DONE |
| 6.5 | **Add orphaned files to nav** | Add `first-partner-path.md`, `licensing.md`, `partner-os-one-pager.md` to `mkdocs.yml` | 15 min | DONE |
| 6.6 | **Add nav completeness test** | Verify all docs/ files appear in mkdocs.yml nav | 30 min | DONE |
| 6.7 | **Add index coverage test** | Verify each template dir has index.md | 20 min | DONE |

---

## Phase 7: Test Expansion 🧪

*Goal: Comprehensive test coverage for site integrity*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 7.1 | **Cross-reference test** | Verify internal markdown links between templates resolve | 1 hr | DONE |
| 7.2 | **MkDocs build test** | Run `mkdocs build --strict` in CI to catch broken pages | 30 min | DONE |
| 7.3 | **Playbook dry-run test** | Validate playbook step execution without LLM calls | 1 hr | DONE |
| 7.4 | **Template polish** | Fix frontmatter in 44 templates (prerequisites, skills_gained, descriptions) | 2 hrs | DONE |

---

## Phase 8: Polish & Release 🎁

*Goal: Professional product ready for distribution*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 8.1 | **Template Frontmatter Polish** | Fix 44 templates with missing/empty fields | 2 hrs | DONE |
| 8.2 | **Test Suite Polish** | Enable skipped tests, reach 78+ passing | 1 hr | DONE |
| 8.3 | **Release v1.4** | Final validation, CHANGELOG, tag | 30 min | PENDING |

---

## Completed Items

| Item | Date |
|------|------|
| Version 1.4 Release | Feb 20, 2026 |
| Test Suite Expansion (43 → 80 tests) | Feb 20, 2026 |
| Phase 6 Complete (4 index pages, nav updates) | Feb 20, 2026 |
| Template Frontmatter Polish (44 templates) | Feb 20, 2026 |
| Documentation refresh (CLAUDE.md, README, BACKLOG, CHANGELOG, ARCHITECTURE, IMPROVEMENT_PLAN) | Feb 21, 2026 |
| Full test suite + UI/UX audit | Feb 21, 2026 |
| Partner Memory (tier, health, notes, milestones) | Feb 20, 2026 |
| Tier Guidance in LLM prompts | Feb 20, 2026 |
| Template Recommendations engine | Feb 20, 2026 |
| Email Generation (generate_email + menu) | Feb 20, 2026 |
| Report Generation (scripts/generate_report.py) | Feb 20, 2026 |
| Agent tests expanded (43 total) | Feb 20, 2026 |
| Legal Templates (NDA, MSA, DPA, SLA) | Feb 20, 2026 |
| Finance Templates (Commission, Rebate, Revenue Share) | Feb 20, 2026 |
| Security Templates (Questionnaire, SOC2) | Feb 20, 2026 |
| Operations Templates (Deal Reg, Standup, Report, Portal) | Feb 20, 2026 |
| Executive Template (Board Deck) | Feb 20, 2026 |
| Analysis Template (Health Scorecard) | Feb 20, 2026 |
| Template Generator Script | Feb 20, 2026 |
| Standardize Script | Feb 20, 2026 |
| MkDocs Navigation (9 sections) | Feb 20, 2026 |
| Template Schema Standardization (17-field frontmatter) | Feb 19, 2026 |
| Demo Mode | Feb 19, 2026 |
| One-Pager & Licensing | Feb 19, 2026 |
| Company Onboarding (onboard.py) | Feb 19, 2026 |
| Template Variables (fill_template.py) | Feb 19, 2026 |
| Quick Start Guide | Feb 19, 2026 |
| Example Fills | Feb 19, 2026 |
| Agent v1.1 fixes (security, retry, logging) | Feb 2, 2026 |
| Initial release (7 playbooks, 25 templates, agent) | Jan 2026 |

---

## Quick Reference

### Running Tests

```bash
pytest tests/ -v
```

### Testing Multi-Agent System

```python
from scripts.partner_agents.drivers import DanAgent, ArchitectAgent, etc

agents = {
    'dan': DanAgent(),
    'architect': ArchitectAgent(),
    # ...
}

# Call a skill
result = agents['architect'].call_skill('architect_onboard', {'partner_id': 'Acme', 'tier': 'Gold'})
```

### Generating Template

```bash
python scripts/generate_template.py --category legal --name my-template
```

### Onboarding

```bash
python scripts/onboard.py
```

---

## Multi-Agent Architecture (v2.0)

*Updated: February 21, 2026*

### Team (v2.0 - Role Names)

| Agent | Role | Skills | Templates |
|-------|------|--------|-----------|
| The Owner | Executive | 6 | 6 |
| Partner Manager | Relationships | 6 | 9 |
| Strategy | ICP & Tiers | 5 | 6 |
| Operations | Deals & Comms | 5 | 9 |
| Marketing | Campaigns | 5 | 7 |
| Leader | Board & ROI | 5 | 6 |
| Technical | Integrations | 4 | 4 |

**Total: 7 agents | 36 skills | 47 templates**

### Web UI (v2.1)

*Added: February 21, 2026*

| Feature | Status |
|---------|--------|
| Beautiful dark theme | DONE |
| Responsive design | DONE |
| Chat interface | DONE |
| Quick action buttons | DONE |
| LLM integration (Minimax via OpenRouter) | DONE |
| Hardcoded API key | DONE |
| Fallback mode | DONE (on error) |

**Run:** `python scripts/partner_agents/web.py`

**Access:** http://localhost:8000

**NOTE:** LLM output formatting needs improvement - responses are too verbose/ugly

### Tests

| Test Suite | Status |
|------------|--------|
| test_templates.py (24 tests) | PASSING |
| test_agent.py (14 tests) | PASSING |
| test_onboarding.py (5 tests) | PASSING |
| test_agents.py (13 tests) | PASSING |
| test_agents_comprehensive.py (32 tests) | PASSING |
| test_web.py (3 tests) | PASSING |
| test_web_comprehensive.py (15 tests) | PASSING |

**Total: 144 tests passing**

---

## Next Steps (Priority Order)

| Priority | Item | Description |
|----------|------|-------------|
| P1 | **Real Agent Logic** | Connect agent skills (Engine, etc) to `partner_state.py` |
| P1 | **Web UI Orchestration** | Use `Orchestrator` in `web.py` to dispatch agent skills |
| P1 | **Partner Onboarding Flow** | Full onboarding workflow in UI |
| P2 | **State Unification** | Merge CLI `state/` and Web `partners.json` storage |
| P2 | **UI Markdown Rendering** | Cleanly render LLM responses in Web UI |
| P2 | **Fix LLM Output Formatting** | Make responses cleaner/compact |
| P2 | **More Actions** | Add clickable actions (QBR, ICP, etc) |
| P3 | **Interactive Web Playbooks** | Port CLI playbook engine to Web UI |
| P3 | **Landing Page** | Product-ready page for selling |

---

## Phase 9: Future Enhancements (Proposed) 🚀

*Goal: Advanced features and robust ecosystem integration*

| # | Item | Purpose |
|---|------|---------|
| 9.1 | **Unified State Management** | Consolidate CLI and Web state into a single shared database via `partner_state.py`. |
| 9.2 | **Web UI Markdown Rendering** | Use `marked.js` to properly format agent responses in the browser. |
| 9.3 | **Real Orchestrator Integration** | Use `Orchestrator` and specialized agent drivers in the Web UI. |
| 9.4 | **Interactive Web Playbooks** | Port the step-by-step playbook engine to the Web UI. |
| 9.5 | **Secure API Key Management** | Add a "Settings" modal for local API key storage. |
| 9.6 | **Partner CRM Dashboard** | Enhanced partner view with health, deals, and activity timeline. |
| 9.7 | **Logic-Driven Agent Skills** | Upgrade skills to perform actual state updates and record milestones. |
| 9.8 | **In-Browser Doc Generation** | Integrated template filling and PDF download in the browser. |
| 9.9 | **Decoupled Frontend** | Refactor Web UI into separate Jinja2 templates and static assets. |
| 9.10| **Unified Cross-Platform Tests** | Integration tests for data integrity between CLI and Web. |
| 9.11| **Multi-Partner Filtering** | Add robust search and filtering (Tier/Status/Vertical) to Web UI. |
| 9.12| **Automated Health Scores** | Dynamic calculation based on activity and deal velocity. |
| 9.13| **Playbook Task Deadlines** | Add target dates and "overdue" alerts to steps. |
| 9.14| **Consolidated Activity Feed** | Unified chronological audit trail for every partner. |
| 9.15| **CRM Export Framework** | Salesforce/HubSpot integration and CSV exports. |
| 9.16| **Advanced Onboarding Meta** | Collect more program-specific data for finance/legal auto-fills. |
| 9.17| **Agent Persona Restrictions** | Role-based approval flows for high-stakes actions. |
| 9.18| **Mobile-First UX** | Responsive mobile optimizations and touch-friendly actions. |
| 9.19| **Smart Template Linking** | Agents provide direct links to recommended Markdown templates. |
| 9.20| **Static Partner Portal Gen** | Generate shareable one-pagers or mini-sites for partners. |

---

## Current Mode: Fallback

The system currently runs in **fallback mode** - responses are generated locally rather than via LLM. This is more reliable. LLM can be enabled later with a valid API key.

---

*Backlog managed per ARCHITECTURE.md vision - "Give them the playbook + the coach"*
