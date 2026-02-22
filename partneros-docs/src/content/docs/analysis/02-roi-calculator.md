---
title: Partner ROI Calculator
description: Calculate the return on investment for your partner program with interactive formulas and real-world examples.
section: Analysis
category: analytical
template_number: A.2
version: 1.0.0
author: PartnerOS Team
last_updated: 2026-02-22
tier: Silver
skill_level: intermediate
purpose: analytical
phase: analysis
time_required: "1-2 hours"
difficulty: medium
prerequisites: [Partner Business Case Template]
outcomes: [ROI calculation spreadsheet, Investment case, Payback period analysis]
skills_gained: [Financial modeling, ROI analysis, Investment planning]
tags: [roi, calculator, finance, investment, metrics]
keywords: ["compelling financial case", "justify investment why", "isn t guesswork", "paybackmonths paybackmonths n", "money back aim", "first minutes define"]
---
Use this template to build a compelling financial case for your partner program—or to validate an existing one.

:::tip[Insider Tip]
The #1 reason partner programs get cancelled? No clear ROI. CFOs approve budgets that show measurable return, not "strategic alignment." This calculator gives you the numbers.
:::

## How to Use This Template

This template provides the formulas, frameworks, and examples you need to calculate partner program ROI. It's designed for finance teams, partner managers, and executives who need to justify investment.

### Why It Works

When you can show a CFO exact payback period and ROI multiples, you remove the biggest blocker to program approval. This isn't guesswork—it's financial rigor.

### Choose Your Level

| Level | Time | Best For |
|-------|------|----------|
| **Quick Win** | 30 min | Ballpark estimate for leadership |
| **Standard** | 1-2 hr | Detailed model with scenarios |
| **Executive** | 2-3 hr | Board-ready presentation |

---

## The Partner ROI Framework

Before calculating, understand the key components that drive partner program ROI:

### Revenue Inputs

- **Partner-sourced revenue**: Revenue from deals partners bring directly
- **Partner-influenced revenue**: Revenue from deals with partner involvement
- **Partner-sourced pipeline**: Registered deals in sales funnel
- **Partner quote volume**: Quotes/proposals with partner pricing

### Cost Inputs

- **Program operational costs**: Partner management, training, enablement
- **Partner enablement costs**: Training, certifications, marketing funds
- **Technology costs**: Partner portal, CRM, PRM system
- **Partner incentive costs**: Rebates, commissions, SPIFFs

### The Core Formula

```
ROI = (Net Partner Revenue - Total Partner Costs) / Total Partner Costs × 100

Payback Period = Total Partner Costs / Monthly Partner Revenue
```

---

## Step-by-Step Calculator

### Step 1: Calculate Partner Revenue

Use this section to estimate revenue from your partner program.

| Metric | Year 1 | Year 2 | Year 3 | Source |
|--------|--------|--------|--------|--------|
| Active Partners | 10 | 25 | 50 | Recruitment plan |
| Revenue per Partner | $15,000 | $20,000 | $25,000 | Conservative estimate |
| **Total Partner Revenue** | $150,000 | $500,000 | $1,250,000 | — |

### Step 2: Calculate Partner Costs

| Cost Category | Year 1 | Year 2 | Year 3 | Notes |
|---------------|--------|--------|--------|-------|
| Partner Manager (1 FTE) | $120,000 | $130,000 | $140,000 | Fully loaded |
| Partner Marketing Funds | $30,000 | $75,000 | $150,000 | 20% of partner revenue |
| Training & Enablement | $25,000 | $40,000 | $60,000 | Per-partner training |
| Technology (PRM/Portal) | $20,000 | $25,000 | $30,000 | SaaS subscriptions |
| Partner Commissions | $22,500 | $100,000 | $312,500 | 15% average |
| **Total Costs** | $217,500 | $370,000 | $692,500 | — |

### Step 3: Calculate ROI

| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| Total Partner Revenue | $150,000 | $500,000 | $1,250,000 |
| Total Partner Costs | $217,500 | $370,000 | $692,500 |
| **Net Partner Revenue** | -$67,500 | $130,000 | $557,500 |
| **ROI** | -31% | 35% | 80% |
| **Payback Period** | 17 months | 9 months | 7 months |

---

## Interactive ROI Calculator

Use this interactive calculator to model your own partner program. Enter your assumptions below:

<div class="roi-calculator">
  <div class="roi-inputs">
    <h3>📊 Your Assumptions</h3>
    
    <div class="input-group">
      <label>Active Partners (Year 1)</label>
      <input type="number" id="partners-y1" value="10" min="1" oninput="calculateROI()">
    </div>
    
    <div class="input-group">
      <label>Active Partners (Year 2)</label>
      <input type="number" id="partners-y2" value="25" min="1" oninput="calculateROI()">
    </div>
    
    <div class="input-group">
      <label>Active Partners (Year 3)</label>
      <input type="number" id="partners-y3" value="50" min="1" oninput="calculateROI()">
    </div>
    
    <div class="input-group">
      <label>Revenue per Partner ($)</label>
      <input type="number" id="revenue-per-partner" value="15000" min="0" step="1000" oninput="calculateROI()">
    </div>
    
    <div class="input-group">
      <label>Partner Manager Cost ($/year)</label>
      <input type="number" id="pm-cost" value="120000" min="0" step="10000" oninput="calculateROI()">
    </div>
    
    <div class="input-group">
      <label>Marketing Funds (% of revenue)</label>
      <input type="number" id="marketing-pct" value="20" min="0" max="100" oninput="calculateROI()">
      <span class="hint">% of partner revenue</span>
    </div>
    
    <div class="input-group">
      <label>Training Cost per Partner ($/year)</label>
      <input type="number" id="training-cost" value="2500" min="0" step="100" oninput="calculateROI()">
    </div>
    
    <div class="input-group">
      <label>Technology Cost ($/year)</label>
      <input type="number" id="tech-cost" value="20000" min="0" step="1000" oninput="calculateROI()">
    </div>
    
    <div class="input-group">
      <label>Commission Rate (%)</label>
      <input type="number" id="commission-pct" value="15" min="0" max="100" oninput="calculateROI()">
    </div>
    
    <div class="scenario-buttons">
      <button onclick="setScenario('conservative')" class="scenario-btn">📉 Conservative</button>
      <button onclick="setScenario('base')" class="scenario-btn active">📊 Base</button>
      <button onclick="setScenario('optimistic')" class="scenario-btn">📈 Optimistic</button>
    </div>
  </div>
  
  <div class="roi-results">
    <h3>📈 Your Results</h3>
    
    <div class="result-card roi-card">
      <div class="result-label">Overall ROI (3-Year)</div>
      <div class="result-value" id="overall-roi">149%</div>
    </div>
    
    <div class="result-card payback-card">
      <div class="result-label">Payback Period</div>
      <div class="result-value" id="payback-period">14 months</div>
    </div>
    
    <div class="result-card net-card">
      <div class="result-label">Net Revenue (3-Year)</div>
      <div class="result-value" id="net-revenue">$1,890,000</div>
    </div>
    
    <div class="results-table">
      <table>
        <thead>
          <tr>
            <th>Metric</th>
            <th>Year 1</th>
            <th>Year 2</th>
            <th>Year 3</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Revenue</td>
            <td id="rev-y1">$150,000</td>
            <td id="rev-y2">$375,000</td>
            <td id="rev-y3">$750,000</td>
          </tr>
          <tr>
            <td>Costs</td>
            <td id="cost-y1">$217,500</td>
            <td id="cost-y2">$370,000</td>
            <td id="cost-y3">$692,500</td>
          </tr>
          <tr class="highlight">
            <td><strong>Net</strong></td>
            <td id="net-y1"><strong>-$67,500</strong></td>
            <td id="net-y2"><strong>$5,000</strong></td>
            <td id="net-y3"><strong>$57,500</strong></td>
          </tr>
          <tr>
            <td>ROI</td>
            <td id="roi-y1">-31%</td>
            <td id="roi-y2">1%</td>
            <td id="roi-y3">8%</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="chart">
      <div class="chart-bar-group">
        <div class="chart-label">Y1</div>
        <div class="chart-bar-container">
          <div class="chart-bar revenue" id="bar-rev-y1" style="height: 20%"></div>
          <div class="chart-bar cost" id="bar-cost-y1" style="height: 29%"></div>
        </div>
      </div>
      <div class="chart-bar-group">
        <div class="chart-label">Y2</div>
        <div class="chart-bar-container">
          <div class="chart-bar revenue" id="bar-rev-y2" style="height: 50%"></div>
          <div class="chart-bar cost" id="bar-cost-y2" style="height: 49%"></div>
        </div>
      </div>
      <div class="chart-bar-group">
        <div class="chart-label">Y3</div>
        <div class="chart-bar-container">
          <div class="chart-bar revenue" id="bar-rev-y3" style="height: 100%"></div>
          <div class="chart-bar cost" id="bar-cost-y3" style="height: 92%"></div>
        </div>
      </div>
      <div class="chart-legend">
        <span class="legend-item"><span class="legend-color revenue"></span> Revenue</span>
        <span class="legend-item"><span class="legend-color cost"></span> Costs</span>
      </div>
    </div>
  </div>
