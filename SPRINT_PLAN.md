---
title: PartnerAgents Tonight Sprint Plan - v1.8
keywords: ["catch issues early", "prospects", "page"]
---
# PartnerAgents Tonight Sprint Plan - v1.8

## Date: February 21-22, 2026

## GOAL: 41 Templates → 53 Templates + Perfect Quality

---

## Phase 1: PRE-SPRINT (15 min)

### 1.1 Version Updates
- [ ] CHANGELOG.md: Update to v1.8
- [ ] README.md: Fix template count (53), update stats

### 1.2 Issue Cleanup
- [ ] Close #40 - Template rewrite complete
- [ ] Close #39 - Security audit done  
- [ ] Merge #31 → #32 - Real Agent → Web UI
- [ ] Re-rank issues #47-50

---

## Phase 2: 12 NEW GOLDEN TEMPLATES

### Batch 1: HIGHEST VALUE (T1-T4)

#### T1: Partner ROI Calculator (Analysis)
- Purpose: Interactive tool for prospects to calculate partner program ROI
- Location: partneros-docs/src/content/docs/analysis/02-roi-calculator.md
- Content: Formula, inputs, outputs, examples

#### T2: Partner Program Charter (Strategy)
- Purpose: Executive founding document establishing program
- Location: partneros-docs/src/content/docs/strategy/09-partner-charter.md
- Content: Mission, vision, goals, governance

#### T3: Partner Kickoff Deck (Enablement)
- Purpose: Day 1 partner meeting template
- Location: partneros-docs/src/content/docs/enablement/09-kickoff-deck.md
- Content: Agenda, introductions, expectations

#### T4: Partner Territory Plan (Operations)
- Purpose: Geographic/segment assignments
- Location: partneros-docs/src/content/docs/operations/05-territory-plan.md
- Content: Regions, segments, coverage

### Batch 2: OPERATIONS FOCUS (T5-T8)

#### T5: Partner Business Review (Operations)
- Purpose: Annual partner meeting template
- Location: partneros-docs/src/content/docs/operations/06-annual-review.md
- Content: Year review, achievements, plans

#### T6: Partner Support Tiers (Operations)
- Purpose: Support escalation matrix
- Location: partneros-docs/src/content/docs/operations/07-support-tiers.md
- Content: Tier definitions, SLAs, contacts

#### T7: Partner Launch Checklist (Enablement)
- Purpose: Go-live verification
- Location: partneros-docs/src/content/docs/enablement/10-launch-checklist.md
- Content: Pre-launch, launch day, post-launch

#### T8: Co-Sell Playbook (Operations)
- Purpose: Joint selling process
- Location: partneros-docs/src/content/docs/operations/08-cosell-playbook.md
- Content: Process, roles, tools

### Batch 3: FINANCE & LEGAL (T9-T12)

#### T9: Partner Comp Plan (Finance)
- Purpose: Detailed commission matrix
- Location: partneros-docs/src/content/docs/finance/04-comp-plan.md
- Content: Tiers, rates, accelerators

#### T10: Channel Conflict Playbook (Strategy)
- Purpose: Sales/partner coexistence
- Location: partneros-docs/src/content/docs/strategy/09-channel-conflict.md
- Content: Rules, escalation, resolution

#### T11: Partner SLA Template (Legal)
- Purpose: Service level agreement
- Location: partneros-docs/src/content/docs/legal/05-sla.md
- Content: SLAs, remedies, reporting

#### T12: Partner Analytics Dashboard (Analysis)
- Purpose: Metrics & KPIs
- Location: partneros-docs/src/content/docs/analysis/02-analytics-dashboard.md
- Content: Metrics, visualizations, reports

---

## Phase 3: ENHANCEMENTS

- [ ] E1: Link ROI Calculator in Business Case template
- [ ] E2: Add commission spreadsheet to Commission Structure
- [ ] E3: Add fillable PDF links to Legal templates
- [ ] E4: Add "Edit This Page" to all templates (check astro.config.mjs)

---

## Phase 4: TESTING & DEBUG

- [ ] Run all tests: pytest tests/ -v
- [ ] Run link tests
- [ ] Run build: npm run build
- [ ] Verify all 53 templates exist
- [ ] Verify all links work

---

## Phase 5: GITHUB & DEPLOY

- [ ] Create GitHub issues for future work
- [ ] Commit all changes
- [ ] Push to main
- [ ] Verify deployment

---

## SUCCESS CRITERIA

| Metric | Before | After |
|--------|--------|-------|
| Template Count | 41 | 53 |
| Test Count | 141 | 141+ |
| Version | 1.7 | 1.8 |
| GitHub Issues | 20 | 15 |

---

## NOTES

- Use A+ quality standard: expert voice, Starlight formatting, progressive levels
- Every template needs: YAML frontmatter, :::tip/:::note/:::caution, Quick Win → Full Implementation
- Test after every batch to catch issues early
