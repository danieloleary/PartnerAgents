---
title: Template Quality Auditor (Expert Edition)
description: Expert framework for auditing and improving PartnerOS templates to A+ standard - with insider tactics, metrics, and stakeholder strategies
version: 3.0.0
last_updated: 2026-02-21
author: PartnerOS Team
tags: 
keywords: ["expert level framework", "frontmatter title start", "content here note", "important information caution", "links every metric", "tables should have"]
---
# Template Quality Auditor (Expert Edition)

## Purpose

This skill provides an **expert-level framework** for auditing and improving PartnerOS templates to A+ quality standard. Unlike generic templates, expert partner leaders bring strategic value—they know what moves the needle, what convinces stakeholders, and what goes wrong.

> **"The difference between a template that's a paperweight and one that drives revenue is understanding the person who'll read it—and what they actually care about."**
> — Dan O'Leary, PartnerOS

---

## Specialized Skills

This is the master skill. For specific tasks, use these dedicated skills:

| Skill | When to Use |
|-------|-------------|
| [Starlight Formatting Guide](./starlight-formatting/) | Formatting templates for Starlight/Astro |
| [Glossary Maintenance](./glossary-maintenance/) | Adding/updating glossary terms |
| [Find and Fix Broken Links](./find-broken-links/) | Fixing broken link issues |

---

## The A+ Template Standard

An A+ template meets ALL of these criteria:

### 1. Expert Voice ✓
- **Sounds like Dan O'Leary** - confident, specific, experienced
- Uses authoritative language ("you must", "critical", "essential")
- Avoids hedging ("maybe", "possibly", "might want to consider")
- Direct actionable guidance, not suggestions

### 2. Substance Over Form ✓
- Full paragraphs explaining WHY, not just WHAT
- Context for every section
- Rationale for recommendations
- Consequences of decisions

### 3. Complete Coverage ✓
- Covers topic end-to-end (start → finish)
- Addresses edge cases
- Includes troubleshooting/common pitfalls
- Has clear next steps

### 4. No Placeholders ✓
- No empty brackets `[ ]` - real guidance only
- If placeholder needed, use specific example: "e.g., Acme Corp" not "[Company Name]"
- Every field has explanation of what goes there and why

### 5. Real Examples ✓
- Concrete, specific examples throughout
- Not generic - use realistic company names, numbers, scenarios
- Show both good AND bad examples where helpful
- Examples demonstrate the standard to achieve

### 6. Two Versions ✓

| Version | Purpose | Naming |
|---------|---------|--------|
| **Template** | Fill-in-the-blank for user's use | `XX-name.md` |
| **Example** | Fully filled showing complete example | `examples/complete-examples/[category]/XX-name-example.md` |

---

## Starlight Formatting Rules

Templates are rendered using **Astro Starlight**, which has specific formatting requirements. Following these ensures your template looks professional and renders correctly.

### Critical Rules

1. **Start with paragraphs, NOT headings**
   - Starlight automatically adds an H1 from the frontmatter title
   - Start your page with 2-3 sentences of intro, then use H2 (`##`) for sections
   - Never use H1 after the frontmatter

2. **Each major section needs context paragraphs**
   - BEFORE a table: Explain what the table shows and why it matters
   - AFTER a table: Interpret the data, explain what the numbers mean
   - Never just drop a table without explanation

3. **Use Starlight asides for callouts**
   ```markdown
   :::tip[Custom Title]
   Your content here
   :::

   :::note
   For important information
   :::

   :::caution
   For warnings
   :::
   ```

4. **Glossary cross-references**
   - Use links to the [Partner Program Glossary](../resources/glossary/)
   - Link terms like: `TAM`, `SAM`, `SOM` (plain text, not links)
   - Every metric in tables should have a definition

### Table Best Practices

**WRONG (AI slop):**
```
| Metric | Value |
|--------|-------|
| TAM | $48B |
```

**RIGHT (Expert):**
```
Here's what each market level means:
- TAM is the ceiling—the total market
- SAM is what you can reach
- SOM is what you can capture

| Level | Definition | Amount |
|-------|------------|--------|
| TAM | Total Addressable Market | $48B |
```

### Heading Hierarchy

Starlight expects this structure:
```markdown
---
title: My Page Title
---

Intro paragraph goes here...

## Section 1 (H2)
### Subsection (H3)

## Section 2 (H2)
### Subsection (H3)
```

### Common AI Slop Patterns to Avoid

| Bad Pattern | Why It's Bad | Fix |
|-------------|--------------|-----|
| Tables without context | Confusing, no interpretation | Add paragraph before AND after |
| Headings without intro | Cluttered TOC | Start with paragraph |
| Placeholder brackets `[ ]` | Looks unfinished | Use real examples |
| Generic examples | Not actionable | Use specific company names |
| No glossary links | Sounds amateur | Link to glossary terms |
| Only bullets | No depth | Add paragraphs |

---

## Expert Tactics: The Secret Sauce

### What Expert Partner Leaders Know

Expert templates include insights that only come from experience:

