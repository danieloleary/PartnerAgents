---
title: PartnerOS Backlog - Prioritized Roadmap
keywords: ["issues vision give", "advisor help customize", "implement target companies", "show prospects easy", "system currently runs", "fallback mode responses"]
---
# PartnerOS Backlog - Prioritized Roadmap

*Generated: February 19, 2026*
*Updated: February 21, 2026*

---

## Tracking Issues

- **GitHub Issues:** https://github.com/danieloleary/PartnerOS/issues
- **Labels:** `p1`, `p2`, `p3` for priority, `enhancement`, `bug`, `docs`
- **Use issues to track detailed tasks** - link PRs to issues

---

## Vision

**"Give them the playbook + the coach"**

- Templates = The playbook (what to do)
- Agent = The coach (guides them through it)
- You = The advisor (help customize and implement)

**Target:** Companies that can drop in PartnerOS and immediately have a world-class partner program.

---

## Current State (v2.1 - February 22, 2026)

**Platform:** Starlight/Astro (no more MkDocs!)
**Live Site:** https://danieloleary.github.io/PartnerOS/

### What's Built
- 67 templates across 9 categories (A+ quality standard)
- 14 Agent-First Templates (7 skill cards + 7 workflow templates)
- ROI Analysis page (v2.0)
- 9 section index pages with Starlight Cards
- 7 automation playbooks
- 141 automated tests (all passing)
- AI Partner Agent with memory, recommendations, email generation
- Web UI with chat interface
- **Web UI Features:**
  - Settings modal with API key management (localStorage)
  - Markdown rendering (marked.js)
  - Response caching (5 min)
  - Partner CRUD operations
  - Rate limiting
- Security: CORS restricted, input sanitization, rate limiting
- UI/UX: Empty states, error messages, partner deletion, keyboard shortcuts
- Performance: Response caching, inline CSS fallback
- 3 CI/CD workflows + DevOps tools (CODEOWNERS, dependabot, release, stale-bot)

### Test Suite
| Suite | Count | Status |
|-------|-------|--------|
| test_templates.py | 35 | ✅ |
| test_agent.py | 14 | ✅ |
| test_onboarding.py | 6 | ✅ |
| test_agents_comprehensive.py | 44 | ✅ |
| test_web_comprehensive.py | 15 | ✅ |
| test_starlight.py | 14 | ✅ |
| test_build.py | 6 | ✅ |
| test_content.py | 6 | ✅ |
| test_deployed_links.py | 10 | ✅ |
| test_links.py | 5 | ✅ |
| test_links.py | 9 | ✅ |
| test_content.py | 8 | ✅ |
| test_build.py | 7 | ✅ |
| test_deployed_links.py | 6 | ✅ |
| **Total** | **141** | ✅ |

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
| 2.4 | **Testimonials/Case Study Template** | Social proof | 2 hrs | DONE |

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
| 5.2 | **Update BACKLOG.md** | Mark completed items, add new findings | 30 min | DONE |
| 5.3 | **Update CLAUDE.md** | Accurate file tree, counts, test list | 1 hr | DONE |
| 5.4 | **Update README.md** | Fix counts, structure, typo | 30 min | DONE |
| 5.5 | **Update CHANGELOG.md** | Add v1.3 entry | 15 min | DONE |
| 5.6 | **Update ARCHITECTURE.md** | Current state, completed features | 30 min | DONE |

---

## Phase 6: Navigation & Index Pages 🧭

*Goal: Every section has a landing page, no orphaned files*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 6.1 | **Create `partneros-docs/.../security/index.mdx`** | Security section landing page with template grid | 30 min | DONE |
| 6.2 | **Create `partneros-docs/.../operations/index.mdx`** | Operations section landing page with template grid | 30 min | DONE |
| 6.3 | **Create `partneros-docs/.../executive/index.mdx`** | Executive section landing page | 20 min | DONE |
| 6.4 | **Create `partneros-docs/.../analysis/index.mdx`** | Analysis section landing page | 20 min | DONE |
| 6.5 | **Starlight auto-discovery** | Starlight auto-generates nav via `autogenerate` | 15 min | DONE |
| 6.6 | **Add nav completeness test** | Verify Starlight builds successfully | 30 min | DONE |
| 6.7 | **Add index coverage test** | Verify each template dir has index.mdx | 20 min | DONE |