</div>

<style>
.roi-calculator {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
  padding: 1.5rem;
  background: var(--sl-color-gray-6);
  border-radius: 0.5rem;
}

@media (max-width: 768px) {
  .roi-calculator {
    grid-template-columns: 1fr;
  }
}

.roi-inputs h3, .roi-results h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--sl-color-white);
}

.input-group {
  margin-bottom: 0.75rem;
}

.input-group label {
  display: block;
  font-size: 0.875rem;
  color: var(--sl-color-gray-3);
  margin-bottom: 0.25rem;
}

.input-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--sl-color-gray-5);
  border-radius: 0.25rem;
  background: var(--sl-color-gray-7);
  color: var(--sl-color-white);
  font-size: 1rem;
}

.input-group input:focus {
  outline: none;
  border-color: var(--sl-color-accent);
}

.input-group .hint {
  font-size: 0.75rem;
  color: var(--sl-color-gray-4);
}

.scenario-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.scenario-btn {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--sl-color-gray-5);
  border-radius: 0.25rem;
  background: var(--sl-color-gray-7);
  color: var(--sl-color-gray-3);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.scenario-btn:hover {
  border-color: var(--sl-color-accent);
}

.scenario-btn.active {
  background: var(--sl-color-accent-low);
  border-color: var(--sl-color-accent);
  color: var(--sl-color-white);
}

.result-card {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  text-align: center;
}

.roi-card {
  background: linear-gradient(135deg, #22c55e20, #16a34a20);
  border: 1px solid #22c55e40;
}

.payback-card {
  background: linear-gradient(135deg, #3b82f620, #2563eb20);
  border: 1px solid #3b82f640;
}

.net-card {
  background: linear-gradient(135deg, #a855f720, #7c3aed20);
  border: 1px solid #a855f740;
}

.result-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--sl-color-gray-3);
  margin-bottom: 0.25rem;
}

.result-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--sl-color-white);
}

.results-table {
  margin-top: 1rem;
  overflow-x: auto;
}

.results-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.results-table th,
.results-table td {
  padding: 0.5rem;
  text-align: right;
  border-bottom: 1px solid var(--sl-color-gray-6);
}

.results-table th:first-child,
.results-table td:first-child {
  text-align: left;
}

.results-table th {
  color: var(--sl-color-gray-3);
  font-weight: normal;
}

.results-table .highlight td {
  background: var(--sl-color-gray-6);
}

.chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 120px;
  margin-top: 1.5rem;
  padding: 1rem 0;
  border-top: 1px solid var(--sl-color-gray-6);
}

