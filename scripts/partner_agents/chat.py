#!/usr/bin/env python3
"""
PartnerAgents CLI Chat Interface
A beautiful, interactive chat interface for the multi-agent partner team.
"""

import sys
from pathlib import Path
from datetime import datetime
import json

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt
from rich.box import ROUNDED
from rich import box

# Custom theme for gorgeous UI
custom_theme = Theme(
    {
        "info": "dim cyan",
        "warning": "yellow",
        "danger": "bold red",
        "agent": "bold cyan",
        "user": "bold green",
        "success": "bold green",
        "header": "bold magenta",
    }
)

console = Console(theme=custom_theme)

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


class PartnerAgentsChat:
    """Beautiful CLI chat interface for PartnerAgents."""

    def __init__(self):
        self.console = Console()
        self.agents = {}
        self.orchestrator = None
        self.session_history = []
        self.partner_context = {}

    def print_banner(self):
        """Print the PartnerAgents banner."""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ███████╗████████╗██████╗  ██████╗                 ║
║   ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗                ║
║   ██████╔╝█████╗     ██║   ██████╔╝██║   ██║                ║
║   ██╔══██╗██╔══╝     ██║   ██╔══██╗██║   ██║                ║
║   ██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝                ║
║   ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝                 ║
║                                                               ║
║          ██████╗  ██████╗  █████╗ ██████╗ ██████╗             ║
║         ██╔════╝ ██╔═══██╗██╔══██╗██╔══██╗██╔══██╗            ║
║         ██║  ███╗██║   ██║███████║██████╔╝██║  ██║            ║
║         ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║            ║
║         ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝            ║
║          ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        console.print(banner, style="header")
        console.print()
        console.print(
            "  [cyan]Your AI Partner Team[/cyan] — Type 'help' for commands",
            justify="center",
        )
        console.print()

    def initialize_agents(self):
        """Initialize all agents."""
        console.print("[dim]Initializing team...[/dim]")

        self.agents = {
            "dan": DanAgent(),
            "architect": ArchitectAgent(),
            "strategist": StrategistAgent(),
            "engine": EngineAgent(),
            "spark": SparkAgent(),
            "champion": ChampionAgent(),
            "builder": BuilderAgent(),
        }

        self.orchestrator = Orchestrator()
        for name, agent in self.agents.items():
            self.orchestrator.register_driver(agent)

        console.print("[success]✓[/success] [green]Team ready[/green]")
        self.print_team_status()

    def print_team_status(self):
        """Print team status table."""
        table = Table(title="[bold]Your Partner Team[/bold]", box=ROUNDED)
        table.add_column("Agent", style="cyan", no_wrap=True)
        table.add_column("Role", style="dim")
        table.add_column("Skills", justify="right", style="yellow")

        for name, agent in self.agents.items():
            p = agent.get_persona()
            table.add_row(p["name"], agent.role, str(len(agent.skills)))

        console.print(table)

    def print_welcome(self):
        """Print welcome message and suggestions."""
        panel = Panel(
            """[bold cyan]What would you like to do?[/bold cyan]

[green]Examples:[/green]
  • "Onboard Acme Corp as Gold partner"
  • "Register a deal for TechCorp, $50,000"
  • "Launch a welcome campaign for new partners"
  • "Create an ICP for enterprise SaaS companies"
  • "Calculate ROI for Q1"

[yellow]Commands:[/yellow]
  • [cyan]partners[/cyan] — List all partners
  • [cyan]skills[/cyan] — Show all available skills
  • [cyan]help[/cyan] — Show this message
  • [cyan]clear[/cyan] — Clear chat history
  • [cyan]exit[/cyan] — Quit
            """,
            title="[bold]Welcome to PartnerAgents[/bold]",
            box=ROUNDED,
            style="cyan",
        )
        console.print(panel)

    def process_message(self, message: str) -> str:
        """Process user message and route to appropriate agent."""
        message = message.strip().lower()

        # Command handling
        if message == "help":
            self.print_welcome()
            return ""
        elif message == "partners":
            self.show_partners()
            return ""
        elif message == "skills":
            self.show_skills()
            return ""
        elif message == "clear":
            self.session_history = []
            console.print("[dim]Chat history cleared[/dim]")
            return ""
        elif message in ["exit", "quit", "bye"]:
            console.print("[yellow]Goodbye! 👋[/yellow]")
            sys.exit(0)

        # Route to appropriate agent based on message content
        return self.route_message(message)

    def route_message(self, message: str) -> str:
        """Route message to the right agent(s)."""

        # Partner onboarding
        if any(x in message for x in ["onboard", "new partner", "add partner"]):
            return self.handle_onboarding(message)

        # Deal registration
        if any(x in message for x in ["deal", "register deal", "deal value"]):
            return self.handle_deal_registration(message)

        # Campaign
        if any(x in message for x in ["campaign", "marketing", "launch"]):
            return self.handle_campaign(message)

        # ICP / Strategy
        if any(x in message for x in ["icp", "ideal partner", "qualify", "evaluate"]):
            return self.handle_icp(message)

        # Commission / Financial
        if any(x in message for x in ["commission", "roi", "calculate"]):
            return self.handle_financial(message)

        # Integration / Technical
        if any(x in message for x in ["integration", "api", "technical"]):
            return self.handle_integration(message)

        # Executive / Board
        if any(x in message for x in ["board", "executive", "brief"]):
            return self.handle_executive(message)

        # Default - ask ARCHITECT (partner manager)
        return self.handle_default(message)

    def handle_onboarding(self, message: str) -> str:
        """Handle partner onboarding."""
        console.print()
        console.print(
            "[agent]ARCHITECT[/agent] Creating onboarding plan...", style="cyan"
        )

        # Extract partner name
        partner_name = self.extract_partner_name(message)
        tier = (
            "Gold"
            if "gold" in message
            else "Silver"
            if "silver" in message
            else "Bronze"
        )

        result = self.orchestrator.call_driver(
            "architect",
            "architect_onboard",
            {"partner_id": partner_name.lower().replace(" ", "-"), "tier": tier},
            from_driver="user",
        )

        checklist = result["result"]["checklist"]

        panel = Panel(
            f"""[bold cyan]Onboarding Plan Created[/bold cyan]

[green]Partner:[/green] {partner_name}
[green]Tier:[/green] {tier}
[green]Timeline:[/green] {result["result"]["timeline"]}

[bold]Checklist:[/bold]
"""
            + "\n".join([f"  ○ {item['task']}" for item in checklist]),
            title="[bold]✓ Partner Onboarded[/bold]",
            box=ROUNDED,
        )
        console.print(panel)

        # Suggest next actions
        self.print_suggestions(
            ["Register a deal for " + partner_name, "Launch a welcome campaign"]
        )
        return ""

    def handle_deal_registration(self, message: str) -> str:
        """Handle deal registration."""
        console.print()
        console.print("[agent]ENGINE[/agent] Registering deal...", style="cyan")

        # Extract details
        partner_name = self.extract_partner_name(message)
        deal_value = self.extract_deal_value(message)

        result = self.orchestrator.call_driver(
            "engine",
            "engine_register",
            {
                "partner_id": partner_name.lower().replace(" ", "-"),
                "deal_value": deal_value,
                "account_name": partner_name,
            },
            from_driver="user",
        )

        panel = Panel(
            f"""[bold cyan]Deal Registered[/bold cyan]

[green]Deal ID:[/green] {result["result"]["deal_id"]}
[green]Partner:[/green] {partner_name}
[green]Value:[/green] ${deal_value:,}
[green]Status:[/green] {result["result"]["status"].upper()}

[dim]Deal is now protected for 90 days.[/dim]
            """,
            title="[bold]✓ Deal Registered[/bold]",
            box=ROUNDED,
        )
        console.print(panel)

        self.print_suggestions(
            ["Calculate commission for this deal", "Register another deal"]
        )
        return ""

    def handle_campaign(self, message: str) -> str:
        """Handle marketing campaigns."""
        console.print()
        console.print("[agent]SPARK[/agent] Launching campaign...", style="cyan")

        partner_name = self.extract_partner_name(message)
        campaign_type = (
            "webinar"
            if "webinar" in message
            else "email"
            if "email" in message
            else "general"
        )

        result = self.orchestrator.call_driver(
            "spark",
            "spark_ignite",
            {
                "campaign_name": f"Campaign for {partner_name}",
                "partner": partner_name,
                "type": campaign_type,
            },
            from_driver="user",
        )

        panel = Panel(
            f"""[bold cyan]Campaign Launched[/bold cyan]

[green]Campaign:[/green] {result["result"]["name"]}
[green]Partner:[/green] {result["result"]["partner"]}
[green]Type:[/green] {result["result"]["type"]}
[green]Status:[/green] {result["result"]["status"].upper()}
            """,
            title="[bold]✓ Campaign Live[/bold]",
            box=ROUNDED,
        )
        console.print(panel)

        return ""

    def handle_icp(self, message: str) -> str:
        """Handle ICP creation."""
        console.print()
        console.print("[agent]STRATEGIST[/agent] Creating ICP...", style="cyan")

        result = self.orchestrator.call_driver(
            "strategist",
            "strategist_icp",
            {
                "company_attributes": ["Enterprise", "SaaS"],
                "ideal_qualities": ["Technical fit", "Market alignment"],
            },
            from_driver="user",
        )

        weights = result["result"]["score_weights"]

        panel = Panel(
            f"""[bold cyan]Ideal Partner Profile Created[/bold cyan]

[green]ICP Name:[/green] {result["result"]["icp_name"]}

[bold]Scoring Weights:[/bold]
{chr(10).join([f"  • {k}: {v * 100:.0f}%" for k, v in weights.items()])}
            """,
            title="[bold]✓ ICP Defined[/bold]",
            box=ROUNDED,
        )
        console.print(panel)

        return ""

    def handle_financial(self, message: str) -> str:
        """Handle financial calculations."""
        console.print()
        console.print("[agent]CHAMPION[/agent] Calculating...", style="cyan")

        result = self.orchestrator.call_driver(
            "champion",
            "champion_roi",
            {
                "costs": {"marketing": 10000, "support": 5000},
                "benefits": {"revenue": 50000},
            },
            from_driver="user",
        )

        panel = Panel(
            f"""[bold cyan]ROI Analysis[/bold cyan]

[green]Total Costs:[/green] ${result["result"]["total_costs"]:,}
[green]Total Benefits:[/green] ${result["result"]["total_benefits"]:,}
[green]ROI:[/green] {result["result"]["roi_percentage"]}%
[green]Payback:[/green] {result["result"]["payback_period_months"]} months
            """,
            title="[bold]✓ Calculated[/bold]",
            box=ROUNDED,
        )
        console.print(panel)

        return ""

    def handle_integration(self, message: str) -> str:
        """Handle technical integration."""
        console.print()
        console.print("[agent]BUILDER[/agent] Starting integration...", style="cyan")

        partner_name = self.extract_partner_name(message)

        result = self.orchestrator.call_driver(
            "builder",
            "builder_integrate",
            {"partner": partner_name, "integration_type": "api"},
            from_driver="user",
        )

        panel = Panel(
            f"""[bold cyan]Integration Started[/bold cyan]

[green]Partner:[/green] {result["result"]["partner"]}
[green]Type:[/green] {result["result"]["integration_type"]}
[green]ETA:[/green] {result["result"]["expected_completion"]}
            """,
            title="[bold]✓ Integration In Progress[/bold]",
            box=ROUNDED,
        )
        console.print(panel)

        return ""

    def handle_executive(self, message: str) -> str:
        """Handle executive communications."""
        console.print()
        console.print(
            "[agent]CHAMPION[/agent] Creating executive brief...", style="cyan"
        )

        result = self.orchestrator.call_driver(
            "champion",
            "champion_brief",
            {
                "topic": "Partner Program Update",
                "key_points": ["New partnerships", "Pipeline growth", "Q1 wins"],
            },
            from_driver="user",
        )

        panel = Panel(
            f"""[bold cyan]Executive Brief Created[/bold cyan]

[green]Topic:[/green] {result["result"]["topic"]}
[green]Summary:[/green] {result["result"]["summary"]}
[green]For:[/green] {result["result"]["for"]}
            """,
            title="[bold]✓ Brief Ready[/bold]",
            box=ROUNDED,
        )
        console.print(panel)

        return ""

    def handle_default(self, message: str) -> str:
        """Default handler."""
        console.print()
        console.print("[agent]ARCHITECT[/agent] Let me help with that...", style="cyan")

        panel = Panel(
            """[yellow]I can help you with:[/yellow]

[green]• Partner Management[/green]
  "Onboard Acme Corp as Gold"
  "List all our partners"
  
[green]• Deals & Revenue[/green]
  "Register a deal for TechCorp, $50,000"
  "Calculate commission for this deal"
  
[green]• Marketing[/green]
  "Launch a campaign for new partners"
  "Create outreach sequence for Acme"
  
[green]• Strategy[/green]
  "Create an ICP for enterprise"
  "Evaluate TechCorp as a partner"
  
[green]• Executive[/green]
  "Create a board deck"
  "Brief executives on partner program"

[dim]Or type 'skills' to see all available actions.[/dim]
            """,
            title="[bold]How Can I Help?[/bold]",
            box=ROUNDED,
        )
        console.print(panel)

        return ""

    def extract_partner_name(self, message: str) -> str:
        """Extract partner name from message."""
        words = message.split()
        # Look for company patterns
        for i, word in enumerate(words):
            if word.lower() in ["for", "partner", "company"] and i + 1 < len(words):
                return words[i + 1].title()
        # Default
        return "Partner"

    def extract_deal_value(self, message: str) -> int:
        """Extract deal value from message."""
        import re

        numbers = re.findall(r"\$?(\d+(?:,\d{3})*(?:\.\d+)?)", message)
        if numbers:
            return int(numbers[0].replace(",", ""))
        return 10000  # Default

    def show_partners(self):
        """Show partners list."""
        panel = Panel(
            """[bold cyan]Partners[/bold cyan]

[yellow]Demo Partners:[/yellow]
  • Acme Corp (Gold) - Active
  • TechCorp (Silver) - Active  
  • StartupXYZ (Bronze) - Onboarding
  • Enterprise Inc (Gold) - Active

[dim]Use 'onboard [name] as [tier]' to add a new partner.[/dim]
            """,
            title="[bold]Partner List[/bold]",
            box=ROUNDED,
        )
        console.print(panel)

    def show_skills(self):
        """Show all available skills."""
        table = Table(title="[bold]Available Skills[/bold]", box=ROUNDED)
        table.add_column("Agent", style="cyan")
        table.add_column("Skill", style="white")
        table.add_column("Description", style="dim")

        for name, agent in self.agents.items():
            p = agent.get_persona()
            for skill_name, skill in agent.skills.items():
                table.add_row(p["name"], skill_name, skill.description)

        console.print(table)

    def print_suggestions(self, suggestions: list):
        """Print action suggestions."""
        if not suggestions:
            return
        console.print()
        console.print("[dim]Suggested actions:[/dim]")
        for s in suggestions:
            console.print(f"  [cyan]→[/cyan] [link]{s}[/link]")

    def chat_loop(self):
        """Main chat loop."""
        self.print_banner()
        self.initialize_agents()
        self.print_welcome()

        while True:
            try:
                user_input = Prompt.ask("[bold green]You[/bold green]", console=console)

                if user_input.strip():
                    self.process_message(user_input)

            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")


def main():
    """Main entry point."""
    chat = PartnerAgentsChat()
    chat.chat_loop()


if __name__ == "__main__":
    main()
