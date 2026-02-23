#!/usr/bin/env python3
"""
Partner State Management Module

Unified state management for PartnerAgents - used by both CLI agent and Web UI.
Handles partner lifecycle tracking, milestones, and progress.

Usage:
    from partner_state import PartnerState

    state = PartnerState("acme-corp")
    state.add_milestone("Signed NDA")
    state.update_stage("recruiting")
    state.save()
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from enum import Enum


class PartnerStage(Enum):
    """Partner lifecycle stages."""

    PROSPECT = "prospect"
    RECRUITING = "recruiting"
    ONBOARDING = "onboarding"
    ENABLED = "enabled"
    GROWING = "growing"
    Strategic = "strategic"
    CHURNED = "churned"


class Milestone:
    """Represents a milestone in partner journey."""

    def __init__(self, name: str, description: str = "", playbook: str = ""):
        self.name = name
        self.description = description
        self.playbook = playbook
        self.completed_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "playbook": self.playbook,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Milestone":
        m = cls(
            data.get("name", ""), data.get("description", ""), data.get("playbook", "")
        )
        m.completed_at = data.get("completed_at", datetime.now().isoformat())
        return m


class Note:
    """Represents a note/observation about a partner."""

    def __init__(self, text: str, category: str = "general"):
        self.text = text
        self.category = category
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "category": self.category,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        n = cls(data.get("text", ""), data.get("category", "general"))
        n.created_at = data.get("created_at", datetime.now().isoformat())
        return n


class PartnerState:
    """
    Manages partner state throughout their lifecycle.

    Attributes:
        name: Partner company name
        slug: URL-safe identifier
        stage: Current lifecycle stage (prospect, recruiting, onboarding, etc.)
        tier: Partner tier (Bronze, Silver, Gold, Strategic)
        vertical: Industry vertical (SaaS, Healthcare, etc.)
        health_score: 0-100 health rating
        milestones: List of completed milestones
        notes: List of notes/observations
        playbooks: Track playbook progress
    """

    DEFAULT_STATE = {
        "name": "",
        "slug": "",
        "stage": "prospect",
        "tier": None,
        "vertical": None,
        "health_score": None,
        "rm": None,  # Relationship Manager
        "created": None,
        "updated": None,
        "milestones": [],
        "notes": [],
        "playbooks": {},
    }

    def __init__(self, partner_name: str, state_dir: str = "./state"):
        self.partner_name = partner_name
        self.state_dir = Path(state_dir)
        self.slug = self._slugify(partner_name)
        self.state = self._load()

    def _slugify(self, text: str) -> str:
        """Convert partner name to URL-safe slug."""
        import re

        text = text.strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "-", text)
        return text.lower().strip("-")

    def _load(self) -> dict:
        """Load state from disk or return default."""
        state_file = self.state_dir / self.slug / "metadata.json"

        if state_file.exists():
            with open(state_file) as f:
                state = json.load(f)
        else:
            state = self.DEFAULT_STATE.copy()

        # Set defaults for any missing fields
        state.setdefault("name", self.partner_name)
        state.setdefault("slug", self.slug)
        state.setdefault("stage", "prospect")
        state.setdefault("milestones", [])
        state.setdefault("notes", [])
        state.setdefault("playbooks", {})

        if not state.get("created"):
            state["created"] = datetime.now().isoformat()

        state["updated"] = datetime.now().isoformat()

        return state

    def save(self):
        """Save state to disk."""
        partner_dir = self.state_dir / self.slug
        partner_dir.mkdir(parents=True, exist_ok=True)

        self.state["updated"] = datetime.now().isoformat()

        state_file = partner_dir / "metadata.json"
        with open(state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def add_milestone(self, name: str, description: str = "", playbook: str = ""):
        """Record a milestone completion."""
        # Check if already completed
        for m in self.state.get("milestones", []):
            if m.get("name") == name:
                return  # Already recorded

        milestone = Milestone(name, description, playbook)
        self.state.setdefault("milestones", []).append(milestone.to_dict())

    def add_note(self, text: str, category: str = "general"):
        """Add a note about the partner."""
        note = Note(text, category)
        self.state.setdefault("notes", []).append(note.to_dict())

    def update_stage(self, stage: str):
        """Update the partner's lifecycle stage."""
        valid_stages = [s.value for s in PartnerStage]
        if stage not in valid_stages:
            raise ValueError(f"Invalid stage: {stage}. Must be one of: {valid_stages}")

        old_stage = self.state.get("stage")
        self.state["stage"] = stage

        # Auto-add milestone when stage changes
        if old_stage and old_stage != stage:
            self.add_milestone(
                f"Stage: {stage.title()}", f"Moved from {old_stage} to {stage}", ""
            )

    def set_tier(self, tier: str):
        """Set partner tier."""
        valid_tiers = ["Bronze", "Silver", "Gold", "Strategic"]
        if tier and tier not in valid_tiers:
            raise ValueError(f"Invalid tier: {tier}. Must be one of: {valid_tiers}")

        old_tier = self.state.get("tier")
        self.state["tier"] = tier

        # Auto-add milestone when tier changes
        if tier and old_tier != tier:
            self.add_milestone(
                f"Tier: {tier}",
                f"Promoted to {tier}"
                if not old_tier
                else f"Changed from {old_tier} to {tier}",
                "",
            )

    def record_playbook_start(self, playbook_name: str):
        """Record that a playbook has started."""
        if playbook_name not in self.state.get("playbooks", {}):
            self.state.setdefault("playbooks", {})[playbook_name] = {}

        self.state["playbooks"][playbook_name].update(
            {
                "started_at": datetime.now().isoformat(),
                "current_step": 0,
                "completed": False,
            }
        )

    def record_playbook_step(self, playbook_name: str, step: int):
        """Record current step in playbook."""
        self.state.setdefault("playbooks", {}).setdefault(playbook_name, {})[
            "current_step"
        ] = step

    def record_playbook_complete(self, playbook_name: str):
        """Record playbook completion and add milestone."""
        self.state.setdefault("playbooks", {}).setdefault(playbook_name, {}).update(
            {"completed": True, "completed_at": datetime.now().isoformat()}
        )

        # Add milestone
        playbook_names = {
            "recruit": "Recruitment Complete",
            "onboard": "Onboarding Complete",
            "qbr": "QBR Completed",
            "expand": "Expansion Started",
            "exit": "Partner Exited",
            "co-marketing": "Co-Marketing Complete",
            "support-escalation": "Support Escalation Resolved",
        }

        milestone_name = playbook_names.get(playbook_name, f"Playbook: {playbook_name}")
        self.add_milestone(
            milestone_name, f"Completed {playbook_name} playbook", playbook_name
        )

    def get_progress(self) -> dict:
        """Get overall progress summary."""
        total_milestones = len(self.state.get("milestones", []))
        completed_playbooks = sum(
            1 for p in self.state.get("playbooks", {}).values() if p.get("completed")
        )

        return {
            "partner": self.partner_name,
            "stage": self.state.get("stage"),
            "tier": self.state.get("tier"),
            "milestones": total_milestones,
            "playbooks_completed": completed_playbooks,
            "health_score": self.state.get("health_score"),
            "created": self.state.get("created"),
            "updated": self.state.get("updated"),
        }

    @classmethod
    def list_all(cls, state_dir: str = "./state") -> List[dict]:
        """List all partners and their states."""
        state_path = Path(state_dir)
        partners = []

        if state_path.exists():
            for partner_dir in state_path.iterdir():
                if partner_dir.is_dir():
                    meta_file = partner_dir / "metadata.json"
                    if meta_file.exists():
                        with open(meta_file) as f:
                            partners.append(json.load(f))

        return sorted(partners, key=lambda p: p.get("updated", ""), reverse=True)


def create_test_state():
    """Create a test state for testing."""
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()

    try:
        state = PartnerState("Test Corp", state_dir=temp_dir)
        state.add_milestone("Signed NDA", "Legal approved", "recruit")
        state.update_stage("recruiting")
        state.set_tier("Silver")
        state.record_playbook_start("recruit")
        state.save()

        # Verify
        loaded = PartnerState("Test Corp", state_dir=temp_dir)
        print(f"Created partner: {loaded.partner_name}")
        print(f"Stage: {loaded.state['stage']}")
        print(f"Tier: {loaded.state['tier']}")
        print(f"Milestones: {len(loaded.state['milestones'])}")

        return loaded

    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    create_test_state()
