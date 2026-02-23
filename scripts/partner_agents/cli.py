#!/usr/bin/env python3
"""
PartnerOS CLI - Chat with the agent swarm from your terminal.

Usage:
    # Interactive mode
    python scripts/partner_agents/cli.py

    # One-shot mode
    python scripts/partner_agents/cli.py "onboard Acme Corp"
    python scripts/partner_agents/cli.py "status of Acme"
    python scripts/partner_agents/cli.py "register deal for Acme, $50k"

Environment:
    OPENROUTER_API_KEY - Your OpenRouter API key (optional, will prompt if missing)
    OPENROUTER_MODEL   - Model to use (default: qwen/qwen3.5-plus-02-15)
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Add scripts to path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from partner_agents import router, partner_state, document_generator


def get_api_key(required: bool = False) -> str:
    """Get API key from env or prompt."""
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key and required:
        key = input("Enter OpenRouter API key (starts with sk-or-v1-): ").strip()
    return key


def get_model() -> str:
    """Get model from env or use default."""
    return os.environ.get("OPENROUTER_MODEL", "qwen/qwen3.5-plus-02-15")


async def send_message(message: str, api_key: str, model: str) -> dict:
    """Send a message to the chat orchestrator."""
    from partner_agents import web

    # Use the web.py chat handler logic
    sanitized = message.strip()

    # Route to document/action generation if detected
    try:
        router_instance = router.Router()
        context = {"partners": partner_state.list_partners()}
        route_result = await router_instance.route(sanitized, context)

        # Check for document OR action requests
        if route_result.is_document_request and route_result.intents:
            intent = route_result.intents[0]
            partner_name = intent.entities.get("partner_name")

            if not partner_name:
                return {
                    "response": "What's the partner company name?",
                    "agent": "system",
                }

            # Create partner if doesn't exist
            partner = partner_state.get_partner(partner_name)
            if not partner:
                partner = partner_state.add_partner(
                    name=partner_name,
                    tier=intent.entities.get("tier", "Bronze"),
                )

            # Handle deal registration
            if intent.name == "deal":
                amount = intent.entities.get("amount", 0)
                account = intent.entities.get("account", partner_name)

                if isinstance(amount, str):
                    amount_str = (
                        amount.replace("$", "")
                        .replace(",", "")
                        .replace("k", "000")
                        .replace("K", "000")
                    )
                    try:
                        amount = int(float(amount_str))
                    except:
                        amount = 0

                deal = partner_state.register_deal(partner_name, amount, account)

                if deal:
                    return {
                        "response": f"Registered deal for **{partner_name}**!\n\nDeal Value: **${amount:,}**\nAccount: {account}\nStatus: {deal['status']}",
                        "agent": "engine",
                        "deal": {
                            "partner": partner_name,
                            "amount": amount,
                            "account": account,
                            "status": deal["status"],
                        },
                    }

            # Handle action types - create NDA by default
            doc_type = intent.name
            if intent.type == "action":
                doc_type = "nda"

            doc_result = document_generator.create_document(
                doc_type=doc_type,
                partner_name=partner_name,
                fields=intent.entities,
            )

            if doc_result:
                partner_state.add_document(
                    partner_name=partner_name,
                    doc_type=doc_type,
                    template=doc_result["template"],
                    file_path=doc_result["path"],
                    fields=doc_result["fields"],
                    status="draft",
                )

                return {
                    "response": f"Created **{doc_type.upper()}** for **{partner_name}**!\n\nSaved to: `{doc_result['relative_path']}`",
                    "agent": "engine",
                    "document": {
                        "type": doc_type,
                        "partner": partner_name,
                        "path": doc_result["relative_path"],
                    },
                }

        # Handle skill requests
        for intent in route_result.intents:
            if intent.type == "skill":
                skill_name = intent.entities.get("skill")
                partner_name = intent.entities.get("partner_name")

                if skill_name == "status":
                    partner = (
                        partner_state.get_partner(partner_name)
                        if partner_name
                        else None
                    )
                    if partner:
                        deals = partner.get("deals", [])
                        docs = partner.get("documents", [])
                        total_deal_value = sum(d.get("value", 0) for d in deals)

                        return {
                            "response": f"""## Partner Status: {partner["name"]}

Tier: {partner.get("tier", "Bronze")}
Status: {partner.get("status", "Active")}

