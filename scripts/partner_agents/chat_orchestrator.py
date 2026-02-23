#!/usr/bin/env python3
"""
Chat Orchestrator - Main brain for the PartnerOS agent swarm
Handles conversation memory, agent coordination, and skill execution.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# Base directory
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MEMORY_DIR = REPO_ROOT / "partners" / ".memory"


@dataclass
class Message:
    """A single conversation message"""

    role: str  # "user" or "assistant"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    agent: str = ""  # Which agent responded
    skills_used: List[str] = field(default_factory=list)


@dataclass
class Conversation:
    """A conversation session with memory"""

    id: str
    created_at: str
    messages: List[Message] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)  # Current partner, etc.


class ConversationMemory:
    """Manages conversation history with disk persistence"""

    def __init__(self, memory_dir: Path = MEMORY_DIR):
        self.memory_dir = memory_dir
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.conversations: Dict[str, Conversation] = {}
        self._load_conversations()

    def _conversation_file(self, conv_id: str) -> Path:
        return self.memory_dir / f"{conv_id}.json"

    def _load_conversations(self):
        """Load all conversations from disk"""
        for f in self.memory_dir.glob("*.json"):
            try:
                with open(f, "r") as fp:
                    data = json.load(fp)
                    conv = Conversation(
                        id=data["id"],
                        created_at=data["created_at"],
                        messages=[Message(**m) for m in data.get("messages", [])],
                        context=data.get("context", {}),
                    )
                    self.conversations[conv.id] = conv
            except Exception:
                pass

    def _save_conversation(self, conv_id: str):
        """Save conversation to disk"""
        if conv_id not in self.conversations:
            return

        conv = self.conversations[conv_id]
        data = {
            "id": conv.id,
            "created_at": conv.created_at,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "agent": m.agent,
                    "skills_used": m.skills_used,
                }
                for m in conv.messages
            ],
            "context": conv.context,
        }

        with open(self._conversation_file(conv_id), "w") as fp:
            json.dump(data, fp, indent=2)

    def get_or_create(self, conv_id: str = "default") -> Conversation:
        """Get existing or create new conversation"""
        if conv_id not in self.conversations:
            self.conversations[conv_id] = Conversation(
                id=conv_id, created_at=datetime.now().isoformat()
            )
        return self.conversations[conv_id]

    def add_message(
        self,
        conv_id: str,
        role: str,
        content: str,
        agent: str = "",
        skills: List[str] = None,
    ):
        """Add a message to conversation"""
        conv = self.get_or_create(conv_id)
        conv.messages.append(
            Message(role=role, content=content, agent=agent, skills_used=skills or [])
        )
        self._save_conversation(conv_id)

    def get_history(self, conv_id: str = "default", limit: int = 20) -> List[Dict]:
        """Get conversation history"""
        conv = self.get_or_create(conv_id)
        return [
            {"role": m.role, "content": m.content, "agent": m.agent}
            for m in conv.messages[-limit:]
        ]

    def set_context(self, conv_id: str, key: str, value: Any):
        """Set conversation context (e.g., current_partner)"""
        conv = self.get_or_create(conv_id)
        conv.context[key] = value
        self._save_conversation(conv_id)

    def get_context(self, conv_id: str, key: str, default: Any = None) -> Any:
        """Get conversation context"""
        conv = self.get_or_create(conv_id)
        return conv.context.get(key, default)

    def clear(self, conv_id: str = "default"):
        """Clear conversation"""
        if conv_id in self.conversations:
            self.conversations[conv_id] = Conversation(
                id=conv_id, created_at=datetime.now().isoformat()
            )
            self._save_conversation(conv_id)


# Global memory instance
memory = ConversationMemory()


# Agent and skill registry
AGENT_SKILLS = {
    "architect": {
        "agent": "ARCHITECT",
        "role": "Partner Program Manager",
        "skills": {
            "architect_onboard": "Build activation path for new partner",
            "architect_status": "Quick status check on any partner",
            "architect_qbr": "Lock in a quarterly business review",
            "architect_qualify": "Assess if prospect is worth pursuing",
            "architect_log": "Record meeting notes or call",
            "architect_escalate": "Flag issue to leadership",
        },
    },
    "engine": {
        "agent": "ENGINE",
        "role": "Partner Operations",
        "skills": {
            "engine_register": "Process a deal registration",
            "engine_calculate": "Calculate commission for a deal",
            "engine_audit": "Check compliance status for partner",
            "engine_provision": "Set up portal access",
        },
    },
    "strategist": {
        "agent": "STRATEGIST",
        "role": "Partner Strategy",
        "skills": {
            "strategist_icp": "Define ideal partner profile",
            "strategist_tier": "Build tier structure",
            "strategist_comp": "Competitive analysis",
            "strategist_score": "Partner fit scoring",
        },
    },
    "spark": {
        "agent": "SPARK",
        "role": "Partner Marketing",
        "skills": {
            "spark_ignite": "Launch co-marketing campaign",
            "spark_sequence": "Write email outreach",
            "spark_deck": "Build sales pitch deck",
            "spark_leads": "Track leads from campaign",
        },
    },
    "champion": {
        "agent": "CHAMPION",
        "role": "Partner Leader",
        "skills": {
            "champion_board": "Build board presentation",
            "champion_roi": "Calculate program ROI",
            "champion_brief": "Create executive summary",
        },
    },
    "builder": {
        "agent": "BUILDER",
        "role": "Partner Technical",
        "skills": {
            "builder_integrate": "Build technical integration",
            "builder_docs": "Generate API documentation",
            "builder_support": "Technical support escalation",
        },
    },
    "dan": {
        "agent": "DAN",
        "role": "The Owner",
        "skills": {
            "dan_decide": "Make final decision on partner matters",
            "dan_approve": "Approve partner program changes",
            "dan_escalate": "Escalate to executive team",
        },
    },
}


def build_swarm_prompt(user_message: str, conv_id: str = "default") -> str:
    """Build the system prompt for the agent swarm"""

    # Get conversation context
    current_partner = memory.get_context(conv_id, "current_partner")
    partner_context = ""

    if current_partner:
        partner_context = f"""
