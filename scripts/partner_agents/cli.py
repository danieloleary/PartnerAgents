#!/usr/bin/env python3
"""
PartnerAgents CLI - Chat with the agent swarm from your terminal.

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

# Try to import readline for input history (arrow keys)
try:
    import readline

    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

# Try to import rich for pretty output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.markdown import Markdown

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Add scripts to path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from partner_agents import router, partner_state, document_generator

console = Console() if RICH_AVAILABLE else None


def print_banner():
    """Print a beautiful banner."""
    if RICH_AVAILABLE:
        banner = """
[bold cyan]██████╗ ███████╗████████╗██████╗  ██████╗ ██████╗  █████╗ ██████╗ ██████╗ 
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗
█████╔╝█████╗     ██║   ██████╔╝██║   ██║██████╔╝██║  ██║██████╔╝
██╔══██╗██╔══╝      ██║   ██╔══██╗██║   ██║██╔══██╗██║  ██║██╔══██╗
██║  ██║███████╗    ██║   ██║  ██║╚██████╔╝██║  ██║██║  ██║
╚═╝  ╚═╝╚══════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝[/bold cyan]

[bold white]PartnerAgents CLI[/bold white] — [italic]Tell the agent swarm what you need. Watch it happen.[/italic]
"""
        console.print(
            Panel.fit(banner.strip(), border_style="cyan", title="PartnerAgents")
        )
    else:
        print("=" * 50)
        print("PartnerAgents CLI - Chat with the agent swarm")
        print("=" * 50)


def print_help():
    """Print available commands."""
    if RICH_AVAILABLE:
        table = Table(
            title="Available Commands", show_header=True, header_style="bold magenta"
        )
        table.add_column("Command", style="cyan")
        table.add_column("Description", style="white")

        table.add_row("onboard [Partner]", "Onboard a new partner")
        table.add_row("status of [Partner]", "Check partner status")
        table.add_row("register deal for [Partner], $[amount]", "Register a deal")
        table.add_row("email to [Partner]", "Generate outreach email")
        table.add_row("qbr for [Partner]", "Schedule QBR")
        table.add_row("roi", "Show program ROI analysis")
        table.add_row("/help", "Show this help")
        table.add_row("quit/exit", "Exit")

        console.print(table)
    else:
        print("Commands:")
        print("  onboard [Partner]  - Onboard a new partner")
        print("  status of [Partner] - Check partner status")
        print("  email to [Partner] - Generate outreach email")
        print("  deal for [Partner], $[amount] - Register deal")
        print("  qbr for [Partner]  - Schedule QBR")
        print("  quit/exit          - Exit")


def print_response(response: dict):
    """Print the response nicely using rich."""
    if not response:
        return

    if RICH_AVAILABLE:
        if "response" in response:
            msg = response["response"]
            if "##" in msg or "**" in msg:
                console.print(Markdown(msg))
            else:
                console.print(
                    Panel.fit(msg.strip(), border_style="green", title="Response")
                )

        if response.get("agent"):
            console.print(f"[dim]Agent:[/dim] [bold]{response['agent']}[/bold]")
        if response.get("skill"):
            console.print(f"[dim]Skill:[/dim] [bold]{response['skill']}[/bold]")
    else:
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


def get_api_key(required: bool = False) -> str:
    """Get API key from env or prompt."""
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key and required:
        if RICH_AVAILABLE:
            console.print(
                "[yellow]Enter your OpenRouter API key (starts with sk-or-v1-):[/yellow]"
            )
            key = input().strip()
        else:
            key = input("Enter OpenRouter API key (starts with sk-or-v1-): ").strip()
    return key


def get_model() -> str:
    """Get model from env or use default."""
    return os.environ.get("OPENROUTER_MODEL", "qwen/qwen3.5-plus-02-15")


async def send_message(
    message: str, api_key: str, model: str, last_partner: str = None
) -> dict:
    """Send a message to the chat orchestrator.

    Args:
        message: The user's message
        api_key: OpenRouter API key
        model: Model to use
        last_partner: Previous partner name from conversation context
    """
    import httpx

    # Use the web.py chat handler logic
    sanitized = message.strip()

    # Build partner context for LLM
    partners = partner_state.list_partners()
    partner_info = ""
    if partners:
        partner_info = "\n\nCurrent Partners:\n"
        for p in partners:
            deals = p.get("deals", [])
            total = sum(d.get("value", 0) for d in deals)
            partner_info += f"- {p['name']} ({p.get('tier', 'Bronze')}, {p.get('status', 'Active')}, ${total:,} revenue)\n"

    # Route to document/action/skills if detected
    try:
        router_instance = router.Router()
        context = {"partners": partners}
        route_result = await router_instance.route(sanitized, context)

        # Check for document OR action/skills if detected
        if route_result.intents and (
            route_result.is_document_request
            or route_result.intents[0].type in ["action", "skill"]
        ):
            intent = route_result.intents[0]
            partner_name = intent.entities.get("partner_name")

            # Use conversation context if no partner specified
            skill_type = intent.entities.get("skill")
            if not partner_name and skill_type != "roi":
                # Try to use last_partner from context
                if last_partner:
                    partner_name = last_partner
                    intent.entities["partner_name"] = partner_name
                else:
                    return {
                        "response": "What's the partner company name?",
                        "agent": "system",
                        "needs_input": True,
                        "missing_field": "partner_name",
                    }

            # Create partner if doesn't exist (skip for roi)
            partner = None
            if partner_name:
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

            # Create partner if doesn't exist (skip for roi)
            partner = None
            if partner_name:
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

                print(
                    f"DEBUG: intent.name={intent.name}, amount={amount}, account={account}",
                    file=sys.stderr,
                )

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

            # Handle action types - create NDA by default (skip for skills)
            if intent.type == "action":
                doc_type = intent.name

                # Full onboarding: create NDA + MSA + DPA + checklist
                if intent.name == "onboard":
                    created_docs = []

                    # Create NDA, MSA, DPA
                    for doc in ["nda", "msa", "dpa"]:
                        doc_result = document_generator.create_document(
                            doc_type=doc,
                            partner_name=partner_name,
                            fields=intent.entities,
                        )
                        if doc_result:
                            partner_state.add_document(
                                partner_name=partner_name,
                                doc_type=doc,
                                template=doc_result["template"],
                                file_path=doc_result["path"],
                                fields=doc_result["fields"],
                                status="draft",
                            )
                            created_docs.append(doc.upper())

                    # Create onboarding checklist document
                    checklist_content = f"""# Onboarding Checklist for {partner_name}

