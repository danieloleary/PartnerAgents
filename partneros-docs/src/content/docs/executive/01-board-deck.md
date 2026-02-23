---
title: Board Deck — Partner Program
section: Executive
category: executive
template_number: X.1
version: 2.0.0
last_updated: 2026-02-21
author: PartnerOS Team
tier: Bronze
skill_level: advanced
purpose: strategic
phase: enablement
time_required: 4-8 hours
difficulty: hard
prerequisites: [Partner program data, QBR metrics]
description: >
  Board presentation template for partner program strategic reviews.
outcomes: [Secure board buy-in, Demonstrate ROI, Obtain resource approval]
skills_gained: [Executive presentation, Strategic communication, Board-level storytelling]
keywords: ["board presentation", "partner program", "executive summary", "board deck", "strategic update"]
---

> **Board presentations should tell a story. Numbers matter—but narrative matters more.** — Dan O'Leary

:::tip[Insider Tip]
Board meetings are not status reports. They're strategic reviews. Your deck should answer: "Are we winning? What's changing? What do we need?"
:::

## Presentation

<div class="presentation-controls">
  <button class="present-btn" id="presentBtn">
    <span class="icon">🎮</span>
    <span class="text">Present in Browser</span>
  </button>
  
  <a href="/assets/pptx/board-deck.pptx" download class="download-btn">
    <span class="icon">📥</span>
    <span class="text">Download PPTX</span>
  </a>
</div>

<div id="present-modal" class="present-modal" hidden>
  <div class="present-container">
    <div class="present-header">
      <span class="present-title">Board Deck - Q4 2025</span>
      <button class="close-btn" id="closePresent">✕</button>
    </div>
    <div class="present-content">
      <iframe 
        id="presentFrame"
        src="" 
        frameborder="0" 
        style="width: 100%; height: 100%;"
      ></iframe>
    </div>
  </div>
</div>

<p style="font-size: 0.9em; color: var(--sl-color-gray-3); margin-top: 8px;">
  <em>Edit the demo data in <code>examples/demo-company/board-deck-data.json</code> and run <code>python3 scripts/generate_pptx.py</code> to regenerate with your own metrics.</em>
</p>

<style>
  .presentation-controls {
    display: flex;
    gap: 12px;
    margin: 24px 0;
    padding: 20px;
    background: var(--sl-color-gray-6);
    border-radius: 12px;
    border: 1px solid var(--sl-color-gray-5);
  }

  .present-btn,
  .download-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    border: none;
  }

  .present-btn {
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    color: white;
  }

  .present-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  }

  .download-btn {
    background: var(--sl-color-gray-5);
    color: var(--sl-color-text);
    border: 1px solid var(--sl-color-gray-4);
  }

  .download-btn:hover {
    background: var(--sl-color-gray-4);
  }

  .icon {
    font-size: 16px;
  }

  .present-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.9);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
    box-sizing: border-box;
  }

  .present-container {
    width: 100%;
    max-width: 1200px;
    aspect-ratio: 16/9;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .present-header {
    padding: 16px 24px;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .present-title {
    color: white;
    font-weight: 600;
    font-size: 16px;
  }

  .close-btn {
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
  }

  .close-btn:hover {
    background: rgba(255,255,255,0.3);
  }

  .present-content {
    flex: 1;
    background: #f3f4f6;
  }
</style>

<script>
  const presentBtn = document.getElementById('presentBtn');
  const closeBtn = document.getElementById('closePresent');
  const modal = document.getElementById('present-modal');
  const frame = document.getElementById('presentFrame');
  
  // PPTX file URL - use a relative URL for local dev
  const pptxUrl = '/assets/pptx/board-deck.pptx';
  
  // Build Office Online embed URL
  const baseUrl = 'https://view.officeapps.live.com/op/embed.aspx';
  // For local development, we'd need to host the file publicly
  // For now, show a message about downloading
  
  presentBtn?.addEventListener('click', () => {
    // Try Office Online embed first
    // Note: This requires the PPTX to be publicly accessible
    // For local dev, we'll show a fallback message
    
    modal.hidden = false;
    
    // Check if we can use Office Online
    // Since we can't easily host locally for Office Online,
    // show a demo message
    frame.src = 'data:text/html,' + encodeURIComponent(`
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 40px;
          }
          h1 { font-size: 32px; margin-bottom: 16px; }
          p { font-size: 16px; opacity: 0.9; max-width: 500px; line-height: 1.6; }
          .download-btn {
            margin-top: 32px;
            background: white;
            color: #6366F1;
            border: none;
            padding: 16px 32px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
          }
        </style>
      </head>
      <body>
        <h1>🎉 Presentation Ready!</h1>
        <p>To present in browser with full features, you can:</p>
        <ol style="text-align: left; max-width: 400px; margin: 24px auto;">
          <li>Download the PPTX file</li>
          <li>Open in PowerPoint or Google Slides</li>
          <li>Present from there with animations</li>
        </ol>
        <a href="${pptxUrl}" download class="download-btn">
          📥 Download Board Deck
        </a>
      </body>
      </html>
    `);
    
    document.body.style.overflow = 'hidden';
  });
  
  closeBtn?.addEventListener('click', closeModal);
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });
  
  function closeModal() {
    modal.hidden = true;
    document.body.style.overflow = '';
    frame.src = '';
  }
  
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
</script>

