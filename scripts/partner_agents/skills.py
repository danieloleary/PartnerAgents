#!/usr/bin/env python3
"""
Shared skill handlers for PartnerOS.

This module provides skill response generation for both CLI and Web UI.
Keeps skill logic in one place (DRY principle).
"""

from typing import Dict, Any, Optional


def get_partner_status(partner_name: str, partner: Optional[Dict]) -> str:
    """Generate partner status response."""
    if not partner:
        return f"Partner '{partner_name}' not found."

    deals = partner.get("deals", [])
    docs = partner.get("documents", [])
    total_deal_value = sum(d.get("value", 0) for d in deals)

    return f"""## Partner Status: {partner["name"]}

Tier: {partner.get("tier", "Bronze")}
Status: {partner.get("status", "Active")}
Created: {partner.get("created_at", "Unknown")}

Deals: {len(deals)}
Total Deal Value: ${total_deal_value:,}
Documents: {len(docs)}"""


def get_email_template(partner_name: str, tier: str = "Bronze") -> str:
    """Generate outreach email template."""
    return f"""## Outreach Email for {partner_name}

Subject: Partnership Opportunity

Hi [Partner Name],

I'd love to explore how we could collaborate. Our {tier} tier partnership offers lead sharing, technical support, and competitive commissions.

Would you be open to a 15-minute call?

Best regards"""


def get_commission_calc(partner_name: str, total_deals: int = 0) -> str:
    """Generate commission calculation."""
    # Commission tiers
    if total_deals >= 500000:
        rate = 0.20
        tier_name = "Gold"
    elif total_deals >= 100000:
        rate = 0.15
        tier_name = "Silver"
    else:
        rate = 0.10
        tier_name = "Bronze"

    commission = total_deals * rate

    return f"""## Commission Calculator for {partner_name}

Total Deal Value: ${total_deals:,}
Partner Tier: {tier_name}
Commission Rate: {rate * 100}%

Total Commission: ${commission:,}

Tier Thresholds:
- Bronze: < $100K - 10%
- Silver: $100K-$500K - 15%
- Gold: > $500K - 20%"""


def get_qbr_info(partner_name: str) -> str:
    """Generate QBR scheduling info."""
    return f"""## QBR Scheduling for {partner_name}

Recommended Schedule:
- Gold partners: Quarterly
- Silver partners: Bi-annually
- Bronze partners: Annually

Topics:
1. Partnership performance review
2. Deal pipeline update
3. Marketing campaign results
4. Technical integration status
5. Goals for next period"""


def get_roi_info(partner_name: Optional[str] = None) -> str:
    """Generate ROI information."""
    name = partner_name if partner_name else "your program"
    return f"""## Program ROI for {name}

Metrics to track:
- Deal Pipeline
- Closed Revenue
- Partner-sourced Leads
- Co-marketing Campaigns

Calculate your specific ROI by entering values above."""


def handle_skill(
    skill_name: str, partner_name: Optional[str], partner: Optional[Dict]
) -> Dict[str, Any]:
    """Handle a skill request and return response.

    Args:
        skill_name: Name of the skill (status, email, commission, qbr, roi)
        partner_name: Name of the partner company
        partner: Partner dict from partner_state (if found)

    Returns:
        Dict with response, agent, and skill keys
    """
    if skill_name == "status":
        return {
            "response": get_partner_status(partner_name, partner),
            "agent": "architect",
            "skill": "status",
        }

    elif skill_name == "email":
        tier = partner.get("tier", "Bronze") if partner else "Bronze"
        return {
            "response": get_email_template(partner_name, tier),
            "agent": "spark",
            "skill": "email",
        }

    elif skill_name == "commission":
        total = 0
        if partner:
            deals = partner.get("deals", [])
            total = sum(d.get("value", 0) for d in deals)
        return {
            "response": get_commission_calc(partner_name, total),
            "agent": "engine",
            "skill": "commission",
        }

    elif skill_name == "qbr":
        return {
            "response": get_qbr_info(partner_name),
            "agent": "architect",
            "skill": "qbr",
        }

    elif skill_name == "roi":
        return {
            "response": get_roi_info(partner_name),
            "agent": "champion",
            "skill": "roi",
        }

    # Default fallback
    return {
        "response": f"Skill '{skill_name}' not recognized.",
        "agent": "system",
        "skill": skill_name,
    }
