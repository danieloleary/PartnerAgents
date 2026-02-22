---
title: Playbooks
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
description: Detailed guide to each Partner Agent playbook
outcomes:
skills_gained:
keywords: ["playbooks playbooks playbooks", "pre defined workflows", "mermaid graph lr", "creating yaml files", "more customization options", "newly signed partner"]
---
# Playbooks

Playbooks are pre-defined workflows that guide you through common partnership scenarios.

---

## Overview

| Playbook | Templates | Use Case |
|----------|-----------|----------|
| `recruit` | 5 | Sign a new partner |
| `onboard` | 5 | Activate a signed partner |
| `qbr` | 4 | Quarterly business review |
| `expand` | 5 | Grow an existing partnership |
| `exit` | 4 | End a partnership gracefully |

## Playbook Flow Visualization

```mermaid
graph LR
    recruit[recruit<br/>Sign Partner] --> onboard[onboard<br/>Activate]
    onboard --> qbr[QBR<br/>Review]
    qbr --> expand[expand<br/>Grow]
    qbr --> exit[exit<br/>Terminate]

    style recruit fill:#e3f2fd
    style onboard fill:#e8f5e9
    style qbr fill:#fff3e0
    style expand fill:#f3e5f5
    style exit fill:#ffebee
```

---

## Recruit

**Purpose:** Take a partner prospect from qualification through signed agreement.

<div class="playbook-flow">
  <span class="playbook-step">Ideal Partner Profile</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Qualification</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Discovery</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Pitch</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Proposal</span>
</div>

### Steps

| Step | Template | What Happens |
|------|----------|--------------|
| 1 | [Ideal Partner Profile](../../strategy/02-ideal-partner-profile/) | Evaluate if partner matches your IPP |
| 2 | [Qualification Framework](../../recruitment/03-qualification-framework/) | Score partner on fit criteria |
| 3 | [Discovery Call Script](../../recruitment/04-discovery-call/) | Prepare qualification call |
| 4 | [Pitch Deck](../../recruitment/05-pitch-deck/) | Customize your pitch |
| 5 | [Proposal Template](../../recruitment/07-proposal/) | Draft the partnership proposal |

```mermaid
graph LR
    A[IPP] --> B[Qualification]
    B --> C[Discovery]
    C --> D[Pitch]
    D --> E[Proposal]
    E --> F((Signed))

    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style F fill:#c8e6c9
```

### Run It

```bash
python agent.py --playbook recruit --partner "Acme Corp"
```

### Success Criteria

- [ ] Partner matches IPP
- [ ] Qualification score > threshold
- [ ] Discovery call completed
- [ ] Pitch delivered
- [ ] Proposal sent

---

## Onboard

**Purpose:** Activate a newly signed partner with training and first wins.

<div class="playbook-flow">
  <span class="playbook-step">Agreement</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Checklist</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Enablement</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Training</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">ICP Alignment</span>
</div>

### Steps

| Step | Template | What Happens |
|------|----------|--------------|
| 1 | [Agreement Template](../../recruitment/08-agreement/) | Finalize partnership agreement |
| 2 | [Onboarding Checklist](../../recruitment/09-onboarding/) | Track activation tasks |
| 3 | [Enablement Roadmap](../../enablement/01-roadmap/) | Plan learning journey |
| 4 | [Training Deck](../../enablement/02-training-deck/) | Customize training plan |
| 5 | [ICP Alignment Tracker](../../recruitment/10-icp-tracker/) | Align on target accounts |

```mermaid
graph LR
    A[Agreement] --> B[Checklist]
    B --> C[Enablement]
    C --> D[Training]
    D --> E[ICP Alignment]
    E --> F((Active))

    style A fill:#e8f5e9
    style B fill:#e8f5e9
    style C fill:#e8f5e9
    style D fill:#e8f5e9
    style E fill:#e8f5e9
    style F fill:#c8e6c9
```

### Run It

```bash
python agent.py --playbook onboard --partner "Acme Corp"
```

### Success Criteria

- [ ] Agreement signed
- [ ] Portal access granted
- [ ] Team trained
- [ ] First opportunity registered

---

## QBR

**Purpose:** Conduct a structured quarterly business review.

<div class="playbook-flow">
  <span class="playbook-step">Metrics</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">ICP Review</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">QBR Doc</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Strategy</span>
</div>

