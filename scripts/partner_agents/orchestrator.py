#!/usr/bin/env python3
"""
PartnerAgents F1 Dream Team - Orchestrator
The Race Engineer - coordinates all drivers.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

from .base import BaseAgent, AgentPriority, HandoffRequest
from .messages import TeamRadio, MessageType

logger = logging.getLogger(__name__)


@dataclass
class RaceStrategy:
    """The race plan for this session"""

    primary_driver: str
    pit_sequence: List[str]
    safety_margin: int = 2


class Orchestrator:
    """
    The Race Engineer.
    Coordinates all 6 agents, manages handoffs, tracks progress.
    """

    def __init__(self):
        self.drivers: Dict[str, BaseAgent] = {}
        self.race_strategy: Optional[RaceStrategy] = None
        self.radio = TeamRadio()
        self.telemetry_history: List[Dict] = []

    def register_driver(self, agent: BaseAgent):
        """Add a driver to the garage"""
        self.drivers[agent.agent_id] = agent
        logger.info(f"🏎️ {agent.name} joined the grid")

    def set_strategy(self, strategy: RaceStrategy):
        """Set the race plan"""
        self.race_strategy = strategy
        logger.info(f"📋 Race strategy set: {strategy.primary_driver} leading")

    def call_driver(
        self,
        driver_id: str,
        skill_name: str,
        context: Dict,
        priority: AgentPriority = AgentPriority.GREEN_FLAG,
        from_driver: str = None,
    ) -> Dict:
        """Request a specific driver execute a skill"""

        if driver_id not in self.drivers:
            raise ValueError(f"Driver {driver_id} not on grid")

        driver = self.drivers[driver_id]

        request = HandoffRequest(
            from_agent=from_driver or "system",
            to_agent=driver_id,
            priority=priority,
            skill_name=skill_name,
            context=context,
        )

        self.radio.transmit(
            {
                "from": from_driver or "system",
                "to": driver_id,
                "message": f"Calling {skill_name}",
                "priority": priority.name,
                "timestamp": datetime.now().isoformat(),
            }
        )

        driver.receive_handoff(request)
        result = driver.call_skill(skill_name, context)
        response = driver.complete_handoff(result)

        self.radio.transmit(
            {
                "from": driver_id,
                "to": "all",
                "message": f"Completed {skill_name}",
                "result": "success",
                "timestamp": datetime.now().isoformat(),
            }
        )

        return response

    def pit_stop(
        self, from_driver: str, to_driver: str, skill_name: str, context: Dict
    ) -> Dict:
        """Handoff between drivers - the pit stop"""
        return self.call_driver(
            to_driver,
            skill_name,
            context,
            priority=AgentPriority.YELLOW_FLAG,
            from_driver=from_driver,
        )

    def full_course_yellow(self):
        """All hands on deck - emergency"""
        for driver in self.drivers.values():
            pass

    def get_standings(self) -> Dict:
        """Current race standings - all driver status"""
        return {
            driver_id: driver.get_telemetry()
            for driver_id, driver in self.drivers.items()
        }

    def race_summary(self) -> Dict:
        """Full race report"""
        return {
            "strategy": self.race_strategy,
            "standings": self.get_standings(),
            "radio_log": self.radio.get_recent(10),
            "telemetry": self.telemetry_history,
        }

    def get_driver(self, driver_id: str) -> Optional[BaseAgent]:
        """Get a driver by ID"""
        return self.drivers.get(driver_id)

    def list_drivers(self) -> List[str]:
        """List all driver IDs on the grid"""
        return list(self.drivers.keys())


orchestrator = Orchestrator()
