#!/usr/bin/env python3
"""
PartnerAgents Multi-Agent Demo
Scenario: New Partner Onboarding

This demo shows how the 7-agent team collaborates to onboard a new partner.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from partner_agents.drivers import (
    DanAgent,
    ArchitectAgent,
    StrategistAgent,
    EngineAgent,
    SparkAgent,
    ChampionAgent,
    BuilderAgent,
)
from partner_agents import Orchestrator


def print_header(text):
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_step(agent_name, action, result):
    print(f"\n[{agent_name}] {action}")
    print(f"  → {result}")


def demo_new_partner_onboarding():
    """Demo: Onboard new partner 'Acme Corp' through the full team."""

    print_header("PARTNEROS MULTI-AGENT DEMO")
    print("Scenario: New Partner Onboarding")
    print("Partner: Acme Corp")
    print("Tier: Gold")

    # Initialize team
    print_header("INITIALIZING TEAM")

    agents = {
        "dan": DanAgent(),
        "architect": ArchitectAgent(),
        "strategist": StrategistAgent(),
        "engine": EngineAgent(),
        "spark": SparkAgent(),
        "champion": ChampionAgent(),
        "builder": BuilderAgent(),
    }

    print(f"✓ Loaded {len(agents)} agents")
    for name, agent in agents.items():
        p = agent.get_persona()
        print(f"  - {p['name']}: {agent.role} ({len(agent.skills)} skills)")

    # Initialize orchestrator
    orchestrator = Orchestrator()
    for name, agent in agents.items():
        orchestrator.register_driver(agent)

    print(f"✓ Orchestrator ready")

    # Step 1: STRATEGIST qualifies the prospect
    print_header("STEP 1: QUALIFY PROSPECT")

    result = orchestrator.call_driver(
        "strategist",
        "strategist_score",
        {
            "partner_data": {
                "company_name": "Acme Corp",
                "revenue": 5000000,
                "employees": 200,
            }
        },
        from_driver="system",
    )
    print_step(
        "STRATEGIST",
        "Evaluate partner fit",
        f"Score: {result['result']['overall_score']}/100 - {result['result']['recommendation']}",
    )

    # Step 2: ARCHITECT creates onboarding plan
    print_header("STEP 2: CREATE ONBOARDING PLAN")

    result = orchestrator.call_driver(
        "architect",
        "architect_onboard",
        {"partner_id": "acme-corp", "tier": "Gold"},
        from_driver="strategist",
    )
    checklist = result["result"]["checklist"]
    print_step(
        "ARCHITECT",
        "Create onboarding plan",
        f"{len(checklist)} items, {result['result']['timeline']}",
    )
    for item in checklist:
        print(f"    - {item['task']}: {item['status']}")

    # Step 3: SPARK launches welcome campaign
    print_header("STEP 3: LAUNCH WELCOME CAMPAIGN")

    result = orchestrator.call_driver(
        "spark",
        "spark_ignite",
        {
            "campaign_name": "Welcome Acme Corp",
            "partner": "Acme Corp",
            "type": "webinar",
        },
        from_driver="architect",
    )
    print_step(
        "SPARK",
        "Launch welcome campaign",
        f"Campaign: {result['result']['name']} - {result['result']['status']}",
    )

    # Step 4: SPARK writes outreach sequence
    print_header("STEP 4: OUTREACH SEQUENCE")

    result = orchestrator.call_driver(
        "spark",
        "spark_sequence",
        {"template": "welcome", "partner_name": "Acme Corp", "goal": "onboarding"},
        from_driver="architect",
    )
    print_step(
        "SPARK",
        "Write outreach sequence",
        f"{len(result['result']['emails'])} emails created",
    )

    # Step 5: ENGINE provisions portal access
    print_header("STEP 5: PROVISION PORTAL")

    result = orchestrator.call_driver(
        "engine",
        "engine_provision",
        {"partner_id": "acme-corp", "tier": "Gold"},
        from_driver="architect",
    )
    print_step(
        "ENGINE",
        "Provision portal access",
        f"Status: {result['result']['access_granted']}, URL sent",
    )

    # Step 6: ENGINE registers first deal
    print_header("STEP 6: REGISTER FIRST DEAL")

    result = orchestrator.call_driver(
        "engine",
        "engine_register",
        {
            "partner_id": "acme-corp",
            "deal_value": 150000,
            "account_name": "TechStartup Inc",
        },
        from_driver="architect",
    )
    print_step(
        "ENGINE",
        "Register deal",
        f"Deal ID: {result['result']['deal_id']}, Value: ${result['result']['value']:,}",
    )

    # Step 7: ENGINE calculates commission
    print_header("STEP 7: CALCULATE COMMISSION")

    result = orchestrator.call_driver(
        "engine",
        "engine_calculate",
        {"deal_id": result["result"]["deal_id"], "partner_tier": "Gold"},
        from_driver="engine",
    )
    print_step(
        "ENGINE",
        "Calculate commission",
        f"Rate: {result['result']['rate'] * 100}%, Commission: ${result['result']['commission']:,}",
    )

    # Step 8: CHAMPION creates board brief
    print_header("STEP 8: BOARD BRIEF")

    result = orchestrator.call_driver(
        "champion",
        "champion_brief",
        {
            "topic": "New Gold Partner: Acme Corp",
            "key_points": ["$150K deal", "Enterprise tier", "Integration planned"],
        },
        from_driver="engine",
    )
    print_step(
        "CHAMPION",
        "Create executive brief",
        f"Summary: {result['result']['summary'][:60]}...",
    )

    # Step 9: CHAMPION calculates ROI
    print_header("STEP 9: PROGRAM ROI")

    result = orchestrator.call_driver(
        "champion",
        "champion_roi",
        {
            "costs": {"marketing": 10000, "support": 5000},
            "benefits": {"revenue": 150000},
        },
        from_driver="champion",
    )
    print_step(
        "CHAMPION",
        "Calculate program ROI",
        f"ROI: {result['result']['roi_percentage']}%, Payback: {result['result']['payback_period_months']} months",
    )

    # Step 10: BUILDER starts integration
    print_header("STEP 10: TECHNICAL INTEGRATION")

    result = orchestrator.call_driver(
        "builder",
        "builder_integrate",
        {"partner": "Acme Corp", "integration_type": "api"},
        from_driver="architect",
    )
    print_step(
        "BUILDER",
        "Start technical integration",
        f"Type: {result['result']['integration_type']}, ETA: {result['result']['expected_completion']}",
    )

    # Step 11: BUILDER generates API docs
    print_header("STEP 11: API DOCUMENTATION")

    result = orchestrator.call_driver(
        "builder",
        "builder_docs",
        {"api_spec": "openapi", "format": "markdown"},
        from_driver="builder",
    )
    print_step(
        "BUILDER",
        "Generate API docs",
        f"Sections: {', '.join(result['result']['sections'])}",
    )

    # Step 12: DAN makes final decision
    print_header("STEP 12: DAN APPROVES")

    result = orchestrator.call_driver(
        "dan",
        "dan_decide",
        {
            "decision": "Approve Acme Corp as Gold partner",
            "stakeholders": ["CRO", "CTO"],
        },
        from_driver="champion",
    )
    print_step("DAN", "Final decision", f"Status: {result['result']['status'].upper()}")

    # Summary
    print_header("DEMO COMPLETE")
    print("✓ Partner qualified (STRATEGIST)")
    print("✓ Onboarding plan created (ARCHITECT)")
    print("✓ Welcome campaign launched (SPARK)")
    print("✓ Portal provisioned (ENGINE)")
    print("✓ First deal registered (ENGINE)")
    print("✓ Commission calculated (ENGINE)")
    print("✓ Executive brief created (CHAMPION)")
    print("✓ ROI calculated (CHAMPION)")
    print("✓ Integration started (BUILDER)")
    print("✓ API docs generated (BUILDER)")
    print("✓ Partnership approved (DAN)")
    print()
    print("🎉 Acme Corp is now a Gold partner!")


if __name__ == "__main__":
    demo_new_partner_onboarding()