## How to Use This Template

**Purpose:**
This deck communicates partner program performance and strategy to the board of directors. It positions the partner program as a strategic growth driver.

**Why It Works:**
A well-structured board deck demonstrates executive presence, strategic thinking, and data-driven decision making. It builds confidence in the partner program and secures ongoing investment.

**Steps:**

1. **Gather data** — Pull metrics and prepare analytics (1-2 hours)
2. **Build narrative** — Structure the story (2-3 hours)
3. **Rehearse** — Practice delivery with Q&A (1 hour)
4. **Present** — Deliver to board (15-20 min + Q&A)

---

# Board Deck Structure

## The 6-Slide Framework

| Slide | Purpose | Time |
|-------|---------|------|
| 1. Executive Summary | One-slide overview | 2 min |
| 2. Strategic Context | Why partners matter | 3 min |
| 3. Performance | Results vs. plan | 5 min |
| 4. Partner Health | Detailed KPIs | 3 min |
| 5. Roadmap | Future plans | 3 min |
| 6. The Ask | Resource request | 2 min |

---

## Slide 1: Executive Summary

**Headline:** Partner Program — Q[X] [YEAR] Update

**Purpose:** Give the board everything they need to know on one slide.

**Content:**

- **Program at a glance:** Total partners, revenue, growth
- **Key wins:** Top 2-3 accomplishments this quarter
- **Key risks:** Top 1-2 concerns (be honest)
- **This quarter's number:** Single most important metric
- **Board decision needed:** What's being asked today

**Example:**
```
Partner Program Q4 2025

📊 At a Glance
• 47 active partners (+12 this quarter)
• $2.3M partner-sourced revenue (+34% YoY)
• 23% of total revenue from partners

✅ Key Wins
• Launched Gold tier with 5 strategic partners
• First $500K+ partner deal closed

⚠️ Focus Areas
• 3 partners at risk of churn
• Slow adoption of new certification

📈 The Number: $2.3M (+34% YoY)

💬 Today: Seeking approval for $150K partner marketing fund
```

**Speaker Notes:**

- Start with the headline number
- Acknowledge challenges upfront — boards respect honesty
- Make the "ask" crystal clear

---

## Slide 2: Strategic Context

**Headline:** Why Partners Are Strategic

**Purpose:** Remind the board why we invest in partners.

**Content:**