## Week 1: Foundation
- [ ] Send welcome email
- [ ] Schedule kickoff call
- [ ] Share partner portal access
- [ ] Provide product training schedule

## Week 2-3: Technical Enablement
- [ ] Complete technical integration setup
- [ ] Test API connections
- [ ] Review documentation and resources
- [ ] Set up sandbox environment

## Week 4: Go-to-Market
- [ ] Finalize joint GTM plan
- [ ] Co-branded marketing materials
- [ ] Announce partnership (if applicable)
- [ ] First co-sell opportunity identified

## First 90 Days
- [ ] Complete certification (if applicable)
- [ ] First deal registered
- [ ] QBR scheduled
- [ ] Expansion opportunities identified
"""
                    # Save checklist
                    from pathlib import Path
                    import os
                    from datetime import datetime

                    slug = partner_name.lower().replace(" ", "-")
                    checklist_dir = Path(f"partners/{slug}/documents")
                    checklist_dir.mkdir(parents=True, exist_ok=True)
                    checklist_path = (
                        checklist_dir
                        / f"{datetime.now().strftime('%Y-%m-%d')}-onboarding-checklist.md"
                    )
                    checklist_path.write_text(checklist_content)

                    partner_state.add_document(
                        partner_name=partner_name,
                        doc_type="checklist",
                        template="recruitment/09-onboarding.md",
                        file_path=str(checklist_path),
                        fields={"partner_name": partner_name},
                        status="draft",
                    )
                    created_docs.append("CHECKLIST")

                    return {
                        "response": f"## Onboarded **{partner_name}**!\n\nCreated:\n"
                        + "\n".join([f"- {d}" for d in created_docs])
                        + f"\n\nPartner is now ready for enablement!",
                        "agent": "architect",
                        "onboarding": {
                            "partner": partner_name,
                            "documents": created_docs,
                        },
                    }

                # Single document creation for other actions
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
            elif intent.type == "skill":
                # Skip document creation for skills, handle directly below
                pass
            else:
                # For documents (nda, msa, dpa)
                doc_type = intent.name
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
                skill_name = intent.entities.get("skill") or intent.name.replace(
                    "skill_", ""
                )
                partner_name = intent.entities.get("partner_name")

                # Handle skills that don't need a partner (roi)
                if skill_name == "roi":
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

                # Skip if no partner name for skills that need it
                if not partner_name:
                    continue

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
                            "partner": partner["name"],
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
                        "partner": partner_name,
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
                        "partner": partner_name,
                    }

                elif skill_name == "commission":
                    partner = (
                        partner_state.get_partner(partner_name)
                        if partner_name
                        else None
                    )
                    total = 0
                    if partner:
                        deals = partner.get("deals", [])
                        total = sum(d.get("value", 0) for d in deals)

                    if total >= 500000:
                        rate = 0.20
                        tier_name = "Gold"
                    elif total >= 100000:
                        rate = 0.15
                        tier_name = "Silver"
                    else:
                        rate = 0.10
                        tier_name = "Bronze"

                    commission = total * rate

                    return {
                        "response": f"""## Commission Calculator for {partner_name}