---

## Phase 7: Test Expansion 🧪

*Goal: Comprehensive test coverage for site integrity*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 7.1 | **Cross-reference test** | Verify internal markdown links between templates resolve | 1 hr | DONE |
| 7.2 | **Starlight build test** | Run `npm run build` to verify site compiles | 30 min | DONE |
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
| Documentation refresh (CLAUDE.md, README, BACKLOG, CHANGELOG, ARCHITECTURE) | Feb 21, 2026 |
| Full test suite + UI/UX audit | Feb 21, 2026 |
| Partner Memory (tier, health, notes, milestones) | Feb 20, 2026 |
| Tier Guidance in LLM prompts | Feb 20, 2026 |
| Template Recommendations engine | Feb 20, 2026 |
| Email Generation (generate_email + menu) | Feb 20, 2026 |
| Report Generation (scripts/generate_report.py) | Feb 20, 2026 |
| Agent tests expanded (43 total) | Feb 20, 2026 |
| Legal Templates (NDA, MSA, DPA, SLA) | Feb 20, 2026 |
| Finance Templates (Commission, Rebate, Revenue Share) | Feb 20, 2026 |
| Real Agent Logic (#31) - PartnerState milestone integration | Feb 21, 2026 |
| Testimonials/Case Study Template (III.8) | Feb 21, 2026 |
| Partner Program Glossary (45 terms) | Feb 21, 2026 |
| Template Quality Audit Skill v3 (Starlight rules) | Feb 21, 2026 |
| Starlight Formatting Skill (SK.2) | Feb 21, 2026 |
| Glossary Maintenance Skill (SK.3) | Feb 21, 2026 |
| Link Test Suite Expansion (18 tests) | Feb 21, 2026 |
| 404.md link fixes | Feb 21, 2026 |
| Version 2.0 Release (Agent-First Templates) | Feb 22, 2026 |
| Version 2.1 Release (Web UI Enhancements) | Feb 22, 2026 |
| Web UI Settings Modal (API key + localStorage) | Feb 22, 2026 |
| Web UI Markdown Rendering (marked.js) | Feb 22, 2026 |
| DevOps Tools (CODEOWNERS, dependabot, release, stale-bot) | Feb 22, 2026 |
| 14 Agent-First Templates (7 skill cards + 7 workflows) | Feb 22, 2026 |
| Template Quality Pass - Business Case (I.1) as pilot | Feb 21, 2026 |
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
| test_templates.py (35 tests) | PASSING |
| test_agent.py (14 tests) | PASSING |
| test_onboarding.py (6 tests) | PASSING |
| test_agents_comprehensive.py (40 tests) | PASSING |
| test_web_comprehensive.py (15 tests) | PASSING |
| test_starlight.py (14 tests) | PASSING |
| test_links.py (9 tests) | PASSING |
| test_content.py (8 tests) | PASSING |
| test_build.py (7 tests) | PASSING (3 skipped) |
| test_deployed_links.py (6 tests) | PASSING |

**Total: 163 tests passing**

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

## Current Mode: Fallback

The system currently runs in **fallback mode** - responses are generated locally rather than via LLM. This is more reliable. LLM can be enabled later with a valid API key.

---

## Phase 9: Web UI Enhancements 🖥️

*Goal: Transform the Web UI into a full-featured partner management platform*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 9.1 | **Unified State Management** | Consolidate CLI state (partner_agent/state/) and Web state (partners.json) into single JSON database | 4 hrs | PENDING |
| 9.2 | **Web UI Markdown Rendering** | Integrate marked.js to render AI responses as formatted Markdown (tables, checklists) | 2 hrs | DONE |
| 9.3 | **Real Orchestrator Integration** | Update Web chat to use Orchestrator class and specialized agents (Architect, Strategist, etc.) | 4 hrs | PENDING |
| 9.4 | **Interactive Playbooks in Web** | Port core playbook engine from CLI to Web UI for guided visual workflows | 6 hrs | PENDING |
| 9.5 | **Secure API Key Management** | Add Settings modal for OpenRouter/Anthropic API keys in browser localStorage | 2 hrs | DONE |
| 9.6 | **Partner CRM Dashboard** | Detailed dashboard per partner: tier, health score, deal history, activity timeline | 4 hrs | PENDING |
| 9.7 | **Logic-Driven Agent Skills** | Upgrade agent skills to perform actual state updates and record milestones | 4 hrs | PENDING |
| 9.8 | **In-Browser Document Generation** | Integrate export_pdf.py and template filling in Web UI | 3 hrs | PENDING |
| 9.9 | **Decouple Web Frontend** | Refactor monolithic HTML in web.py into Jinja2 templates + static assets | 4 hrs | PENDING |
| 9.10 | **Cross-Platform Integration Tests** | E2E tests verifying partner data integrity between CLI and Web | 3 hrs | PENDING |

---

## Phase 10: Template Quality Audit 📋

*Goal: Ensure all 40+ templates are consistent, complete, and production-ready*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 10.1 | **Link Audit** | Verify all internal links work across docs/ and partneros-docs/ | 2 hrs | DONE |
| 10.2 | **Frontmatter Consistency** | All templates have required 17 frontmatter fields | 2 hrs | DONE |
| 10.3 | **Metadata Display** | All templates show metadata table (number, version, time, difficulty) | 1 hr | DONE |
| 10.4 | **Content Completeness** | Each template has outcomes, skills_gained, prerequisites | 4 hrs | PENDING |
| 10.5 | **Style Consistency** | All templates follow same formatting conventions | 4 hrs | PENDING |
| 10.6 | **Cross-Reference Audit** | Templates link to related templates appropriately | 2 hrs | PENDING |
| 10.7 | **Legal/Compliance Review** | Legal templates reviewed by counsel | 8 hrs | PENDING |
| 10.8 | **Example Fills** | Add filled examples for each template category | 8 hrs | PENDING |

---

## Version 1.5: Stabilization Release 📦

*Released: February 21, 2026*
*Goal: Stabilize docs, fix links, clean up anchors*

### Changes in v1.5

| # | Item | Status |
|---|------|--------|
| 1 | Migrate from MkDocs to Starlight-only | DONE |
| 2 | Fix relative links (works in local + deployed) | DONE |
| 3 | Add site config for proper URL generation | DONE |
| 4 | Add test_deployed_links.py (6 tests) | DONE |
| 5 | Add CI pre-build link validation | DONE |
| 6 | Remove anchor ID conflicts ({#anchor}) | DONE |
| 7 | Update CLAUDE.md for Starlight | DONE |
| 8 | Clean up trailing whitespace | DONE |

### Test Suite (v1.5)

| Test Suite | Status |
|------------|--------|
| test_templates.py (35 tests) | PASSING |
| test_agent.py (14 tests) | PASSING |
| test_onboarding.py (6 tests) | PASSING |
| test_agents_comprehensive.py (40 tests) | PASSING |
| test_web_comprehensive.py (15 tests) | PASSING |
| test_starlight.py (14 tests) | PASSING |
| test_links.py (9 tests) | PASSING |
| test_content.py (8 tests) | PASSING |
| test_build.py (7 tests) | PASSING (3 skipped) |
| test_deployed_links.py (6 tests) | PASSING |

**Total: 163 tests passing**

---

## Version 1.6: Future 🚀

*Goal: Web UI enhancements and Starlight-powered documentation*

### Starlight Enhancement Ideas

Based on Starlight's built-in components to improve UX:

| # | Feature | Description | Effort |
|---|---------|-------------|--------|
| S1 | **`<Steps>` Component** | Use Starlight's Steps for visual task progression in onboarding | 2 hrs |
| S2 | **`<Badge>` for T-Shirt Sizing** | Add time/difficulty badges to tasks (90 min, Deep Work, Quick Win) | 1 hr |
| S3 | **Interactive Checklists** | Client-side LocalStorage to save checkbox progress | 4 hrs |
| S4 | **`<CardGrid>` Resource Discovery** | Replace inline links with visual card grids for templates | 2 hr |
| S5 | **Enhanced Code Blocks** | Use `title` attribute for AI agent commands | 1 hr |
| S6 | **First Partner Path MDX** | Draft full Week 1 as MDX with all Starlight components | 3 hrs |

### Planned Items

| Priority | Item | Description |
|----------|------|-------------|
| P1 | Real Agent Logic | Connect agent skills to `partner_state.py` |
| P1 | Web UI Orchestration | Use `Orchestrator` in `web.py` to dispatch agent skills |
| P1 | Partner Onboarding Flow | Full onboarding workflow in UI |
| P2 | State Unification | Merge CLI `state/` and Web `partners.json` storage |
| P2 | UI Markdown Rendering | Cleanly render LLM responses in Web UI |
| P2 | Fix LLM Output Formatting | Make responses cleaner/compact |
| P2 | More Actions | Add clickable actions (QBR, ICP, etc) |
| P3 | Interactive Web Playbooks | Port CLI playbook engine to Web UI |
| P3 | Landing Page | Product-ready page for selling |
| P3 | Starlight S1-S6 | Enhance docs with Starlight components |

---

## Expert Assessment Findings (Feb 2026)

*Assessment from Partner Architect, Leader, Designer, and Security perspectives*

### Quick Wins (v1.8)

| # | Item | Purpose | Priority | Effort |
|---|------|---------|----------|--------|
| Q1 | **Customer Success Stories** | Add 2-3 case studies/testimonials to site | p1 | 4 hrs |
| Q2 | **Edit This Page Links** | Add Starlight edit links to every template | p1 | 2 hrs |
| Q3 | **Search Analytics** | Track what users search for to improve content | p2 | 3 hrs |
| Q4 | **Web UI Modernization** | Update chat UI to feel like ChatGPT | p2 | 6 hrs |
| Q5 | **Template Count Fix** | Resolve README 40 vs 41 template mismatch | p1 | 1 hr |
| Q6 | **Interactive ROI Calculator** | Add web-based calculator for business case | p2 | 4 hrs |

### Medium Term (v2.0)

| # | Item | Purpose | Priority | Effort |
|---|------|---------|----------|--------|
| M1 | **Web UI Authentication** | Add login/access control to web interface | p1 | 8 hrs |
| M2 | **Partner API Template** | New template for REST API documentation | p2 | 4 hrs |
| M3 | **Multi-Currency Support** | Update finance templates for international | p2 | 3 hrs |
| M4 | **PRM Setup Guide** | Partner Relationship Management implementation | p2 | 4 hrs |
| M5 | **Visual Diagrams** | Add flowcharts, architecture diagrams to templates | p2 | 6 hrs |
| M6 | **Variable Interpolation** | Interactive form to fill templates online | p2 | 8 hrs |

### Long Term (v2.1+)

| # | Item | Purpose | Priority | Effort |
|---|------|---------|----------|--------|
| L1 | **SOC 2 Type II Compliance** | Security compliance package | p1 | 20 hrs |
| L2 | **SAML/SSO Integration** | Enterprise identity integration | p1 | 12 hrs |
| L3 | **Partner Portal Template** | Full portal with login, dashboards | p1 | 16 hrs |
| L4 | **Marketplace Templates** | AWS, Azure, Salesforce marketplace docs | p2 | 8 hrs |
| L5 | **Multi-Region Support** | International partnership frameworks | p2 | 6 hrs |
| L6 | **Custom Tier Framework** | Beyond Bronze/Silver/Gold | p3 | 4 hrs |

### Security Enhancements

| # | Item | Purpose | Priority | Effort |
|---|------|---------|----------|--------|
| S1 | **Audit Logging** | Track all partner state changes | p1 | 4 hrs |
| S2 | **Data Encryption** | Encrypt partners.json at rest | p1 | 3 hrs |
| S3 | **API Key Management** | Secure handling of LLM keys | p1 | 2 hrs |
| S4 | **Security Scanning** | Add SAST to CI/CD pipeline | p2 | 4 hrs |
| S5 | **GDPR Compliance** | Data privacy documentation | p2 | 4 hrs |

---

## Agent-First Templates & Skill Cards (v2.0)

*Make templates actionable by specific AI agents - "hire" the right team member for each task*

### Agent Skill Cards

| # | Item | Purpose | Priority | Effort |
|---|------|---------|----------|--------|
| A1 | **Create The Owner Skill Card** | Visual card for executive approval skills | p1 | 2 hrs |
| A2 | **Create Partner Manager Skill Card** | Visual card for relationship management skills | p1 | 2 hrs |
| A3 | **Create Partner Marketing Skill Card** | Visual card for campaign/content creation skills | p1 | 2 hrs |
| A4 | **Create Partner Operations Skill Card** | Visual card for comp plans, deal registration | p1 | 2 hrs |
| A5 | **Create Partner Strategy Skill Card** | Visual card for ICP, evaluation, tier design | p1 | 2 hrs |
| A6 | **Create Partner Technical Skill Card** | Visual card for integrations, API docs | p1 | 2 hrs |
| A7 | **Create Partner Leader Skill Card** | Visual card for board decks, ROI, executive comms | p1 | 2 hrs |

### Agent Workflow Templates

| # | Item | Purpose | Priority | Effort |
|---|------|---------|----------|--------|
| W1 | **Partner Manager Onboarding Workflow** | Agent builds complete onboarding plan | p1 | 4 hrs |
| W2 | **Partner Setup Workflow** | Agent configures portal, deals, pricing | p1 | 4 hrs |
| W3 | **Partner Campaign Generator** | Agent creates email sequences, campaigns | p1 | 3 hrs |
| W4 | **Partner Comp Plan Builder** | Agent builds commission structures | p1 | 3 hrs |
| W5 | **Partner Deal Calculator** | Agent calculates commissions, rebates | p1 | 2 hrs |
| W6 | **Partner Pitch Generator** | Agent creates personalized pitches | p1 | 3 hrs |
| W7 | **Partner Health Check** | Agent runs QBR, creates board decks | p1 | 3 hrs |

### AI Prompt Integration

Add "Tell Your Agent To..." section to existing templates:

| # | Item | Purpose | Priority | Effort |
|---|------|---------|----------|--------|
| P1 | **Add Agent Prompts to Strategy Templates** | Action prompts for strategy agents | p2 | 4 hrs |
| P2 | **Add Agent Prompts to Operations Templates** | Action prompts for ops agents | p2 | 4 hrs |
| P3 | **Add Agent Prompts to Finance Templates** | Action prompts for comp calculations | p2 | 2 hrs |
| P4 | **Add Agent Prompts to Enablement Templates** | Action prompts for marketing/content | p2 | 3 hrs |

### Example Agent Prompt Format

```markdown
## Tell Your Agent To...

**Partner Manager:** "Run a QBR for Acme Corp covering Q4 performance, 2025 goals, and expansion opportunities"

**Partner Marketing:** "Write a 5-email welcome sequence for our new Silver partner tier"

**Partner Ops:** "Calculate the commission for a $50K deal with 20% base rate and 1.25x accelerator"
```

---

## Template Quality & Formatting Fixes (v1.9)

### Critical Fixes Found

| # | Issue | Files Affected | Priority | Effort |
|---|-------|----------------|----------|--------|
| Q1 | **:::tip formatting broken** | 17 files | p1 | 1 hr |
| Q2 | **:::caution formatting broken** | 6 files | p1 | 1 hr |
| Q3 | **Link verification** | All templates | p1 | 2 hrs |
| Q4 | **Template consistency audit** | All 53 templates | p2 | 4 hrs |
| Q5 | **Cross-reference verification** | All templates | p2 | 2 hrs |

---

*Backlog managed per ARCHITECTURE.md vision - "Give them the playbook + the coach"*
