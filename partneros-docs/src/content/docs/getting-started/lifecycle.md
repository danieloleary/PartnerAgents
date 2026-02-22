---
title: Partner Lifecycle
category: operational
version: 1.0.0
author: PartnerOS Team
tier:
skill_level: intermediate
purpose: operational
phase: onboarding
time_required: 1-2 hours
difficulty: easy
prerequisites:
description: Understanding the end-to-end partner journey
outcomes:
skills_gained:
keywords: ["part ways do", "need partners", "re looking", "re building", "partner program", "scratch start"]
---
# Partner Lifecycle

Every successful partnership follows a predictable lifecycle. PartnerOS provides templates for each phase.

```mermaid
graph TB
    subgraph Strategy
        A[Business Case] --> B[Ideal Partner Profile]
        B --> C[Program Design]
    end

    subgraph Recruitment
        C --> D[Identify & Qualify]
        D --> E[Pitch & Propose]
        E --> F[Sign Agreement]
    end

    subgraph Enablement
        F --> G[Onboard & Train]
        G --> H[Launch & Support]
        H --> I[Measure & Optimize]
    end

    I --> |QBR| H
    I --> |Expand| J[Grow Partnership]
    I --> |Exit| K[Graceful Termination]
```

---

## Phase 1: Strategy

**Goal:** Define *why* you need partners and *who* you're looking for.

| Template | Purpose |
|----------|---------|
| [Partner Business Case](../strategy/01-partner-business-case.md) | Justify the investment in partnerships |
| [Ideal Partner Profile](../strategy/02-ideal-partner-profile.md) | Define your target partner characteristics |
| [3C/4C Evaluation](../strategy/03-evaluation-framework.md) | Framework for assessing partner fit |
| [Competitive Differentiation](../strategy/04-competitive-differentiation.md) | Position against competitor programs |
| [Partner Strategy Plan](../strategy/05-strategy-plan.md) | Overall partnership strategy document |
| [Program Architecture](../strategy/06-program-architecture.md) | Design tiers, benefits, requirements |
| [Internal Alignment](../strategy/07-internal-alignment.md) | Get buy-in across your organization |

!!! tip "Start Here"
    If you're building a partner program from scratch, start with the **Business Case** to align stakeholders, then define your **Ideal Partner Profile**.

---

## Phase 2: Recruitment

**Goal:** Find, qualify, and sign the right partners.

| Template | Purpose |
|----------|---------|
| [Email Sequences](../recruitment/01-email-sequence.md) | Outreach templates for prospecting |
| [Outreach Engagement](../recruitment/02-outreach-engagement.md) | Multi-touch engagement cadence |
| [Qualification Framework](../recruitment/03-qualification-framework.md) | Score and prioritize prospects |
| [Discovery Call Script](../recruitment/04-discovery-call.md) | Structured qualification call |
| [Partner Pitch Deck](../recruitment/05-pitch-deck.md) | Present your partner program |
| [Partnership One-Pager](../recruitment/06-one-pager.md) | Quick overview for prospects |
| [Proposal Template](../recruitment/07-proposal.md) | Formal partnership proposal |
| [Agreement Template](../recruitment/08-agreement.md) | Legal partnership agreement |
| [Onboarding Checklist](../recruitment/09-onboarding.md) | Activation checklist |
| [ICP Alignment Tracker](../recruitment/10-icp-tracker.md) | Track customer overlap |

!!! example "Typical Recruitment Flow"
    ```
    Outreach → Discovery Call → Pitch → Proposal → Agreement → Onboarding
    ```

---

## Phase 3: Enablement

**Goal:** Train, support, and grow successful partners.

| Template | Purpose |
|----------|---------|
| [Enablement Roadmap](../enablement/01-roadmap.md) | Plan partner learning journey |
| [Training Deck](../enablement/02-training-deck.md) | Core training materials |
| [Certification Program](../enablement/03-certification.md) | Design certification tracks |
| [Co-Marketing Playbook](../enablement/04-co-marketing.md) | Joint marketing activities |
| [Technical Integration](../enablement/05-technical-integration.md) | Integration guidance |
| [Success Metrics](../enablement/06-success-metrics.md) | KPIs and measurement |
| [QBR Template](../enablement/07-qbr-template.md) | Quarterly business reviews |

---

## Ongoing Operations

### Quarterly Business Reviews

Run QBRs to maintain alignment and drive growth:

```mermaid
graph LR
    A[Gather Metrics] --> B[Prepare QBR Doc]
    B --> C[Conduct Meeting]
    C --> D[Action Items]
    D --> E[Follow Up]
    E --> |Next Quarter| A
```

[QBR Template →](../enablement/07-qbr-template.md)

### Partner Expansion

When a partnership is thriving, use these to grow:

- Update [Partner Strategy Plan](../strategy/05-strategy-plan.md)
- Expand [Co-Marketing](../enablement/04-co-marketing.md)
- Deepen [Technical Integration](../enablement/05-technical-integration.md)

### Partner Exit

When it's time to part ways, do it gracefully:

[Partner Exit Checklist →](../strategy/08-exit-checklist.md)

---

## Partner Agent Playbooks

The [Partner Agent](../agent/index.mdx) automates these workflows:

| Playbook | Lifecycle Phase | Templates Used |
|----------|-----------------|----------------|
| `recruit` | Recruitment | IPP → Qualification → Discovery → Pitch → Proposal |
| `onboard` | Enablement | Agreement → Checklist → Roadmap → Training |
| `qbr` | Ongoing | Metrics → ICP Review → QBR → Strategy |
| `expand` | Growth | Business Case → Strategy → Co-Marketing |
| `exit` | Termination | Exit Checklist → Customer Transition |

[Learn about Partner Agent →](../agent/index.mdx)