Total Deal Value: ${total:,}
Partner Tier: {tier_name}
Commission Rate: {rate * 100}%

Total Commission: ${commission:,}

Tier Thresholds:
- Bronze: < $100K - 10%
- Silver: $100K-$500K - 15%
- Gold: > $500K - 20%""",
                        "agent": "engine",
                        "skill": "commission",
                        "partner": partner_name,
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
        import traceback

        if RICH_AVAILABLE:
            console.print(
                f"[bold red]Error:[/bold red] {str(e) or 'Something went wrong. Please try again.'}"
            )
        else:
            print(f"Error: {str(e) or 'Something went wrong. Please try again.'}")

        # Log full traceback to stderr for debugging
        traceback.print_exc()

        return {
            "response": "I encountered an error processing your request. Please try again or rephrase your message.",
            "agent": "system",
            "error": str(e),
        }

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

    # Fallback: use LLM for any unrecognized input
    system_prompt = f"""You are a helpful partner program management assistant for a B2B company.

You help users manage their partner program including:
- Onboarding new partners
- Checking partner status and health
- Registering deals and calculating commissions
- Generating outreach emails
- Scheduling QBRs (Quarterly Business Reviews)
- Analyzing program ROI

Partner Tiers:
- Bronze: < $100K revenue - 10% commission
- Silver: $100K-$500K - 15% commission  
- Gold: > $500K - 20% commission{partner_info}

Available commands the user can use:
- "onboard [Partner Name]" - Create new partner account
- "status [Partner Name]" - Check partner status
- "register deal for [Partner], $[amount]" - Record a deal
- "email [Partner]" - Generate outreach email
- "qbr [Partner]" - Get QBR scheduling info
- "commission [Partner]" - Calculate commission
- "roi" - Show ROI analysis