### Steps

| Step | Template | What Happens |
|------|----------|--------------|
| 1 | [Success Metrics](../../enablement/06-success-metrics/) | Gather performance data |
| 2 | [ICP Alignment Tracker](../../recruitment/10-icp-tracker/) | Review pipeline and accounts |
| 3 | [QBR Template](../../enablement/07-qbr-template/) | Prepare full QBR document |
| 4 | [Strategy Plan](../../strategy/05-strategy-plan/) | Update strategic alignment |

```mermaid
graph LR
    A[Metrics] --> B[ICP Review]
    B --> C[QBR Doc]
    C --> D[Strategy]
    D --> E((Aligned))

    style A fill:#fff3e0
    style B fill:#fff3e0
    style C fill:#fff3e0
    style D fill:#fff3e0
    style E fill:#c8e6c9
```

### Run It

```bash
python agent.py --playbook qbr --partner "Acme Corp"
```

### Success Criteria

- [ ] Metrics compiled
- [ ] QBR document prepared
- [ ] Meeting conducted
- [ ] Action items assigned

---

## Expand

**Purpose:** Deepen investment in a successful partnership.

<div class="playbook-flow">
  <span class="playbook-step">Business Case</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Strategy</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Co-Marketing</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Integration</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Alignment</span>
</div>

### Steps

| Step | Template | What Happens |
|------|----------|--------------|
| 1 | [Partner Business Case](../../strategy/01-partner-business-case/) | Build expansion business case |
| 2 | [Partner Strategy Plan](../../strategy/05-strategy-plan/) | Update partnership strategy |
| 3 | [Co-Marketing Playbook](../../enablement/04-co-marketing/) | Plan joint marketing |
| 4 | [Technical Integration](../../enablement/05-technical-integration/) | Deepen integration |
| 5 | [Internal Alignment](../../strategy/07-internal-alignment/) | Get internal buy-in |

```mermaid
graph LR
    A[Business Case] --> B[Strategy]
    B --> C[Co-Marketing]
    C --> D[Integration]
    D --> E[Alignment]
    E --> F((Expanded))

    style A fill:#f3e5f5
    style B fill:#f3e5f5
    style C fill:#f3e5f5
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#c8e6c9
```

### Run It

```bash
python agent.py --playbook expand --partner "Acme Corp"
```

### Success Criteria

- [ ] Expansion justified
- [ ] New initiatives planned
- [ ] Resources committed
- [ ] Tier upgrade (if applicable)

---

## Exit

**Purpose:** End a partnership professionally while protecting customers.

<div class="playbook-flow">
  <span class="playbook-step">Exit Planning</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Customer Review</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Metrics Doc</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Wind-Down</span>
</div>

### Steps

| Step | Template | What Happens |
|------|----------|--------------|
| 1 | [Exit Checklist](../../strategy/08-exit-checklist/) | Plan the exit process |
| 2 | [ICP Alignment Tracker](../../recruitment/10-icp-tracker/) | Review affected customers |
| 3 | [Success Metrics](../../enablement/06-success-metrics/) | Document final performance |
| 4 | [Exit Checklist](../../strategy/08-exit-checklist/) | Execute wind-down |

```mermaid
graph LR
    A[Exit Planning] --> B[Customer Review]
    B --> C[Metrics Doc]
    C --> D[Wind-Down]
    D --> E((Closed))

    style A fill:#ffebee
    style B fill:#ffebee
    style C fill:#ffebee
    style D fill:#ffebee
    style E fill:#ffcdd2
```

### Run It

```bash
python agent.py --playbook exit --partner "Acme Corp"
```

!!! warning "Handle with Care"
    Exit playbooks should only be run after leadership approval and legal consultation.

### Success Criteria

- [ ] Customers transitioned
- [ ] Access revoked
- [ ] Finances settled
- [ ] Post-mortem completed

---

## Creating Custom Playbooks

Add new playbooks by creating YAML files in `playbooks/`:

```yaml
name: Partner Renewal
description: Annual partnership renewal process
steps:
  - template: ../../enablement/06-success-metrics.md
    name: Review Metrics
    prompt: |
      Review the partner's performance over the past year.

  - template: ../../enablement/07-qbr-template.md
    name: Renewal Discussion
    prompt: |
      Prepare talking points for the renewal conversation.
```

See [Configuration](configuration/) for more customization options.
