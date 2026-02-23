"""Comprehensive tests for PartnerAgents agents."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def test_all_agents_import():
    """Test all agents can be imported."""
    from scripts.partner_agents.drivers import (
        DanAgent,
        ArchitectAgent,
        StrategistAgent,
        EngineAgent,
        SparkAgent,
        ChampionAgent,
        BuilderAgent,
    )

    assert DanAgent is not None
    assert ArchitectAgent is not None
    assert StrategistAgent is not None
    assert EngineAgent is not None
    assert SparkAgent is not None
    assert ChampionAgent is not None
    assert BuilderAgent is not None


def test_agent_personas():
    """Test all agents have valid personas."""
    from scripts.partner_agents.drivers import (
        DanAgent,
        ArchitectAgent,
        StrategistAgent,
        EngineAgent,
        SparkAgent,
        ChampionAgent,
        BuilderAgent,
    )

    agents = [
        DanAgent(),
        ArchitectAgent(),
        StrategistAgent(),
        EngineAgent(),
        SparkAgent(),
        ChampionAgent(),
        BuilderAgent(),
    ]

    for agent in agents:
        persona = agent.get_persona()
        assert "name" in persona
        assert "purpose" in persona
        assert "background_drop_in" in persona
        # Agent also has role attribute
        assert agent.role is not None


def test_agent_templates():
    """Test all agents have templates."""
    from scripts.partner_agents.drivers import (
        DanAgent,
        ArchitectAgent,
        StrategistAgent,
        EngineAgent,
        SparkAgent,
        ChampionAgent,
        BuilderAgent,
    )

    agents = [
        DanAgent(),
        ArchitectAgent(),
        StrategistAgent(),
        EngineAgent(),
        SparkAgent(),
        ChampionAgent(),
        BuilderAgent(),
    ]

    for agent in agents:
        templates = agent.get_templates()
        assert isinstance(templates, list)
        assert len(templates) > 0


def test_agent_skills():
    """Test all agents have skills registered."""
    from scripts.partner_agents.drivers import (
        DanAgent,
        ArchitectAgent,
        StrategistAgent,
        EngineAgent,
        SparkAgent,
        ChampionAgent,
        BuilderAgent,
    )

    expected_skills = {
        "DanAgent": 6,
        "ArchitectAgent": 6,
        "StrategistAgent": 5,
        "EngineAgent": 5,
        "SparkAgent": 5,
        "ChampionAgent": 5,
        "BuilderAgent": 4,
    }

    for agent_class, expected_count in expected_skills.items():
        agent = eval(f"{agent_class}()")
        assert len(agent.skills) == expected_count, (
            f"{agent_class} should have {expected_count} skills"
        )


def test_architect_onboard():
    """Test ARCHITECT onboard skill."""
    from scripts.partner_agents.drivers import ArchitectAgent

    agent = ArchitectAgent()
    result = agent.call_skill(
        "architect_onboard", {"partner_id": "test-corp", "tier": "Gold"}
    )

    assert result["tier"] == "Gold"
    assert "checklist" in result
    assert len(result["checklist"]) > 0


def test_architect_status():
    """Test ARCHITECT status skill."""
    from scripts.partner_agents.drivers import ArchitectAgent

    agent = ArchitectAgent()
    result = agent.call_skill("architect_status", {"partner_id": "test-corp"})

    assert "health_score" in result
    assert "tier" in result


def test_architect_qualify():
    """Test ARCHITECT qualify skill."""
    from scripts.partner_agents.drivers import ArchitectAgent

    agent = ArchitectAgent()
    result = agent.call_skill(
        "architect_qualify", {"prospect_data": {"company_name": "TestCorp"}}
    )

    assert "score" in result
    assert "rating" in result


def test_engine_register():
    """Test ENGINE register deal skill."""
    from scripts.partner_agents.drivers import EngineAgent

    agent = EngineAgent()
    result = agent.call_skill(
        "engine_register",
        {
            "partner_id": "test-corp",
            "deal_value": 50000,
            "account_name": "Test Account",
        },
    )

    assert "deal_id" in result
    assert result["status"] == "registered"


def test_engine_calculate():
    """Test ENGINE calculate commission skill."""
    from scripts.partner_agents.drivers import EngineAgent

    agent = EngineAgent()
    result = agent.call_skill(
        "engine_calculate", {"deal_id": "D1", "partner_tier": "Gold"}
    )

    assert "commission" in result
    assert "rate" in result


def test_engine_provision():
    """Test ENGINE portal provisioning skill."""
    from scripts.partner_agents.drivers import EngineAgent

    agent = EngineAgent()
    result = agent.call_skill(
        "engine_provision", {"partner_id": "test-corp", "tier": "Gold"}
    )

    assert result["access_granted"] is True


def test_engine_audit():
    """Test ENGINE compliance audit skill."""
    from scripts.partner_agents.drivers import EngineAgent

    agent = EngineAgent()
    result = agent.call_skill("engine_audit", {"partner_id": "test-corp"})

    assert "overall_status" in result


def test_spark_ignite():
    """Test SPARK campaign skill."""
    from scripts.partner_agents.drivers import SparkAgent

    agent = SparkAgent()
    result = agent.call_skill(
        "spark_ignite",
        {"campaign_name": "Test Campaign", "partner": "TestCorp", "type": "webinar"},
    )

    assert result["status"] == "launched"
    assert "campaign_id" in result


def test_spark_sequence():
    """Test SPARK email sequence skill."""
    from scripts.partner_agents.drivers import SparkAgent

    agent = SparkAgent()
    result = agent.call_skill(
        "spark_sequence",
        {"template": "welcome", "partner_name": "TestCorp", "goal": "onboarding"},
    )

    assert "emails" in result
    assert len(result["emails"]) > 0


def test_spark_deck():
    """Test SPARK deck creation skill."""
    from scripts.partner_agents.drivers import SparkAgent

    agent = SparkAgent()
    result = agent.call_skill(
        "spark_deck", {"partner": "TestCorp", "key_messages": ["message1", "message2"]}
    )

    assert "slides" in result


def test_spark_leads():
    """Test SPARK lead tracking skill."""
    from scripts.partner_agents.drivers import SparkAgent

    agent = SparkAgent()
    result = agent.call_skill("spark_leads", {"campaign_id": "C1"})

    assert "total_leads" in result
    assert "qualified" in result


def test_strategist_icp():
    """Test STRATEGIST ICP skill."""
    from scripts.partner_agents.drivers import StrategistAgent

    agent = StrategistAgent()
    result = agent.call_skill(
        "strategist_icp",
        {"company_attributes": ["SaaS"], "ideal_qualities": ["Enterprise"]},
    )

    assert "icp_name" in result
    assert "score_weights" in result


def test_strategist_tier():
    """Test STRATEGIST tier building skill."""
    from scripts.partner_agents.drivers import StrategistAgent

    agent = StrategistAgent()
    result = agent.call_skill("strategist_tier", {"tier_requirements": {}})

    assert "tiers" in result
    assert len(result["tiers"]) > 0


def test_strategist_comp():
    """Test STRATEGIST competitive analysis skill."""
    from scripts.partner_agents.drivers import StrategistAgent

    agent = StrategistAgent()
    result = agent.call_skill("strategist_comp", {"target_competitors": ["Comp1"]})

    assert "our_advantages" in result


def test_strategist_score():
    """Test STRATEGIST partner scoring skill."""
    from scripts.partner_agents.drivers import StrategistAgent

    agent = StrategistAgent()
    result = agent.call_skill(
        "strategist_score", {"partner_data": {"company_name": "TestCorp"}}
    )

    assert "overall_score" in result
    assert "recommendation" in result


def test_champion_board():
    """Test CHAMPION board deck skill."""
    from scripts.partner_agents.drivers import ChampionAgent

    agent = ChampionAgent()
    result = agent.call_skill("champion_board", {"time_period": "Q1", "metrics": {}})

    assert "deck_id" in result
    assert "slides" in result


def test_champion_roi():
    """Test CHAMPION ROI calculation skill."""
    from scripts.partner_agents.drivers import ChampionAgent

    agent = ChampionAgent()
    result = agent.call_skill(
        "champion_roi", {"costs": {"marketing": 10000}, "benefits": {"revenue": 50000}}
    )

    assert "roi_percentage" in result
    assert result["roi_percentage"] > 0


def test_champion_brief():
    """Test CHAMPION executive brief skill."""
    from scripts.partner_agents.drivers import ChampionAgent

    agent = ChampionAgent()
    result = agent.call_skill(
        "champion_brief", {"topic": "Test", "key_points": ["point1"]}
    )

    assert "summary" in result


def test_champion_budget():
    """Test CHAMPION budget skill."""
    from scripts.partner_agents.drivers import ChampionAgent

    agent = ChampionAgent()
    result = agent.call_skill(
        "champion_budget",
        {"current_spend": 10000, "requested_amount": 20000, "justification": "Growth"},
    )

    assert "requested" in result
    assert "ready_for_review" in result


def test_dan_decide():
    """Test DAN decision skill."""
    from scripts.partner_agents.drivers import DanAgent

    agent = DanAgent()
    result = agent.call_skill(
        "dan_decide", {"decision": "Approve partner", "stakeholders": ["CRO"]}
    )

    assert result["status"] == "final"


def test_dan_approve():
    """Test DAN approval skill."""
    from scripts.partner_agents.drivers import DanAgent

    agent = DanAgent()
    result = agent.call_skill("dan_approve", {"request": "New tier", "amount": 50000})

    assert result["status"] == "approved"


def test_dan_escalate():
    """Test DAN escalation skill."""
    from scripts.partner_agents.drivers import DanAgent

    agent = DanAgent()
    result = agent.call_skill(
        "dan_escalate", {"issue": "Critical bug", "urgency": "high"}
    )

    assert "ticket_id" in result
    assert "escalated_to" in result


def test_builder_integrate():
    """Test BUILDER integration skill."""
    from scripts.partner_agents.drivers import BuilderAgent

    agent = BuilderAgent()
    result = agent.call_skill(
        "builder_integrate", {"partner": "TestCorp", "integration_type": "api"}
    )

    assert result["status"] == "in_progress"


def test_builder_docs():
    """Test BUILDER docs generation skill."""
    from scripts.partner_agents.drivers import BuilderAgent

    agent = BuilderAgent()
    result = agent.call_skill(
        "builder_docs", {"api_spec": "openapi", "format": "markdown"}
    )

    assert "sections" in result


def test_builder_support():
    """Test BUILDER support skill."""
    from scripts.partner_agents.drivers import BuilderAgent

    agent = BuilderAgent()
    result = agent.call_skill(
        "builder_support", {"issue": "API error", "priority": "high"}
    )

    assert "ticket_id" in result


def test_orchestrator():
    """Test orchestrator coordination."""
    from scripts.partner_agents.drivers import ArchitectAgent, EngineAgent
    from scripts.partner_agents import Orchestrator

    orchestrator = Orchestrator()
    architect = ArchitectAgent()
    engine = EngineAgent()

    orchestrator.register_driver(architect)
    orchestrator.register_driver(engine)

    result = orchestrator.call_driver(
        "architect",
        "architect_onboard",
        {"partner_id": "test", "tier": "Gold"},
        from_driver="test",
    )

    assert result["agent"] == "architect"
    assert result["skill_used"] == "architect_onboard"


def test_team_stats():
    """Test total team statistics."""
    from scripts.partner_agents.drivers import (
        DanAgent,
        ArchitectAgent,
        StrategistAgent,
        EngineAgent,
        SparkAgent,
        ChampionAgent,
        BuilderAgent,
    )

    agents = [
        DanAgent(),
        ArchitectAgent(),
        StrategistAgent(),
        EngineAgent(),
        SparkAgent(),
        ChampionAgent(),
        BuilderAgent(),
    ]

    total_skills = sum(len(a.skills) for a in agents)
    total_templates = sum(len(a.get_templates()) for a in agents)

    assert total_skills == 36
    assert total_templates == 47


def test_all_skill_names_unique():
    """Test all skill names are unique across agents."""
    from scripts.partner_agents.drivers import (
        DanAgent,
        ArchitectAgent,
        StrategistAgent,
        EngineAgent,
        SparkAgent,
        ChampionAgent,
        BuilderAgent,
    )

    agents = [
        DanAgent(),
        ArchitectAgent(),
        StrategistAgent(),
        EngineAgent(),
        SparkAgent(),
        ChampionAgent(),
        BuilderAgent(),
    ]

    all_skills = []
    for agent in agents:
        for skill_name in agent.skills.keys():
            assert skill_name not in all_skills, f"Duplicate skill: {skill_name}"
            all_skills.append(skill_name)

    assert len(all_skills) > 30  # Should have 36 skills total