Be concise and helpful. If the user asks something outside of partner management, politely redirect to what you can help with."""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": sanitized},
                    ],
                },
                timeout=30.0,
            )
            if response.status_code == 200:
                result = response.json()
                choices = result.get("choices", [])
                if choices:
                    content = (
                        choices[0].get("message", {}).get("content", "No response")
                    )
                    return {
                        "response": content,
                        "agent": "ai_assistant",
                    }
            return {
                "response": f"AI Error: {response.status_code}",
                "agent": "system",
            }
    except Exception as e:
        return {
            "response": f"Error calling AI: {str(e)}",
            "agent": "system",
        }


def print_response(response: dict):
    """Print the response nicely."""
    if not response:
        print()
        print("=" * 50)
        print("No response")
        print("=" * 50)
        return

    if RICH_AVAILABLE:
        # Rich formatted output
        if response.get("response"):
            msg = response["response"]
            if "##" in msg or "**" in msg or "`" in msg:
                console.print(Markdown(msg))
            else:
                console.print(
                    Panel.fit(msg.strip(), border_style="green", title="Response")
                )

        if response.get("agent"):
            console.print(f"[dim]Agent:[/dim] [bold]{response['agent']}[/bold]")
        if response.get("skill"):
            console.print(f"[dim]Skill:[/dim] [bold]{response['skill']}[/bold]")
    else:
        # Plain text fallback
        print()
        print("=" * 50)
        if response.get("response"):
            print(response["response"])
        else:
            print(response)
        print("=" * 50)
        if response.get("agent"):
            print(f"Agent: {response['agent']}")
        if response.get("skill"):
            print(f"Skill: {response['skill']}")
        print()


# Slash commands - 20 common commands
SLASH_COMMANDS = {
    "help": ("Show all available commands", "Show this help message"),
    "clear": ("Clear the screen", "Clear all output from the terminal"),
    "partners": ("List all partners", "Show all partners in your program"),
    "status": ("Check partner status", "Usage: /status <partner_name>"),
    "onboard": ("Onboard a partner", "Usage: /onboard <partner_name>"),
    "deal": ("Register a deal", "Usage: /deal <partner>, $<amount>"),
    "email": ("Generate outreach email", "Usage: /email <partner_name>"),
    "qbr": ("Schedule QBR", "Usage: /qbr <partner_name>"),
    "commission": ("Calculate commission", "Usage: /commission <partner_name>"),
    "roi": ("Show ROI analysis", "Show program ROI metrics"),
    "model": ("Show/change model", "Usage: /model <model_name>"),
    "models": ("List available models", "Show all available AI models"),
    "api": ("API settings", "Show or set API key"),
    "history": ("Show conversation history", "Show previous messages in this session"),
    "export": ("Export conversation", "Usage: /export <filename>"),
    "quit": ("Exit the CLI", "Exit PartnerAgents"),
    "exit": ("Exit the CLI", "Exit PartnerAgents"),
    "source": ("Manage data sources", "Connect/disconnect data sources"),
    "think": ("Toggle thinking mode", "Show AI reasoning process"),
    "tokens": ("Show token usage", "Display token count for this session"),
}


async def handle_slash_command(
    command: str, console, api_key: str, model: str, last_partner: str
) -> dict:
    """Handle slash commands."""
    parts = command.strip().split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []

    response = {"response": "", "agent": "system"}

    if cmd == "help":
        table = Table(
            title="Slash Commands", show_header=True, header_style="bold magenta"
        )
        table.add_column("Command", style="cyan", width=15)
        table.add_column("Description", style="white")

        for name, (short, long_desc) in SLASH_COMMANDS.items():
            table.add_row(f"/{name}", short)

        if RICH_AVAILABLE:
            console.print(table)
        else:
            console.print("Available commands:")
            for name, (short, _) in SLASH_COMMANDS.items():
                console.print(f"  /{name} - {short}")
        response["response"] = "Use /help <command> for detailed info"

    elif cmd == "clear":
        if RICH_AVAILABLE:
            console.clear()
            console.print(print_banner())
        else:
            import os

            os.system("cls" if os.name == "nt" else "clear")
        response["response"] = "Screen cleared"

    elif cmd == "partners" or cmd == "partner":
        partners = partner_state.list_partners()
        if not partners:
            response["response"] = "No partners found. Use /onboard to add one."
        else:
            if RICH_AVAILABLE:
                table = Table(title="Partners", show_header=True)
                table.add_column("Name", style="cyan")
                table.add_column("Tier", style="yellow")
                table.add_column("Status", style="green")
                table.add_column("Revenue", style="magenta")

                for p in partners:
                    deals = p.get("deals", [])
                    total = sum(d.get("value", 0) for d in deals)
                    table.add_row(
                        p["name"],
                        p.get("tier", "Bronze"),
                        p.get("status", "Active"),
                        f"${total:,}",
                    )
                console.print(table)
            else:
                response["response"] = "Partners:\n" + "\n".join(
                    f"  - {p['name']} ({p.get('tier', 'Bronze')})" for p in partners
                )

    elif cmd == "status":
        if args:
            partner = partner_state.get_partner(args[0])
            if partner:
                deals = partner.get("deals", [])
                total = sum(d.get("value", 0) for d in deals)
                response["response"] = f"""## {partner["name"]}

- **Tier:** {partner.get("tier", "Bronze")}
- **Status:** {partner.get("status", "Active")}
- **Deals:** {len(deals)}
- **Revenue:** ${total:,}
- **Documents:** {len(partner.get("documents", []))}"""
            else:
                response["response"] = f"Partner '{args[0]}' not found."
        else:
            response["response"] = "Usage: /status <partner_name>"

    elif cmd == "onboard":
        if args:
            partner_name = " ".join(args)
            response = {
                "response": f"Onboarding {partner_name}...",
                "agent": "architect",
                "partner": partner_name,
            }
        else:
            response["response"] = "Usage: /onboard <partner_name>"

    elif cmd == "deal":
        if args:
            # Parse "partner, $amount"
            deal_text = " ".join(args)
            if "," in deal_text:
                parts = deal_text.split(",")
                partner_name = parts[0].strip()
                amount_str = parts[1].strip().replace("$", "").replace(",", "")
                try:
                    amount = int(amount_str)
                    response = {
                        "response": f"Registering deal for {partner_name}: ${amount:,}",
                        "agent": "architect",
                        "partner": partner_name,
                    }
                except:
                    response["response"] = (
                        "Invalid amount. Usage: /deal <partner>, $<amount>"
                    )
            else:
                response["response"] = "Usage: /deal <partner>, $<amount>"
        else:
            response["response"] = "Usage: /deal <partner>, $<amount>"

    elif cmd == "email":
        if args:
            partner_name = " ".join(args)
            partner = partner_state.get_partner(partner_name)
            tier = partner.get("tier", "Bronze") if partner else "Bronze"
            response["response"] = f"""## Outreach Email for {partner_name}

