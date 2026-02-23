"""Partner state management."""

# TODO: Technical Debt - Divergent state management.
# This implementation uses a single partners.json file, while the CLI agent
# in scripts/partner_agent/ uses a directory-per-partner approach.
# These should be unified into a single persistence layer.

import json
import os
import html
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

PARTNERS_FILE = Path(__file__).resolve().parent / "partners.json"

# In-memory cache for performance
_partners_cache: Optional[List[Dict]] = None
_partners_by_name: Dict[str, Dict] = {}
_stats_cache: Optional[Dict] = None
_last_mtime: float = 0


def load_partners() -> List[Dict]:
    """Load partners from file with in-memory caching."""
    global _partners_cache, _last_mtime, _partners_by_name

    if not PARTNERS_FILE.exists():
        _partners_cache = []
        _partners_by_name = {}
        _last_mtime = 0
        return []

    try:
        mtime = os.path.getmtime(PARTNERS_FILE)
        if _partners_cache is not None and mtime <= _last_mtime:
            return _partners_cache

        with open(PARTNERS_FILE) as f:
            _partners_cache = json.load(f)
            _partners_by_name = {p["name"].lower(): p for p in _partners_cache}
            _last_mtime = mtime
            return _partners_cache
    except Exception:
        return _partners_cache if _partners_cache is not None else []


def save_partners(partners: List[Dict]):
    """Save partners to file and update cache."""
    global _partners_cache, _last_mtime, _stats_cache, _partners_by_name
    with open(PARTNERS_FILE, "w") as f:
        json.dump(partners, f, indent=2)
    _partners_cache = partners
    _partners_by_name = {p["name"].lower(): p for p in partners}
    _stats_cache = None  # Invalidate stats cache
    try:
        _last_mtime = os.path.getmtime(PARTNERS_FILE)
    except Exception:
        _last_mtime = 0


def add_partner(
    name: str, tier: str = "Bronze", contact: str = "", email: str = ""
) -> Dict:
    """Add a new partner."""
    partners = load_partners()

    # Ensure inputs are strings and sanitize
    name = html.escape(str(name).strip())[:100]
    email = html.escape(str(email).strip())[:100]
    contact = html.escape(str(contact).strip())[:100]
    tier = html.escape(str(tier).strip())[:50]

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
        "documents": [],
    }

    partners.append(partner)
    save_partners(partners)
    return partner


def get_partner(name: str) -> Dict:
    """Get partner by name (optimized with dict lookup)."""
    load_partners()
    return _partners_by_name.get(name.lower())


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
            # Ensure inputs are strings and sanitize
            account = html.escape(str(account).strip())[:100]
            try:
                deal_value = int(deal_value)
            except (ValueError, TypeError):
                deal_value = 0

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


def get_partner_stats() -> Dict:
    """Get overall partner stats with caching."""
    global _stats_cache

    # Reload partners if needed (handles external file changes)
    partners = load_partners()

    if _stats_cache is not None:
        return _stats_cache

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

    _stats_cache = {
        "total_partners": len(partners),
        "tiers": tiers,
        "total_deals": total_deals,
        "total_value": total_value,
    }
    return _stats_cache


def delete_partner(name: str) -> bool:
    """Delete a partner by name."""
    partners = load_partners()
    original_len = len(partners)
    partners = [p for p in partners if p["name"].lower() != name.lower()]
    if len(partners) < original_len:
        save_partners(partners)
        return True
    return False


def add_document(
    partner_name: str,
    doc_type: str,
    template: str,
    file_path: str,
    fields: Dict[str, Any] = None,
    status: str = "draft",
) -> Optional[Dict]:
    """Add a document to a partner's document list."""
    partners = load_partners()
    for p in partners:
        if p["name"].lower() == partner_name.lower():
            doc = {
                "id": f"doc-{len(p.get('documents', [])) + 1}",
                "type": doc_type,
                "template": template,
                "path": file_path,
                "status": status,
                "fields": fields or {},
                "created_at": datetime.now().isoformat(),
            }
            p.setdefault("documents", []).append(doc)
            p["updated_at"] = datetime.now().isoformat()
            save_partners(partners)
            return doc
    return None


def get_partner_documents(partner_name: str) -> List[Dict]:
    """Get all documents for a partner."""
    partner = get_partner(partner_name)
    if partner:
        return partner.get("documents", [])
    return []
