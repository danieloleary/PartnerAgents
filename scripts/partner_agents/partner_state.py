"""Partner state management."""

import json
import os
import html
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

PARTNERS_FILE = Path(__file__).resolve().parent / "partners.json"


def load_partners() -> List[Dict]:
    """Load partners from file."""
    if not PARTNERS_FILE.exists():
        return []
    try:
        with open(PARTNERS_FILE) as f:
            return json.load(f)
    except:
        return []


def save_partners(partners: List[Dict]):
    """Save partners to file."""
    with open(PARTNERS_FILE, "w") as f:
        json.dump(partners, f, indent=2)


def add_partner(
    name: str, tier: str = "Bronze", contact: str = "", email: str = ""
) -> Dict:
    """Add a new partner."""
    partners = load_partners()

    # Sanitize inputs
    name = html.escape(name.strip())[:100]
    email = html.escape(email.strip())[:100]
    contact = html.escape(contact.strip())[:100]
    tier = html.escape(tier.strip())[:50]

    # Check if exists
    for p in partners:
        if p["name"].lower() == name.lower():
            return p

    partner = {
        "id": f"partner-{len(partners) + 1}",
        "name": name,
        "tier": tier,
        "contact": contact,
        "email": email,
        "status": "Onboarding",
        "created_at": datetime.now().isoformat(),
        "deals": [],
        "campaigns": [],
        "notes": [],
    }

    partners.append(partner)
    save_partners(partners)
    return partner


def get_partner(name: str) -> Dict:
    """Get partner by name."""
    partners = load_partners()
    for p in partners:
        if p["name"].lower() == name.lower():
            return p
    return None


def list_partners() -> List[Dict]:
    """List all partners."""
    return load_partners()


def update_partner(name: str, updates: Dict) -> Dict:
    """Update partner details."""
    partners = load_partners()
    for p in partners:
        if p["name"].lower() == name.lower():
            p.update(updates)
            p["updated_at"] = datetime.now().isoformat()
            save_partners(partners)
            return p
    return None


def register_deal(partner_name: str, deal_value: int, account: str) -> Dict:
    """Register a deal for partner."""
    partners = load_partners()
    for p in partners:
        if p["name"].lower() == partner_name.lower():
            # Sanitize inputs
            account = html.escape(account.strip())[:100]

            deal = {
                "id": f"deal-{len(p.get('deals', [])) + 1}",
                "value": deal_value,
                "account": account,
                "status": "registered",
                "registered_at": datetime.now().isoformat(),
            }
            p.setdefault("deals", []).append(deal)
            p["updated_at"] = datetime.now().isoformat()
            save_partners(partners)
            return deal
    return None


def get_partner_stats(partners: List[Dict] = None) -> Dict:
    """Get overall partner stats."""
    if partners is None:
        partners = load_partners()
    tiers = {"Gold": 0, "Silver": 0, "Bronze": 0}
    total_deals = 0
    total_value = 0

    for p in partners:
        tier = p.get("tier", "Bronze")
        if tier in tiers:
            tiers[tier] += 1
        for deal in p.get("deals", []):
            total_deals += 1
            total_value += deal.get("value", 0)

    return {
        "total_partners": len(partners),
        "tiers": tiers,
        "total_deals": total_deals,
        "total_value": total_value,
    }


def delete_partner(name: str) -> bool:
    """Delete a partner by name."""
    partners = load_partners()
    original_len = len(partners)
    partners = [p for p in partners if p["name"].lower() != name.lower()]
    if len(partners) < original_len:
        save_partners(partners)
        return True
    return False