**Subject:** Partnership Opportunity

Hi [Partner Name],

I'd love to explore how we could collaborate. Our {tier} tier partnership offers:

- Lead sharing
- Technical support
- Competitive commissions

Would you be open to a 15-minute call?

Best regards"""
            response["partner"] = partner_name
        else:
            response["response"] = "Usage: /email <partner_name>"

    elif cmd == "qbr":
        if args:
            partner_name = " ".join(args)
            partner = partner_state.get_partner(partner_name)
            tier = partner.get("tier", "Bronze") if partner else "Bronze"

            schedule = {
                "Gold": "Quarterly",
                "Silver": "Bi-annually",
                "Bronze": "Annually",
            }
            response["response"] = f"""## QBR Schedule for {partner_name}

**Tier:** {tier}
**Recommended:** {schedule.get(tier, "Annually")}

**Topics to cover:**
1. Performance review
2. Pipeline update
3. Campaign results
4. Integration status
5. Goals for next period"""
            response["partner"] = partner_name
        else:
            response["response"] = "Usage: /qbr <partner_name>"

    elif cmd == "commission":
        if args:
            partner_name = " ".join(args)
            partner = partner_state.get_partner(partner_name)
            deals = partner.get("deals", []) if partner else []
            total = sum(d.get("value", 0) for d in deals)

            if total >= 500000:
                rate = 0.20
                tier_name = "Gold"
            elif total >= 100000:
                rate = 0.15
                tier_name = "Silver"
            else:
                rate = 0.10
                tier_name = "Bronze"

            commission = total * rate
            response["response"] = f"""## Commission for {partner_name}

**Total Deal Value:** ${total:,}
**Tier:** {tier_name}
**Rate:** {rate * 100}%

**Commission:** ${commission:,}

**Tier thresholds:**
- Bronze: < $100K → 10%
- Silver: $100K-$500K → 15%
- Gold: > $500K → 20%"""
            response["partner"] = partner_name
        else:
            response["response"] = "Usage: /commission <partner_name>"

    elif cmd == "roi":
        response["response"] = """## Program ROI

**Key Metrics:**
- Deal Pipeline
- Closed Revenue
- Partner-sourced Leads
- Co-marketing Campaign Results

Enter your values to calculate specific ROI."""

    elif cmd == "model":
        if args:
            response["response"] = f"Model changed to: {args[0]}"
        else:
            response["response"] = f"Current model: {model}\nUsage: /model <model_name>"

    elif cmd == "models":
        models = [
            ("qwen/qwen3.5-plus-02-15", "Default, fast"),
            ("anthropic/claude-3.5-sonnet", "Best quality"),
            ("google/gemini-2.0-flash", "Google's fastest"),
            ("openai/gpt-4o", "OpenAI's best"),
        ]
        if RICH_AVAILABLE:
            table = Table(title="Available Models")
            table.add_column("Model ID", style="cyan")
            table.add_column("Description", style="white")
            for m_id, desc in models:
                table.add_row(m_id, desc)
            console.print(table)
        else:
            response["response"] = "Models:\n" + "\n".join(
                f"  {m} - {d}" for m, d in models
            )

    elif cmd == "api":
        if args and args[0] == "show":
            response["response"] = (
                f"API key: {api_key[:10]}..." if api_key else "No API key set"
            )
        else:
            response["response"] = "Usage: /api show"

    elif cmd == "history":
        response["response"] = (
            "History feature coming soon - use arrow keys to navigate previous commands"
        )

    elif cmd == "export":
        response["response"] = (
            f"Export to {args[0] if args else 'file.json'} - coming soon"
        )

    elif cmd == "quit" or cmd == "exit":
        response["response"] = "__QUIT__"

    elif cmd == "source":
        response["response"] = """## Data Sources

Current sources:
- partners.json (local database)