- **Strategic rationale:** 2-3 sentences on why partners drive growth
- **Market context:** What's happening in the market that makes partners important
- **Competitive landscape:** How competitors use partners
- **Our approach:** Brief summary of partner strategy

**Example:**
```
Strategic Rationale

Partners provide:
• Scale: Reach customers we can't (45% of market)
• Speed: Faster GTM in new verticals
• Trust: Partner relationships reduce sales cycle 30%

Market Context
• Competitors investing heavily in partner ecosystems
• Customer buying preferences shifting to solutions over single products

Our Position
• Building a tiered ecosystem (Bronze/Silver/Gold)
• Focused on 3 strategic verticals
```

**Speaker Notes:**

- This is your "why" slide
- Connect to board's strategic priorities
- Show you understand the competitive landscape

---

## Slide 3: Performance

**Headline:** Q[X] Performance vs. Plan

**Purpose:** Show whether we're hitting our targets.

**Content:**

- **Revenue:** Partner-sourced revenue vs. target
- **Growth:** YoY and QoQ trends
- **Pipeline:** Partner-generated pipeline
- **Top partners:** Revenue by top 5 partners
- **Variance analysis:** Why we did/didn't hit targets

**Example:**
```
Q4 Performance

Revenue: $2.3M (+34% YoY, -5% vs. plan)
├── Partner-sourced: $1.4M (61%)
├── Partner-influenced: $900K (39%)
└── vs. Plan: $2.4M target

Pipeline: $4.2M (+50% QoQ)
├── Registered deals: $2.8M
├── Stage distribution: 40% Qual, 30% Prop, 30% Close

Top Partners
├── Acme Corp: $420K (18%)
├── TechStart: $380K (17%)
├── GlobalSys: $290K (13%)
└── ...

Missed Plan: Why?
• 2 strategic deals pushed to Q1
• New partner ramp took longer than expected
```

**Visual Tip:** Use a combo chart showing actual vs. target with variance callouts.

**Speaker Notes:**

- Explain the variance — don't hide misses
- Highlight what's driving revenue
- Call out partner-specific wins

---

## Slide 4: Partner Health KPIs

**Headline:** Partner Program Health

**Purpose:** Deep dive into the metrics that matter.

**Content:**

- **Partner count:** Active by tier
- **Engagement:** Certified partners, deal regs, co-marketing
- **Retention:** Churn rate, expansion revenue
- **Productivity:** Revenue per partner, time to first deal

**Example:**
```
Partner Health Dashboard

Partner Count: 47 active (+12 Q4)
├── Gold: 5 (target: 8)
├── Silver: 12 (target: 15)
└── Bronze: 30 (target: 35)

Engagement Score: 72/100
├── Certified partners: 28 (60%)
├── Deal registrations: 34
└── Co-marketing events: 8

Retention & Growth
├── Churn rate: 8% (target: <10%)
├── Expansion revenue: $340K
└── NPS: 42 (up from 38)

Productivity
├── Revenue/partner: $49K
├── Time to first deal: 4.2 months
└── Win rate: 34%
```

**Visual Tip:** Use a dashboard layout with green/yellow/red indicators for traffic light status.

**Speaker Notes:**

- Walk through each quadrant
- Call out trends — what's improving, what's declining
- Connect metrics to business outcomes

---

## Slide 5: Roadmap

**Headline:** Partner Program Roadmap

**Purpose:** Show what's coming and when.

**Content:**

- **This quarter:** Current initiatives
- **Next quarter:** Planned launches
- **Year ahead:** Strategic priorities
- **Key milestones:** Dates the board should know

**Example:**
```
2026 Partner Roadmap

Q1 (Current)
├── Launch partner portal v2.0
├── Recruit 5 new Gold partners
└── Expand to 2 new verticals

Q2 (Planned)
├── Launch co-sell incentive program
├── Add 10 new Silver partners
└── Partner certification revamp

H2 Priorities
├── International partner expansion
├── Partner-led growth >30% of revenue
└── Launch partner marketplace

Board Milestones
├── Mar: Portal launch
├── Jun: Co-sell program live
└── Dec: 30% revenue target
```

