#!/usr/bin/env python3
"""
Team Configuration - Customizable for YOUR company
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field
import yaml
from pathlib import Path


@dataclass
class DriverConfig:
    """Configuration for a single driver"""

    full_name: str = ""
    background: Dict[str, Any] = field(default_factory=dict)
    custom_fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TeamConfig:
    """Full team configuration"""

    team_name: str = "PartnerAgents Dream Team"
    season: str = "2026"
    drivers: Dict[str, DriverConfig] = field(default_factory=dict)

    strategy: Dict[str, Any] = field(
        default_factory=lambda: {
            "primary_driver": "max",
            "pit_sequence": ["max", "pitwall", "lando", "lewis", "race_control", "drs"],
        }
    )

    sla: Dict[str, int] = field(
        default_factory=lambda: {
            "red_flag": 15,
            "safety_car": 30,
            "virtual_safety": 60,
            "yellow_flag": 240,
            "green_flag": 1440,
        }
    )

    telemetry: Dict[str, Any] = field(
        default_factory=lambda: {
            "state_dir": "scripts/partner_agents/state",
            "log_retention_days": 90,
            "metrics_refresh_minutes": 15,
        }
    )

    @classmethod
    def load(
        cls, config_path: str = "scripts/partner_agents/config.yaml"
    ) -> "TeamConfig":
        """Load config from YAML file"""
        path = Path(config_path)
        if not path.exists():
            return cls()

        with open(path) as f:
            data = yaml.safe_load(f)

        config = cls()
        config.team_name = data.get("team_name", config.team_name)
        config.season = data.get("season", config.season)

        for driver_id, driver_data in data.get("drivers", {}).items():
            config.drivers[driver_id] = DriverConfig(
                full_name=driver_data.get("full_name", ""),
                background=driver_data.get("background", {}),
                custom_fields=driver_data.get("custom_fields", {}),
            )

        config.strategy = data.get("strategy", config.strategy)
        config.sla = data.get("sla", config.sla)
        config.telemetry = data.get("telemetry", config.telemetry)

        return config

    def save(self, config_path: str = "scripts/partner_agents/config.yaml"):
        """Save config to YAML file"""
        data = {
            "team_name": self.team_name,
            "season": self.season,
            "drivers": {
                driver_id: {
                    "full_name": d.full_name,
                    "background": d.background,
                    "custom_fields": d.custom_fields,
                }
                for driver_id, d in self.drivers.items()
            },
            "strategy": self.strategy,
            "sla": self.sla,
            "telemetry": self.telemetry,
        }

        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

    def customize_driver(
        self, driver_id: str, full_name: str, background: Dict[str, Any]
    ):
        """Customize a driver's background for your company"""
        if driver_id not in self.drivers:
            self.drivers[driver_id] = DriverConfig()

        self.drivers[driver_id].full_name = full_name
        self.drivers[driver_id].background = background


config = TeamConfig()
