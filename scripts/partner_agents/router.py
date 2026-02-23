#!/usr/bin/env python3
"""
Router Agent - Intent detection and entity extraction for PartnerOS
Uses LLM to understand user requests and route to appropriate actions.

Detection patterns:
- onboard X -> action intent
- NDA/MSA/DPA for X -> document intent
- campaign for X -> action intent
- deal for X, $amount -> action intent

Fallback: Keyword-based routing when no LLM available
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Intent:
    """Represents a detected user intent"""

    type: str  # "document", "action", "question"
    name: str  # "nda", "msa", "dpa", "onboard", "campaign", "deal", "chat"
    agents: List[str]  # Which agents should handle this
    entities: Dict[str, Any]  # Extracted entities (partner_name, tier, amount, etc.)
    confidence: float  # 0.0-1.0 certainty of detection
    missing_fields: List[str]  # Required fields not provided by user


@dataclass
class RouterResult:
    """Result from the router"""

    intents: List[Intent]
    is_document_request: bool
    response: Optional[str]  # What to tell the user


# Template type to file mapping (MVP: just NDA)
TEMPLATE_MAP = {
    "nda": {
        "template": "legal/01-nda.md",
        "required_fields": ["partner_name"],
        "optional_fields": ["effective_date", "term_years"],
    },
    "msa": {
        "template": "legal/02-msa.md",
        "required_fields": ["partner_name"],
        "optional_fields": ["effective_date", "term_years", "services"],
    },
    "dpa": {
        "template": "legal/03-dpa.md",
        "required_fields": ["partner_name"],
        "optional_fields": ["effective_date", "jurisdiction"],
    },
}


def _build_router_prompt(
    user_message: str, context: Optional[Dict[str, Any]] = None
) -> str:
    """Build the prompt for intent detection."""

    partners_info = ""
    if context and context.get("partners"):
        partners_info = f"\n\nExisting partners: {', '.join([p['name'] for p in context['partners'][:10]])}"

    prompt = f"""You are the PartnerOS Router. Your job is to understand what the user wants.

User message: "{user_message}"{partners_info}

Available document types:
- nda: Mutual Non-Disclosure Agreement
- msa: Master Service Agreement  
- dpa: Data Processing Agreement

For each user request, analyze and return JSON with:
{{
    "intents": [
        {{
            "type": "document|action|question",
            "name": "nda|msa|dpa|onboard|recruit|qualify|qbr|chat",
            "entities": {{
                "partner_name": "extracted or null",
                "tier": "Gold|Silver|Bronze or null",
                "contact_name": "extracted or null",
                "email": "extracted or null",
                "effective_date": "YYYY-MM-DD or null",
                "term_years": "number or null"
            }},
            "confidence": 0.0-1.0,
            "missing_fields": ["list of required fields not provided"]
        }}
    ]
}}

Rules:
1. If user wants any document (NDA, MSA, DPA, agreement, contract), type = "document"
2. If user wants a plan, onboarding, recruitment, type = "action"  
3. If user is just asking a question, type = "question"
4. Be conservative - if unclear, set confidence < 0.7
5. partner_name: extract company names from the message (e.g., "Acme Corp" from "for Acme Corp")

