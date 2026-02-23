#!/usr/bin/env python3
"""
PartnerAgents F1 Dream Team - Base Agent
The chassis that all drivers inherit from.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AgentPriority(Enum):
    """Pit stop urgency levels"""

    RED_FLAG = 1
    SAFETY_CAR = 2
    VIRTUAL_SAFETY = 3
    YELLOW_FLAG = 4
    GREEN_FLAG = 5


class AgentStatus(Enum):
    """Driver status"""

    ON_TRACK = "racing"
    IN_PIT = "processing"
    IN_GARAGE = "idle"
    RETIRED = "done"


@dataclass
class AgentSkill:
    """A skill/capability this driver exposes"""

    name: str
    description: str
    priority: AgentPriority
    callback: Any
    requires_context: List[str] = field(default_factory=list)
    returns: str = "dict"


@dataclass
class HandoffRequest:
    """Request from another agent"""

    from_agent: str
    to_agent: str
    priority: AgentPriority
    skill_name: str
    context: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)


class BaseAgent(ABC):
    """
    The chassis - all agents inherit from this.
    Like the F1 car chassis: provides the foundation every driver needs.
    """

    def __init__(self, agent_id: str, name: str, role: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.status = AgentStatus.IN_GARAGE
        self.skills: Dict[str, AgentSkill] = {}
        self.telemetry: Dict[str, Any] = {}
        self.current_task: Optional[HandoffRequest] = None

    @abstractmethod
    def get_persona(self) -> Dict[str, Any]:
        """Return the driver profile - persona, background, purpose"""
        pass

    @abstractmethod
    def get_templates(self) -> List[str]:
        """List of templates this driver owns"""
        pass

    @abstractmethod
    def get_focus_areas(self) -> List[str]:
        """What does this driver focus on?"""
        pass

    def register_skill(self, skill: AgentSkill):
        """Register a skill other agents can call"""
        self.skills[skill.name] = skill
        logger.info(f"{self.name} registered skill: {skill.name}")

    def call_skill(self, skill_name: str, context: Dict) -> Any:
        """Execute a skill this agent owns"""
        if skill_name not in self.skills:
            raise ValueError(f"{self.name} doesn't have skill: {skill_name}")

        skill = self.skills[skill_name]
        self.status = AgentStatus.IN_PIT
        try:
            result = skill.callback(context)
            return result
        finally:
            self.status = AgentStatus.ON_TRACK

    def receive_handoff(self, request: HandoffRequest):
        """Handle incoming request from another agent"""
        self.current_task = request
        self.status = AgentStatus.IN_PIT
        logger.info(f"{self.name} received handoff: {request.skill_name}")

    def complete_handoff(self, result: Any) -> Dict:
        """Finish processing and return result"""
        response = {
            "agent": self.agent_id,
            "skill_used": self.current_task.skill_name,
            "result": result,
            "completed_at": datetime.now().isoformat(),
        }
        self.current_task = None
        self.status = AgentStatus.ON_TRACK
        return response

    def get_telemetry(self) -> Dict[str, Any]:
        """Return current driver stats"""
        return {
            "agent_id": self.agent_id,
            "status": self.status.value,
            "skills_count": len(self.skills),
            "telemetry": self.telemetry,
        }

    def update_telemetry(self, key: str, value: Any):
        """Update driver telemetry"""
        self.telemetry[key] = value
        self.telemetry["last_updated"] = datetime.now().isoformat()
