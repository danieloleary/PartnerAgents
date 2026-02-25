---
title: Quick Start
description: Get started with PartnerAgents in 30 seconds — no install required.
template: splash
hero:
  tagline: From zero to partner in 30 seconds
  image:
    file: /src/assets/logo.svg
  actions:
    - text: Try Web UI (Recommended)
      link: /PartnerAgents/getting-started/quick-start/#web-ui
      icon: rocket
      variant: primary
    - text: Browse Templates
      link: /PartnerAgents/strategy/
      icon: open-book
---

import { Card, CardGrid, Tabs, TabItem } from '@astrojs/starlight/components';

## 1. Pick Your Path

<Tabs syncKey="path">
<TabItem label="⚡ Web UI (Recommended)">

**No install. Works in your browser.**

```bash
# Clone and run
git clone https://github.com/danieloleary/PartnerAgents.git
cd PartnerAgents
python scripts/partner_agents/web.py
```

Then open http://localhost:8000

**What you get:**
- Chat interface with your partner program
- Natural language commands: "onboard Acme", "register deal for Acme $50k"
- Full partner state management

</TabItem>
<TabItem label="💻 CLI">

**For developers who want automation.**

```bash
# Clone and run
git clone https://github.com/danieloleary/PartnerAgents.git
cd PartnerAgents

# One-shot command
python scripts/partner_agents/cli.py "onboard Acme"

# Or interactive mode
python scripts/partner_agents/cli.py
```

**Commands:**
| Command | Output |
|---------|--------|
| `onboard Acme` | Creates partner + NDA/MSA/DPA |
| `register deal Acme $50k` | Deal with 90-day protection |
| `status Acme` | Partner health & deals |
| `email Acme about renewal` | Personalized email |

</TabItem>
<TabItem label="📋 Templates Only">

**No install needed.**

Browse 40+ ready-to-use templates:

- [Strategy Templates](/PartnerAgents/strategy/) — Business case, ICP, tier design
- [Recruitment Templates](/PartnerAgents/recruitment/) — Outreach, pitch deck, proposal
- [Legal Templates](/PartnerAgents/legal/) — NDA, MSA, DPA
- [Enablement Templates](/PartnerAgents/enablement/) — Training, certification, QBR

</TabItem>
</Tabs>

---

## 2. What Can PartnerAgents Do?

<CardGrid stagger>
	<Card title="🤖 Onboard Partners" icon="rocket">
		`onboard Acme` → Creates partner, generates NDA/MSA/DPA, creates checklist
	</Card>
	<Card title="📝 Register Deals" icon="pencil">
		`register deal Acme $50k` → Deal with 90-day protection, auto-updates partner state
	</Card>
	<Card title="📊 Partner Status" icon="chart">
		`status Acme` → Tier, deals, revenue, health score
	</Card>
	<Card title="✉️ Generate Emails" icon="email">
		`email Acme about renewal` → Personalized outreach
	</Card>
	<Card title="💰 Commission Calc" icon="money">
		`commission Acme Q4` → Payout calculation with accelerators
	</Card>
	<Card title="📊 Build QBRs" icon="presentation">
		`qbr Acme` → Quarterly business review deck
	</Card>
</CardGrid>

---

## 3. What's Next?

| If you... | Then explore... |
|----------|-----------------|
| ✅ Ran a command | [AI Skills](/PartnerAgents/skills/) — All available commands |
| ✅ Want templates | [Browse 40+ Templates](/PartnerAgents/strategy/) |
| ✅ Need help | [GitHub Issues](https://github.com/danieloleary/PartnerAgents/issues) |
