---
title: PartnerAgents Assistant Agent Design
keywords: ["chase surface risks", "messy inputs then", "calendar meeting notes", "already exist memory", "db tables matching", "blocked feedback loop"]
---
# PartnerAgents Assistant Agent Design

## What it does

### Core job
1. Ingest partner signals (notes, emails, Slack threads, docs).
2. Normalize them into a consistent partner record (based on the PBP template).
3. Curate weekly updates and exec-ready briefs.
4. Maintain an action register with owners and dates (and chase).
5. Surface risks and asks so leadership time goes where it matters.

### North Star
Make partner management feel like one cockpit, not 12 tabs and 400 Slack messages.

## Data model (copy the PBP)

Use the Partner Business Plan (PBP) template as the canonical schema.

### Partner Profile and Alignment
- Goals, priorities, challenges, partnership relevance.
- Importance of Axon, share of business, new vs existing clients (dropdown-driven).

### Coverage and Capability
- Current Axon products, appetite to expand, familiarity with portfolio.

### Operating Plan
- SMART action plan: task, why, measurable outcome, owner, timeline.

### Partner Pod
- Named people, roles, must-haves (2 sellers, 2 SEs, exec sponsor).

Why this matters: the agent can fill the sheet automatically from messy inputs,
then you sanity-check.

## Agent architecture (simple, reliable, shippable)

### 1) Ingestion layer

Start with the sources you already use:
- Slack: capture key messages and threads (partner updates, asks, blockers).
- SharePoint docs and sheets: PBPs, plans, meeting notes.

Add next (optional, high value):
- Email and calendar meeting notes, to detect weekly changes.

### 2) Extraction and normalization

Pipeline:
- Classify content: update, decision, risk, ask, next step, artifact link.
- Entity extraction: partner name, accounts, product lines, people, dates,
  commitments.
- Write to partner record (PBP schema).
- Write to action register (task, owner, due date, status).

This is not AI magic. It is mostly turning free text into structured fields
that already exist.

### 3) Memory and storage
- Partner records stored as structured JSON (or DB tables) matching the PBP
  sections.
- Each extracted fact links back to the source (Slack permalink, doc link) for
  auditability.

### 4) Reasoning layer (outputs)
- Weekly partner brief (per partner): wins, changes, open risks, top 3 next
  actions, asks.
- Portfolio rollup: what is hot, what is stuck, where exec air cover is needed.
- Meeting prep pack: last decisions and unresolved items.
- Auto-updated action register: what is due this week, who is late, what is
  blocked.

### 5) Feedback loop

The agent always asks one question when uncertain:
- "I found 2 possible owners for this action. Pick one."
- "Due date mentioned as end of month. Should I set Jan 31, 2026?"

This prevents hallucinated accountability.

## Agent behaviors (the how)

### A) Curate and summarize
- Default view: last 7 days of changes per partner.
- Tag everything as Decision, Update, Risk, Ask, or Next step.
- Keep it tight: 5 to 10 bullets per partner.

### B) Maintain the action register

Use the PBP action table as the template.

Rules:
- Every action must have Owner and Date or it is Draft.
- Every due date triggers reminders at T-7, T-3, T-1.
- Every overdue action becomes a Blocker until cleared.

### C) Produce exec-grade partner plans

Use the updated Accenture PBP as the gold standard:
- Clear tasks, DRIs, and dates.
- Explicit asks (exec sponsor, pricing guardrails, artifacts, legal).

The agent replicates this format for every strategic partner.

### D) Make-it-easy-to-buy hygiene

If a partner plan is missing:
- Exec sponsor
- 2 sellers and 2 SEs
- Training commitment

Then flag it as a structural gap.

## MVP scope (ship in 2 sprints)

### MVP v0
- Ingest Slack and SharePoint PBP docs.
- Auto-generate:
  - Partner brief
  - Action register
  - Asks list
- Manual confirmation UI: approve edits before writing back.

### v1
- Add email and calendar ingestion.
- Add meeting prep pack.
- Add partner tier tags and a simple health score (green/yellow/red).

## Implementation notes

### Prompts (high-level)
- "Extract PBP fields from this text. Output JSON with confidence scores."
- "Generate weekly partner brief from partner record plus last 7 days deltas."
- "Generate action items, require owner and due date, else mark as Draft."

### Evaluation
- Precision on action extraction (no phantom tasks).
- Owner assignment accuracy.
- "Did it save Dan time?" measured by fewer manual updates.

### Hard guardrails
- No auto-sending external partner emails without explicit approval.
- No overwriting PBP fields unless confidence is high or you approve.

## Owners and dates

- Owner: Dan (product owner).
- DRI to build: one engineer (or whoever owns the PartnerAgents repo).
- By Jan 17, 2026: finalize MVP spec (sources, outputs, UI, guardrails).
- By Jan 31, 2026: MVP live for 2 pilot partners (one should be Accenture).

## One-line takeaway
Build the agent around the PBP template and the action register, and it will
scale your partner brain without inventing new process.