CURRENT PARTNER: {current_partner}
"""

    # Get recent conversation
    history = memory.get_history(conv_id, limit=5)
    history_text = ""
    if history:
        history_text = "\nRECENT CONVERSATION:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else msg.get("agent", "Assistant")
            history_text += f"{role}: {msg['content'][:200]}...\n"

    skills_list = []
    for agent_id, agent_data in AGENT_SKILLS.items():
        for skill_name, skill_desc in agent_data["skills"].items():
            skills_list.append(f"- {agent_data['agent']}.{skill_name}: {skill_desc}")

    skills_text = "\n".join(skills_list[:15])  # Limit for prompt size

    prompt = f"""You are the PartnerOS Agent Swarm - a coordinated team of 7 specialized agents working together.

Your job is to understand what the user wants and orchestrate the right agents to get it done.

{partner_context}{history_text}

AVAILABLE AGENTS AND SKILLS:
{skills_text}

INSTRUCTIONS:
1. Understand what the user wants
2. If they mention a partner by name, acknowledge it and load their context
3. Choose the most relevant agent(s) and skill(s) to help
4. Execute the skill and return a helpful response
5. Tell the user which agent handled their request
6. If you need more info, ask clarifying questions

Response format:
- Be conversational and helpful
- Mention which agent is responding
- If creating documents, mention what was created
- If checking status, summarize what you found
- Always suggest next steps

Remember: You're a SWARM working together. Use multiple agents if needed!"""

    return prompt


def extract_partner_mentions(text: str) -> List[str]:
    """Extract partner names from user message"""
    # Simple pattern: look for capitalized words that might be company names
    # Skip common words
    skip_words = {
        "I",
        "We",
        "You",
        "What",
        "Who",
        "How",
        "When",
        "Where",
        "Why",
        "The",
        "A",
        "An",
        "This",
        "That",
        "These",
        "Those",
        "It",
        "Its",
        "Can",
        "Could",
        "Would",
        "Should",
        "Will",
        "Do",
        "Does",
        "Did",
        "Help",
        "Thanks",
        "Thank",
        "Please",
        "Next",
        "Now",
        "Then",
    }

    # Look for various patterns
    patterns = [
        r"for\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
        r"with\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
        r"to\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
        r"(?:onboard|status|check|help)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
    ]

    partners = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        partners.extend(matches)

    # Filter out common words
    partners = [p for p in partners if p not in skip_words]

    return partners


class ChatOrchestrator:
    """Main orchestrator for chat-based agent swarm"""

    def __init__(self):
        self.memory = memory
        self.partner_state = None

    async def chat(
        self, user_message: str, conv_id: str = "default", llm_client=None
    ) -> Dict[str, Any]:
        """Main chat interface - orchestrates the agent swarm"""

        # Save user message
        self.memory.add_message(conv_id, "user", user_message)

        # Extract partner mentions and update context
        partners = extract_partner_mentions(user_message)
        if partners:
            partner_name = partners[0]
            self.memory.set_context(conv_id, "current_partner", partner_name)

        # Build prompt
        system_prompt = build_swarm_prompt(user_message, conv_id)

        # Get history for LLM
        history = self.memory.get_history(conv_id, limit=10)

        # Call LLM
        response_text = ""
        agent_used = "swarm"

        if llm_client:
            response_text = await llm_client(system_prompt, user_message, history)
        else:
            # Fallback response
            response_text = self._fallback_response(user_message)

        # Save assistant response
        self.memory.add_message(conv_id, "assistant", response_text, agent=agent_used)

        return {
            "response": response_text,
            "agent": agent_used,
            "partners_detected": partners,
        }

    def _fallback_response(self, message: str) -> str:
        """Fallback when no LLM available"""
        msg = message.lower()
        partners = extract_partner_mentions(message)

        if "onboard" in msg or "onboard" in message:
            if partners:
                return f"""I'll help onboard {partners[0]}!

Here's what I'll do:

1. **ARCHITECT** is creating an onboarding checklist for {partners[0]}
2. **ENGINE** will set up their portal access
3. **SPARK** will create a welcome campaign

The onboarding plan includes:
- Day 1-2: Agreement review and signing
- Day 3-5: Portal setup and training
- Day 7: First check-in call

Would you like me to continue with any specific step?"""

        if "status" in msg or "next" in msg:
            if partners:
                return f"""Let me check on {partners[0]}... 

**Current Status for {partners[0]}:**
- Tier: (need to look up)
- Health: (need to look up)
- Last activity: (need to look up)

Would you like me to dig deeper into any of these?"""

        if "campaign" in msg or "launch" in msg:
            if partners:
                return f"""I'll launch a welcome campaign for {partners[0]}!

Here's what **SPARK** will create:
- Welcome email sequence (5 emails)
- Partner introduction deck
- Co-marketing one-pager
- Social media assets

Would you like me to start creating these?"""

        return """I'm here to help with your partner program! 

Try:
- "onboard [Partner Name]" - Start onboarding a new partner
- "status of [Partner Name]" - Check partner status and next steps
- "launch campaign for [Partner Name]" - Start a marketing campaign

What would you like to do?"""


# Convenience function
orchestrator = ChatOrchestrator()


async def chat(
    message: str, conv_id: str = "default", llm_client=None
) -> Dict[str, Any]:
    """Quick chat function"""
    return await orchestrator.chat(message, conv_id, llm_client)