Deals: {len(deals)}
Total Deal Value: ${total_deal_value:,}
Documents: {len(docs)}""",
                            "agent": "architect",
                            "skill": "status",
                        }

                elif skill_name == "email":
                    partner = (
                        partner_state.get_partner(partner_name)
                        if partner_name
                        else None
                    )
                    tier = partner.get("tier", "Bronze") if partner else "Bronze"

                    return {
                        "response": f"""## Outreach Email for {partner_name}

Subject: Partnership Opportunity

Hi [Partner Name],

I'd love to explore how we could collaborate. Our {tier} tier partnership offers lead sharing, technical support, and competitive commissions.

Would you be open to a 15-minute call?

Best regards""",
                        "agent": "spark",
                        "skill": "email",
                    }

                elif skill_name == "qbr":
                    return {
                        "response": f"""## QBR Scheduling for {partner_name}

Recommended Schedule:
- Gold: Quarterly
- Silver: Bi-annually  
- Bronze: Annually

Topics: Performance review, pipeline update, campaign results, integration status, goals.""",
                        "agent": "architect",
                        "skill": "qbr",
                    }

                elif skill_name == "roi":
                    return {
                        "response": """## Program ROI

Metrics to track:
- Deal Pipeline
- Closed Revenue
- Partner-sourced Leads
- Co-marketing Campaigns

Calculate your specific ROI by entering values above.""",
                        "agent": "champion",
                        "skill": "roi",
                    }

    except Exception as e:
        pass

    # Fallback: use LLM if API key provided
    if not api_key:
        return {
            "response": "Please configure your API key (set OPENROUTER_API_KEY env var or it will prompt you)",
            "agent": "system",
        }

    if len(api_key) < 20 or not api_key.startswith("sk-"):
        return {
            "response": "Invalid API key format. Key should start with 'sk-' and be at least 20 characters.",
            "agent": "system",
        }

    # Use simple response for now
    return {"response": f"I received your message: '{message}'", "agent": "swarm"}


def print_response(response: dict):
    """Print the response nicely."""
    print()
    print("=" * 50)
    if "response" in response:
        print(response["response"])
    else:
        print(response)
    print("=" * 50)
    if response.get("agent"):
        print(f"Agent: {response['agent']}")
    if response.get("skill"):
        print(f"Skill: {response['skill']}")
    print()


async def interactive_mode(api_key: str, model: str):
    """Run interactive chat mode."""
    # Prompt for API key if not available
    if not api_key:
        api_key = get_api_key(required=True)

    print("=" * 50)
    print("PartnerOS CLI - Chat with the agent swarm")
    print("=" * 50)
    print()
    print("Commands:")
    print("  onboard [Partner]  - Onboard a new partner")
    print("  status of [Partner] - Check partner status")
    print("  email to [Partner] - Generate outreach email")
    print("  deal for [Partner], $[amount] - Register deal")
    print("  qbr for [Partner]  - Schedule QBR")
    print("  quit/exit          - Exit")
    print()

    while True:
        try:
            message = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not message:
            continue

        if message.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        response = await send_message(message, api_key, model)
        print_response(response)


async def one_shot_mode(message: str, api_key: str, model: str):
    """Run one-shot message mode."""
    response = await send_message(message, api_key, model)
    print_response(response)


def main():
    parser = argparse.ArgumentParser(
        description="PartnerOS CLI - Chat with the agent swarm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Interactive mode
  %(prog)s "onboard Acme Corp"                # Onboard partner
  %(prog)s "status of Acme"                   # Check status
  %(prog)s "register deal for Acme, $50k"    # Register deal
  %(prog)s "email to Acme"                    # Generate email
        """,
    )
    parser.add_argument(
        "message",
        nargs="?",
        help="Message to send (if omitted, runs in interactive mode)",
    )
    parser.add_argument(
        "--model", default=get_model(), help=f"Model to use (default: {get_model()})"
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="OpenRouter API key (or set OPENROUTER_API_KEY env var)",
    )

    args = parser.parse_args()

    # Use env var, --api-key flag, or prompt (interactive only)
    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY", "").strip()
    model = args.model

    if args.message:
        # One-shot mode
        asyncio.run(one_shot_mode(args.message, api_key, model))
    else:
        # Interactive mode
        asyncio.run(interactive_mode(api_key, model))


if __name__ == "__main__":
    main()