Return ONLY valid JSON, no explanation."""

    return prompt


def _parse_llm_response(response: str) -> List[Intent]:
    """Parse the LLM response into Intent objects."""
    intents = []

    # Try to extract JSON from response
    try:
        # Find JSON block
        json_match = re.search(r"\{[\s\S]*\}", response)
        if json_match:
            data = json.loads(json_match.group(0))

            for intent_data in data.get("intents", []):
                intent = Intent(
                    type=intent_data.get("type", "question"),
                    name=intent_data.get("name", "chat"),
                    agents=_route_to_agents(intent_data.get("name", "chat")),
                    entities=intent_data.get("entities", {}),
                    confidence=float(intent_data.get("confidence", 0.5)),
                    missing_fields=intent_data.get("missing_fields", []),
                )
                intents.append(intent)
    except (json.JSONDecodeError, KeyError) as e:
        # If parsing fails, create a default chat intent
        intents.append(
            Intent(
                type="question",
                name="chat",
                agents=[],
                entities={},
                confidence=0.0,
                missing_fields=[],
            )
        )

    return intents


def _route_to_agents(intent_name: str) -> List[str]:
    """Map intent to appropriate agents."""
    agent_map = {
        "nda": ["engine"],
        "msa": ["engine"],
        "dpa": ["engine"],
        "onboard": ["architect"],
        "recruit": ["architect", "strategist"],
        "qualify": ["strategist"],
        "qbr": ["architect"],
    }
    return agent_map.get(intent_name, [])


def get_template_for_intent(intent_name: str) -> Optional[Dict]:
    """Get template info for an intent."""
    return TEMPLATE_MAP.get(intent_name)


class Router:
    """Main router class for intent detection."""

    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    async def route(
        self, user_message: str, context: Optional[Dict[str, Any]] = None
    ) -> RouterResult:
        """Route user message to appropriate action."""

        # Build prompt
        prompt = _build_router_prompt(user_message, context)

        # Call LLM (will be wired into web.py)
        if self.llm_client:
            response = await self.llm_client(prompt)
            intents = _parse_llm_response(response)
        else:
            # Fallback: simple keyword matching
            intents = self._fallback_route(user_message)

        # Check if this is a document or action request
        is_document = any(i.type in ("document", "action") for i in intents)

        # Build response
        if is_document:
            # Prefer document intents, fall back to action intents
            doc_intents = [i for i in intents if i.type == "document"]
            if doc_intents:
                doc = doc_intents[0]
                template_info = get_template_for_intent(doc.name)
                if template_info:
                    response = f"I'll create a {doc.name.upper()} for {doc.entities.get('partner_name', 'your partner')}."
                else:
                    response = f"I understand you want to create a {doc.name}, but I don't have a template for that yet."
            else:
                # It's an action (onboard, campaign, etc.)
                action = intents[0]
                response = f"I'll help you {action.name} for {action.entities.get('partner_name', 'your partner')}."
        else:
            response = ""  # Fall back to chat

        return RouterResult(
            intents=intents,
            is_document_request=is_document,
            response=response or "",
        )

    def _fallback_route(self, user_message: str) -> List[Intent]:
        """Simple keyword-based fallback routing."""
        msg = user_message.lower()
        intents = []

        # Check for document keywords
        doc_keywords = {
            "nda": ["nda", "non-disclosure", "confidentiality", "agreement"],
            "msa": ["msa", "master service", "service agreement"],
            "dpa": ["dpa", "data processing", "privacy"],
        }

        # Action keywords - these create partners with documents
        action_keywords = {
            "onboard": ["onboard", "onboarding", "on-board"],
            "recruit": ["recruit", "recruitment", "add partner"],
            "campaign": ["campaign", "launch campaign", "marketing"],
            "deal": ["deal", "register deal", "register a deal"],
        }

        # Helper to extract partner name
        def extract_partner(text):
            words = text.split()
            # First try with prepositions (for, with, to, of)
            for i, word in enumerate(words):
                if word.lower() in ["for", "with", "to", "of"]:
                    if i + 1 < len(words):
                        partner = " ".join(words[i + 1 :]).strip(".,!?")
                        partner = " ".join(partner.split()[:2])
                        if partner and partner[0].isupper():
                            return partner
            # Try: action verb is followed directly by partner name
            # e.g., "onboard TestCo" -> partner is after "onboard"
            action_words = ["onboard", "onboarding", "recruit", "add", "create"]
            for i, word in enumerate(words):
                word_lower = word.lower().rstrip("s")  # handle "onboards" -> "onboard"
                if word_lower in action_words:
                    if i + 1 < len(words):
                        partner = " ".join(words[i + 1 :]).strip(".,!?")
                        partner = " ".join(partner.split()[:2])
                        if partner and partner[0].isupper():
                            return partner
            return None

        # Check for document requests
        for doc_type, keywords in doc_keywords.items():
            if any(k in msg for k in keywords):
                partner_name = extract_partner(user_message)
                intents.append(
                    Intent(
                        type="document",
                        name=doc_type,
                        agents=["engine"],
                        entities={"partner_name": partner_name},
                        confidence=0.8,
                        missing_fields=["partner_name"] if not partner_name else [],
                    )
                )
                break

        # Check for action requests (create partner + generate docs)
        if not intents:
            for action, keywords in action_keywords.items():
                if any(k in msg for k in keywords):
                    partner_name = extract_partner(user_message)
                    intents.append(
                        Intent(
                            type="action",
                            name=action,
                            agents=["architect", "engine"],
                            entities={"partner_name": partner_name},
                            confidence=0.8,
                            missing_fields=["partner_name"] if not partner_name else [],
                        )
                    )
                    break

        if not intents:
            # Default to chat
            intents.append(
                Intent(
                    type="question",
                    name="chat",
                    agents=[],
                    entities={},
                    confidence=0.0,
                    missing_fields=[],
                )
            )

        return intents