Connect more sources:
- Salesforce
- HubSpot
- Slack"""

    elif cmd == "think":
        response["response"] = "Thinking mode: Shows AI reasoning - coming soon"

    elif cmd == "tokens":
        response["response"] = "Token tracking - coming soon"

    else:
        response["response"] = f"Unknown command: /{cmd}\nUse /help for all commands"

    return response


async def interactive_mode(api_key: str, model: str):
    """Run interactive chat mode."""
    if not api_key:
        api_key = get_api_key(required=True)

    print_banner()
    print_help()

    # Setup input history with readline
    if READLINE_AVAILABLE:
        histfile = Path.home() / ".partneragents" / "history"
        histfile.parent.mkdir(parents=True, exist_ok=True)
        try:
            readline.read_history_file(str(histfile))
            readline.set_history_length(1000)
        except (FileNotFoundError, PermissionError, OSError):
            pass

    # Setup tab completion for partners and commands
    if READLINE_AVAILABLE:
        # Command keywords for completion
        COMMAND_COMPLETIONS = [
            "onboard",
            "status",
            "email",
            "register deal",
            "qbr",
            "roi",
            "commission",
            "/help",
            "/partners",
            "quit",
            "exit",
        ]

        def get_completions(text, state):
            # Get partner names
            try:
                partners = partner_state.list_partners()
                partner_names = [p["name"] for p in partners]
            except:
                partner_names = []

            # Combine all completions
            all_completions = COMMAND_COMPLETIONS + partner_names
            matches = [c for c in all_completions if c.startswith(text.lower())]
            if state < len(matches):
                return matches[state]
            return None

        try:
            readline.set_completer(get_completions)
            readline.parse_and_bind("tab: complete")
        except:
            pass

    # Conversation context - partner name persists (never expires)
    last_partner = None
    pending_intent = None  # For clarification flow

    while True:
        try:
            if RICH_AVAILABLE:
                message = console.input("\n[bold cyan]>[/bold cyan] ").strip()
            else:
                message = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            # Save input history before exiting
            if READLINE_AVAILABLE:
                try:
                    readline.write_history_file(str(histfile))
                except:
                    pass
            if RICH_AVAILABLE:
                console.print("[yellow]Goodbye![/yellow]")
            else:
                print("\nGoodbye!")
            break

        if not message:
            continue

        # Basic input validation
        if len(message) > 1000:
            print_response(
                {
                    "response": "Your message is too long. Please keep it under 1000 characters.",
                    "agent": "system",
                }
            )
            continue

        # Handle slash commands
        if message.startswith("/"):
            slash_response = await handle_slash_command(
                message[1:], console, api_key, model, last_partner
            )
            # Check for quit
            if slash_response.get("response") == "__QUIT__":
                if READLINE_AVAILABLE:
                    try:
                        readline.write_history_file(str(histfile))
                    except:
                        pass
                if RICH_AVAILABLE:
                    console.print("[yellow]Goodbye![/yellow]")
                else:
                    print("Goodbye!")
                break
            print_response(slash_response)
            # Update last_partner from slash command response
            if slash_response.get("partner"):
                last_partner = slash_response["partner"]
            continue

        if message.lower() in ["quit", "exit", "q"]:
            # Save input history before exiting
            if READLINE_AVAILABLE:
                try:
                    readline.write_history_file(str(histfile))
                except:
                    pass
            if RICH_AVAILABLE:
                console.print("[yellow]Goodbye![/yellow]")
            else:
                print("Goodbye!")
            break

        if message.lower() == "/help":
            print_help()
            continue

        # Handle clarification - if we need partner name, use this input
        if pending_intent:
            message = f"{pending_intent} {message}"
            pending_intent = None

        response = await send_message(message, api_key, model, last_partner)
        print_response(response)

        # Extract partner from response to maintain context
        if response.get("partner"):
            last_partner = response["partner"]

        # Handle needs_input for clarification
        if response.get("needs_input"):
            # Ask for the missing field
            if RICH_AVAILABLE:
                partner_input = console.input(
                    "\n[bold yellow]Partner name:[/bold yellow] "
                ).strip()
            else:
                partner_input = input("\nPartner name: ").strip()

            if partner_input:
                # Re-send with partner name
                response = await send_message(message, api_key, model, last_partner)
                print_response(response)
                if response.get("partner"):
                    last_partner = response["partner"]
            pending_intent = None


async def one_shot_mode(message: str, api_key: str, model: str):
    """Run one-shot message mode."""
    response = await send_message(message, api_key, model)
    print_response(response)


def main():
    parser = argparse.ArgumentParser(
        description="PartnerAgents CLI - Chat with the agent swarm",
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