#### 1. "What I Wish I Knew" Insights
Include a section with hard-learned lessons:

```markdown
### What I Wish I Knew Before I Started

**The hidden cost no one talks about:**
- Partner programs take 18 months before revenue materializes
- Your first 5 partners will teach you more than any consultant

**The question that closes deals:**
- "What would it take to make this your #1 vendor in this category?"

**The mistake that kills programs:**
- Launching without clear partner success metrics
```

#### 2. Negotiation Levers
For templates involving agreements or deals:

```markdown
### Negotiation Levers

| What Partners Want | Your Leverage | Common Concession |
|-------------------|---------------|-------------------|
| Higher margins | Exclusive territory | Volume bonuses |
| Faster payment | Priority leads | Quarterly vs annual |
| Co-marketing funds | Certification | Staff training |
| Protected pricing | Deal registration | Volume tiers |
```

#### 3. Internal Sell Tactics
For strategic templates (business cases, ROI):

```markdown
### How to Sell This Internally

**For the CFO:**
- Focus on: ROI, payback period, risk mitigation
- Language: "Breaks even in 18 months", "2.3x return"
- Avoid: Growth projections without cost controls

**For the CEO:**
- Focus on: Market share, competitive moat, speed to market
- Language: "First-mover advantage", "Channel vs competitors"
- Avoid: Detailed financials they can't action

**For VP Sales:**
- Focus on: Territory protection, deal registration
- Language: "No channel conflict", "Pipeline acceleration"
- Avoid: Anything that sounds like replacing direct sales
```

---

## Metrics That Matter

Expert templates include specific, benchmarked metrics—not vague "track progress."

### The 36 Partnership Metrics (Industry-Validated)

From partnership leader research, here are the metrics that matter:

#### Revenue Metrics
| Metric | Definition | Benchmark |
|--------|------------|-----------|
| Partner-Sourced Revenue | Revenue from deals where partner is primary driver | 15-30% of total |
| Partner-Influenced Revenue | Revenue where partner contributed to sale | 25-50% of total |
| Partner Program Revenue | Total revenue from partner channel | Growing YoY |
| Revenue per Partner | Average revenue per active partner | $50K-200K |

#### Partner Health Metrics
| Metric | Definition | Benchmark |
|--------|------------|-----------|
| Time to First Revenue | Days from partner signing to first deal | < 90 days |
| Time to Productivity | Days to partner's 5th deal | < 180 days |
| Partner NPS | Partner satisfaction score | 50+ |
| Partner Retention Rate | % partners renewing annually | > 80% |

#### Program Efficiency Metrics
| Metric | Definition | Benchmark |
|--------|------------|-----------|
| Cost to Acquire Partner | Total acquisition cost / # partners | < $5K |
| Partner Program ROI | (Revenue - Cost) / Cost | > 3x |
| Win Rate with Partner | Close rate on co-sold deals | > 40% |
| Partner Pipeline Coverage | Partner pipeline / quota | > 3x |

### Template Metric Requirements

Every template that mentions metrics should include:

1. **Specific KPI name** (not "track progress")
2. **Industry benchmark** (so user knows target)
3. **How to measure** (formula or method)
4. **Warning signs** (what's off-track)

```markdown
### Key Metrics to Track

| Metric | Target | How to Measure |
|--------|-------|---------------|
| Time to First Revenue | < 90 days | First deal date - contract signed date |
| Partner NPS | 50+ | Quarterly survey via PRM |
| Partner-Influenced Revenue | 30% of total | Marked deals in CRM + partner attribution |
```

---

## Stakeholder Playbooks

Expert templates speak the language of the person who'll use them.

### CFO Language
```markdown
**What they care about:**
- ROI and payback period
- Risk mitigation
- Budget predictability
- Clear success metrics

**Phrases that work:**
- "Breaks even in 18 months"
- "2.3x return on investment"
- "Fixed cost, variable return"
- "No CapEx required"
```

### CEO Language
```markdown
**What they care about:**
- Market share growth
- Competitive positioning
- Speed to market
- Scalable growth engine

**Phrases that work:**
- "First-mover advantage in channel"
- "Competitor X has 40% via channel—we're at 0%"
- "Turn fixed costs into variable"
- "Revenue at scale without headcount"
```

### VP Sales Language
```markdown
**What they care about:**
- Territory protection
- Deal registration
- No channel conflict
- Quota attainment

**Phrases that work:**
- "Deal registration prevents conflict"
- "Partners sell to ICP we can't reach"
- "3x pipeline coverage from channel"
- "No displacement of direct deals"
```

---

## Failure Modes: What Goes Wrong

Expert templates anticipate failure and prevent it.

### Top 5 Reasons Partner Programs Fail

| # | Failure Mode | Warning Signs | Prevention |
|---|-------------|--------------|------------|
| 1 | No partner revenue in 18 months | Low engagement, no deals | Clear milestones, accountability |
| 2 | Channel conflict with direct sales | Sales team blocking partners | Deal registration, territories |
| 3 | Partner churn after Year 1 | No tier progression | Clear value prop, regular QBRs |
| 4 | Operational overwhelm | Missed commissions, slow onboarding | Automation, clear processes |
| 5 | Executive losing interest | No quick wins | Monthly progress reports |

### Template Failure Prevention

For each template, include:

```markdown
### Common Pitfalls

**Pitfall #1: [Name]**
- **What happens:** [Specific failure]
- **Warning sign:** [How to detect early]
- **Prevention:** [What to do instead]

**Pitfall #2: [Name]**
- **What happens:** [Specific failure]
- **Warning sign:** [How to detect early]
- **Prevention:** [What to do instead]
```

---

## Progressive Levels

Expert templates meet users where they are:

### Level 1: Quick Win (30 min)
- Core template only
- Essential fields
- Basic example

### Level 2: Standard (2-4 hours)
- Full template
- Metrics and benchmarks
- Implementation guide

### Level 3: Strategic (8-16 hours)
- Full business case
- Stakeholder arguments
- Risk analysis
- Executive presentation

### Template Structure for Levels

```markdown
## Quick Win Section
*[Complete this in 30 minutes]*

## Standard Implementation
*[Complete this in 2-4 hours]*

## Strategic Deep Dive
*[Optional: Complete for executive presentations]*
```

---

## Template Structure (Full)

Each template should have:

```markdown
---
title: [Clear Title]
section: [Category]
category: [strategic|operational|tactical|legal|financial|security|executive|analytical]
template_number: [I.1, II.2, etc.]
version: 1.0.0
last_updated: [YYYY-MM-DD]
author: PartnerOS Team
tier: [Bronze|Silver|Gold]
skill_level: [beginner|intermediate|advanced]
purpose: [strategic|operational|tactical]
phase: [recruitment|onboarding|enablement|growth|retention|exit]
time_required: [e.g., "2-3 hours"]
difficulty: [easy|medium|hard]
prerequisites: []
description: >
  [2-3 sentence description - what this IS and why it matters]
purpose_detailed: >
  [Extended description of use case and business value]
outcomes:
  - [Concrete outcome 1]
  - [Concrete outcome 2]
skills_gained:
  - [Skill 1]
  - [Skill 2]
---

> **Expert quote or summary** - captures the essence

:::tip[Insider Tip]
Key insider tip or common mistake to avoid
:::

## How to Use This Template

**Purpose:**
[One sentence - what this template accomplishes]

**Why It Works:**
[Brief explanation of business value]

**Steps:**
1. [Step with context]
2. [Step with context]
3. [Step with context]

---

# [Template Title]

## Section 1: [Name]

### What I Wish I Knew Before I Started
[Hard-learned lessons for this section]

### Subsection

[Full paragraph explaining context, why this matters, what to consider]

**[Guidance in bold]:** [Specific actionable instruction]

**Example:**
```
[Real example with specific details]
```

### Key Metrics to Track
| Metric | Target | How to Measure |
|--------|-------|---------------|
| [Metric 1] | [Benchmark] | [Formula] |
| [Metric 2] | [Benchmark] | [Formula] |

### Common Pitfalls
**Pitfall #1: [Name]**
- **What happens:** [Specific failure]
- **Warning sign:** [How to detect early]
- **Prevention:** [What to do instead]

---

## Section 2: [Name]

[Continue with same pattern...]

---

## Quick Win Checklist
*[Complete these first]*

- [ ] [Essential item 1]
- [ ] [Essential item 2]

## Full Implementation
*[Complete for standard implementation]*

- [ ] [Additional item 1]
- [ ] [Additional item 2]

## Executive Ready
*[Include for strategic presentations]*

- [ ] [CFO arguments]
- [ ] [ROI calculation]
- [ ] [Risk analysis]

---

## Quality Checklist

Before marking a template as A+ complete, verify:

- [ ] Expert voice throughout (confident, specific)
- [ ] Every section has substantive paragraphs
- [ ] No placeholder brackets `[ ]` remain
- [ ] Real examples embedded in template
- [ ] "What I Wish I Knew" section included
- [ ] Metrics with benchmarks included
- [ ] Common pitfalls identified
- [ ] Example version created in `examples/complete-examples/`
- [ ] Frontmatter complete (17 fields)
- [ ] Metadata table present
- [ ] Related templates cross-referenced
- [ ] No broken internal links
- [ ] Stakeholder language included (CFO/CEO/VP Sales)
- [ ] Progressive levels available (Quick Win / Standard / Strategic)
- [ ] **Starlight formatting** - paragraphs before headings, no H1 after frontmatter
- [ ] **Table context** - paragraphs before AND after every major table
- [ ] **Glossary links** - all metrics link to [Glossary](/resources/glossary/)
- [ ] **Asides used** - :::tip, :::note, :::caution for callouts
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-21 | Initial release |
| 2.0 | 2026-02-21 | Added expert tactics, metrics, stakeholder playbooks, failure modes, progressive levels |
| 3.0 | 2026-02-21 | Added Starlight formatting rules, table best practices, glossary integration |

---

*This skill is maintained by PartnerOS. For questions, contact the team.*