**Visual Tip:** Use a timeline or Gantt-style visual with milestones marked.

**Speaker Notes:**

- Connect to strategic context from Slide 2
- Show resource requirements implicitly through scope
- Highlight dependencies on other teams

---

## Slide 6: The Ask

**Headline:** Resource Request

**Purpose:** Make a specific, justified request.

**Content:**

- **The ask:** Specific request (budget, headcount, approval)
- **The why:** Business case for investment
- **The return:** Expected ROI or impact
- **The risk:** What happens without it

**Example:**
```
The Ask: $150K Partner Marketing Fund

Why We Need It
• Current fund exhausted (used for Q4 launches)
• Q1 pipeline dependent on co-marketing
• 3 major events require sponsorship

Expected Return
• Generate $600K pipeline (4:1 ROI)
• Enable 8 co-marketing campaigns
• Support 5 new partner launches

Risk of Inaction
• Lose co-marketing momentum
• Miss Q1 pipeline targets
• Partner satisfaction decline

Request: Approve Q1 marketing fund by [DATE]
```

**Visual Tip:** Keep it simple — ask in one line, supporting detail below.

**Speaker Notes:**

- Be specific: "I'm asking for X"
- Connect to board priorities
- Be prepared for negotiation

---

## Common Board Questions

Prepare answers to these likely questions:

| Question | How to Answer |
|----------|---------------|
| "Why is partner revenue down?" | Show trend, explain cause, share recovery plan |
| "What's the ROI on partners?" | Compare CAC with vs. without partners |
| "Who are our top partners?" | Name names, show revenue concentration |
| "What's the churn rate?" | Be honest, explain root cause |
| "Why should we invest more?" | Quantify the opportunity |

---

## Common Pitfalls

**Pitfall #1: Data Dump**
- **What happens:** Overwhelm the board with spreadsheets
- **Warning sign:** >10 metrics on a slide
- **Prevention:** One key message per slide

**Pitfall #2: No Story**
- **What happens:** Sounds like a status report
- **Warning sign:** "First we did X, then we did Y..."
- **Prevention:** Lead with conclusions, support with data

**Pitfall #3: Hiding Bad News**
- **What happens:** Lose credibility when issues surface
- **Warning sign:** Only showing green metrics
- **Prevention:** Acknowledge issues, show action plan

**Pitfall #4: Vague Asks**
- **What happens:** No decision made, no progress
- **Warning sign:** "Looking for guidance"
- **Prevention:** Specific request with timeline

---

## Visual Design Tips

- **Keep it clean:** Max 6 bullet points per slide
- **Use visuals:** Charts, dashboards, timelines
- **One message per slide:** Boards decide on headlines
- **Consistent formatting:** Same template every quarter
- **High contrast:** Test in the boardroom (projector-friendly)

---

## Quick Win Checklist

*Complete these first (2 hours)*

- [ ] Pull Q[X] partner revenue data
- [ ] Update partner count by tier
- [ ] Create Executive Summary slide
- [ ] Draft the Ask slide
- [ ] Practice 3-minute walkthrough

---

## Full Implementation

*Complete for standard implementation (4-8 hours)*

- [ ] Complete all 6 slides with full content
- [ ] Prepare speaker notes for each slide
- [ ] Build supporting appendix (optional)
- [ ] Rehearse with C-suite peer
- [ ] Prepare Q&A backup slides
- [ ] Send deck 48 hours in advance

---

## Related Templates

- [Strategy Plan](../strategy/05-strategy-plan/) — Program strategy
- [Success Metrics](../enablement/06-success-metrics/) — Track KPIs
- [Health Scorecard](../analysis/01-health-scorecard/) — Detailed assessment
- [Monthly Partner Report](../operations/03-monthly-report/) — Operational updates