.chart-bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.chart-label {
  font-size: 0.75rem;
  color: var(--sl-color-gray-4);
  margin-bottom: 0.5rem;
}

.chart-bar-container {
  display: flex;
  gap: 4px;
  align-items: flex-end;
  height: 100px;
  width: 100%;
  justify-content: center;
}

.chart-bar {
  width: 20px;
  border-radius: 2px 2px 0 0;
  transition: height 0.3s ease;
}

.chart-bar.revenue {
  background: #22c55e;
}

.chart-bar.cost {
  background: #ef4444;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
  font-size: 0.75rem;
  color: var(--sl-color-gray-4);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-color.revenue {
  background: #22c55e;
}

.legend-color.cost {
  background: #ef4444;
}
</style>

<script>
function calculateROI() {
  const partnersY1 = parseInt(document.getElementById('partners-y1').value) || 0;
  const partnersY2 = parseInt(document.getElementById('partners-y2').value) || 0;
  const partnersY3 = parseInt(document.getElementById('partners-y3').value) || 0;
  const revenuePerPartner = parseInt(document.getElementById('revenue-per-partner').value) || 0;
  const pmCost = parseInt(document.getElementById('pm-cost').value) || 0;
  const marketingPct = parseInt(document.getElementById('marketing-pct').value) || 0;
  const trainingCost = parseInt(document.getElementById('training-cost').value) || 0;
  const techCost = parseInt(document.getElementById('tech-cost').value) || 0;
  const commissionPct = parseInt(document.getElementById('commission-pct').value) || 0;
  
  // Calculate revenue per year
  const revY1 = partnersY1 * revenuePerPartner;
  const revY2 = partnersY2 * revenuePerPartner;
  const revY3 = partnersY3 * revenuePerPartner;
  
  // Calculate costs per year
  const costY1 = pmCost + (revY1 * marketingPct / 100) + (partnersY1 * trainingCost) + techCost + (revY1 * commissionPct / 100);
  const costY2 = pmCost * 1.08 + (revY2 * marketingPct / 100) + (partnersY2 * trainingCost) + techCost * 1.1 + (revY2 * commissionPct / 100);
  const costY3 = pmCost * 1.17 + (revY3 * marketingPct / 100) + (partnersY3 * trainingCost) + techCost * 1.2 + (revY3 * commissionPct / 100);
  
  // Net revenue
  const netY1 = revY1 - costY1;
  const netY2 = revY2 - costY2;
  const netY3 = revY3 - costY3;
  
  // ROI per year
  const roiY1 = costY1 > 0 ? (revY1 - costY1) / costY1 * 100 : 0;
  const roiY2 = costY2 > 0 ? (revY2 - costY2) / costY2 * 100 : 0;
  const roiY3 = costY3 > 0 ? (revY3 - costY3) / costY3 * 100 : 0;
  
  // Overall 3-year ROI
  const totalRevenue = revY1 + revY2 + revY3;
  const totalCosts = costY1 + costY2 + costY3;
  const overallROI = totalCosts > 0 ? (totalRevenue - totalCosts) / totalCosts * 100 : 0;
  
  // Payback period (months to break-even)
  let paybackMonths = 0;
  let cumulativeNet = 0;
  const monthlyRevY1 = revY1 / 12;
  const monthlyCostY1 = costY1 / 12;
  for (let i = 1; i <= 36; i++) {
    const monthlyNet = (i <= 12 ? monthlyRevY1 : i <= 24 ? monthlyRevY2 / 12 : monthlyRevY3 / 12) - 
                      (i <= 12 ? monthlyCostY1 : i <= 24 ? costY2 / 12 : costY3 / 12);
    cumulativeNet += monthlyNet;
    if (cumulativeNet >= 0 && paybackMonths === 0) {
      paybackMonths = i;
    }
  }
  if (paybackMonths === 0) paybackMonths = "N/A";
  
  // Update UI
  document.getElementById('overall-roi').textContent = Math.round(overallROI) + '%';
  document.getElementById('overall-roi').style.color = overallROI >= 0 ? '#22c55e' : '#ef4444';
  
  document.getElementById('payback-period').textContent = typeof paybackMonths === 'number' ? paybackMonths + ' months' : 'N/A';
  
  const netRevenue = netY1 + netY2 + netY3;
  document.getElementById('net-revenue').textContent = '$' + netRevenue.toLocaleString();
  document.getElementById('net-revenue').style.color = netRevenue >= 0 ? '#22c55e' : '#ef4444';
  
  // Table
  document.getElementById('rev-y1').textContent = '$' + revY1.toLocaleString();
  document.getElementById('rev-y2').textContent = '$' + revY2.toLocaleString();
  document.getElementById('rev-y3').textContent = '$' + revY3.toLocaleString();
  
  document.getElementById('cost-y1').textContent = '$' + Math.round(costY1).toLocaleString();
  document.getElementById('cost-y2').textContent = '$' + Math.round(costY2).toLocaleString();
  document.getElementById('cost-y3').textContent = '$' + Math.round(costY3).toLocaleString();
  
  document.getElementById('net-y1').innerHTML = '<strong>' + (netY1 >= 0 ? '$' + Math.round(netY1).toLocaleString() : '-$' + Math.abs(Math.round(netY1)).toLocaleString()) + '</strong>';
  document.getElementById('net-y1').style.color = netY1 >= 0 ? '#22c55e' : '#ef4444';
  document.getElementById('net-y2').innerHTML = '<strong>' + (netY2 >= 0 ? '$' + Math.round(netY2).toLocaleString() : '-$' + Math.abs(Math.round(netY2)).toLocaleString()) + '</strong>';
  document.getElementById('net-y2').style.color = netY2 >= 0 ? '#22c55e' : '#ef4444';
  document.getElementById('net-y3').innerHTML = '<strong>' + (netY3 >= 0 ? '$' + Math.round(netY3).toLocaleString() : '-$' + Math.abs(Math.round(netY3)).toLocaleString()) + '</strong>';
  document.getElementById('net-y3').style.color = netY3 >= 0 ? '#22c55e' : '#ef4444';
  
  document.getElementById('roi-y1').textContent = Math.round(roiY1) + '%';
  document.getElementById('roi-y1').style.color = roiY1 >= 0 ? '#22c55e' : '#ef4444';
  document.getElementById('roi-y2').textContent = Math.round(roiY2) + '%';
  document.getElementById('roi-y2').style.color = roiY2 >= 0 ? '#22c55e' : '#ef4444';
  document.getElementById('roi-y3').textContent = Math.round(roiY3) + '%';
  document.getElementById('roi-y3').style.color = roiY3 >= 0 ? '#22c55e' : '#ef4444';
  
  // Chart
  const maxValue = Math.max(revY1, revY2, revY3, costY1, costY2, costY3);
  document.getElementById('bar-rev-y1').style.height = (revY1 / maxValue * 100) + '%';
  document.getElementById('bar-rev-y2').style.height = (revY2 / maxValue * 100) + '%';
  document.getElementById('bar-rev-y3').style.height = (revY3 / maxValue * 100) + '%';
  document.getElementById('bar-cost-y1').style.height = (costY1 / maxValue * 100) + '%';
  document.getElementById('bar-cost-y2').style.height = (costY2 / maxValue * 100) + '%';
  document.getElementById('bar-cost-y3').style.height = (costY3 / maxValue * 100) + '%';
}

function setScenario(scenario) {
  document.querySelectorAll('.scenario-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  
  if (scenario === 'conservative') {
    document.getElementById('partners-y1').value = 5;
    document.getElementById('partners-y2').value = 10;
    document.getElementById('partners-y3').value = 20;
    document.getElementById('revenue-per-partner').value = 10000;
    document.getElementById('marketing-pct').value = 15;
    document.getElementById('training-cost').value = 3000;
    document.getElementById('commission-pct').value = 10;
  } else if (scenario === 'base') {
    document.getElementById('partners-y1').value = 10;
    document.getElementById('partners-y2').value = 25;
    document.getElementById('partners-y3').value = 50;
    document.getElementById('revenue-per-partner').value = 15000;
    document.getElementById('marketing-pct').value = 20;
    document.getElementById('training-cost').value = 2500;
    document.getElementById('commission-pct').value = 15;
  } else if (scenario === 'optimistic') {
    document.getElementById('partners-y1').value = 20;
    document.getElementById('partners-y2').value = 50;
    document.getElementById('partners-y3').value = 100;
    document.getElementById('revenue-per-partner').value = 20000;
    document.getElementById('marketing-pct').value = 25;
    document.getElementById('training-cost').value = 2000;
    document.getElementById('commission-pct').value = 20;
  }
  
  calculateROI();
}

// Initial calculation
calculateROI();
</script>

---

## Scenario Analysis

Always present multiple scenarios. CFOs respect honesty about risk.

### Conservative Scenario (60% of base)

| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| Revenue | $90,000 | $300,000 | $750,000 |
| Costs | $217,500 | $370,000 | $692,500 |
| ROI | -59% | -19% | 8% |

### Base Case (100%)

| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| Revenue | $150,000 | $500,000 | $1,250,000 |
| Costs | $217,500 | $370,000 | $692,500 |
| ROI | -31% | 35% | 80% |

### Optimistic Scenario (140%)

| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| Revenue | $210,000 | $700,000 | $1,750,000 |
| Costs | $217,500 | $370,000 | $692,500 |
| ROI | -3% | 89% | 153% |

---

## Key Metrics to Track

Once approved, track these monthly to validate your model:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Partner Revenue per Active Partner | $20,000+ | Total partner revenue / # active |
| Cost to Serve per Partner | <$8,000 | Total program cost / # partners |
| Partner-Influenced Pipeline | 3x registered | CRM attribution |
| Time to First Partner Revenue | <90 days | First deal date - partner sign date |

---

## What I Wish I Knew

The biggest mistake? Overestimating revenue and underestimating costs. Be conservative—it's easier to exceed expectations than defend missed targets.

The second mistake? Not calculating payback period. CFOs don't just want ROI—they want to know when they'll get their money back. Aim for 18 months or less.

The third mistake? Ignoring partner churn. Assume 20% annual churn and build that into your model. Conservative assumptions build trust.

---

## Quick Win Checklist

Complete these first (30 minutes):

- [ ] Define your active partner count assumptions
- [ ] Estimate revenue per partner (conservative)
- [ ] List all program costs (including hidden ones)
- [ ] Calculate Year 1 ROI
- [ ] Identify your payback period

---

## Full Implementation

Complete for detailed analysis (1-2 hours):

- [ ] Build 3-year revenue model by partner tier
- [ ] Detail all cost categories with assumptions
- [ ] Create conservative/base/optimistic scenarios
- [ ] Calculate ROI, NPV, and payback period
- [ ] Document sensitivity analysis
- [ ] Identify key risk factors
- [ ] Prepare executive summary

---

## Executive Ready

For board presentations, include:

### The ROI Summary

- **Program Investment**: $1.28M over 3 years
- **Expected Return**: $1.9M net revenue
- **ROI**: 149%
- **Payback Period**: 14 months

### The Business Case

- Partners provide 3x pipeline coverage vs. direct sales
- CAC through partners is 40% lower than direct
- Every $1 in partner program generates $2.49 in revenue

### The Risk Mitigation

- Phased investment minimizes exposure
- 18-month payback provides early proof points
- Conservative assumptions validated by industry benchmarks

---

## Related Templates

- [Partner Business Case](../strategy/01-partner-business-case/) — Build the full business justification
- [Commission Structure](../finance/01-commission/) — Detailed commission calculations
- [Partner Program Charter](../strategy/09-partner-charter/) — Program governance and goals
- [Partner Health Scorecard](../analysis/01-health-scorecard/) — Ongoing performance tracking
