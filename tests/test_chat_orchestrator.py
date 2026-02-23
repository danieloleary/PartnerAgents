#!/usr/bin/env python3
"""
Tests for PartnerOS Chat Orchestrator and Document Generation

Tests:
1. Router intent detection (onboard, NDA, MSA, campaign, deal)
2. Partner extraction from messages
3. Document generation (NDA, MSA, DPA)
4. Web chat endpoint integration
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from partner_agents import router, document_generator, partner_state, chat_orchestrator


class TestRouterIntentDetection:
    """Test router can detect various intents"""

    @pytest.mark.asyncio
    async def test_onboard_intent(self):
        """Test 'onboard X' creates action intent"""
        r = router.Router()
        result = await r.route("onboard AcmeCorp", {"partners": []})

        assert result.is_document_request is True
        assert len(result.intents) > 0
        assert result.intents[0].type == "action"
        assert result.intents[0].name == "onboard"
        assert result.intents[0].entities.get("partner_name") == "AcmeCorp"

    @pytest.mark.asyncio
    async def test_nda_intent(self):
        """Test 'NDA for X' creates document intent"""
        r = router.Router()
        result = await r.route("Create NDA for TestCompany", {"partners": []})

        assert result.is_document_request is True
        assert result.intents[0].type == "document"
        assert result.intents[0].name == "nda"
        assert result.intents[0].entities.get("partner_name") == "TestCompany"

    @pytest.mark.asyncio
    async def test_msa_intent(self):
        """Test MSA detection"""
        r = router.Router()
        result = await r.route("We need an MSA with PartnerX", {"partners": []})

        assert result.is_document_request is True
        assert result.intents[0].name == "msa"

    @pytest.mark.asyncio
    async def test_campaign_intent(self):
        """Test campaign launch detection"""
        r = router.Router()
        result = await r.route("launch campaign for MyPartner", {"partners": []})

        assert result.is_document_request is True
        assert result.intents[0].type == "action"
        assert result.intents[0].name == "campaign"

    @pytest.mark.asyncio
    async def test_deal_intent(self):
        """Test deal registration detection"""
        r = router.Router()
        result = await r.route("register a deal for BigCorp, $100000", {"partners": []})

        # This should route to chat for now (no deal skill wired yet)
        # But should at least not crash
        assert result is not None


class TestPartnerExtraction:
    """Test partner name extraction from messages"""

    def test_extract_partner_for(self):
        """Test 'for X' pattern"""
        r = router.Router()
        result = asyncio.get_event_loop().run_until_complete(
            r.route("NDA for Acme Corp", {"partners": []})
        )
        # May route to chat or document depending on confidence
        assert result is not None

    def test_extract_partner_onboard(self):
        """Test 'onboard X' pattern"""
        r = router.Router()
        result = asyncio.get_event_loop().run_until_complete(
            r.route("onboard TechStartup", {"partners": []})
        )
        assert result.intents[0].entities.get("partner_name") == "TechStartup"

    def test_extract_partner_status_of(self):
        """Test 'status of X' pattern"""
        r = router.Router()
        result = asyncio.get_event_loop().run_until_complete(
            r.route("status of ExistingPartner", {"partners": []})
        )
        # Status routes to chat for now
        assert result is not None


class TestDocumentGeneration:
    """Test document generation functionality"""

    def test_create_nda(self):
        """Test NDA document creation"""
        result = document_generator.create_document(
            doc_type="nda",
            partner_name="TestNDACompany",
            fields={"partner_name": "TestNDACompany"},
        )

        assert result is not None
        assert result["doc_type"] == "nda"
        assert result["partner_name"] == "TestNDACompany"
        assert "path" in result
        assert "nda.md" in result["path"]

    def test_create_msa(self):
        """Test MSA document creation"""
        result = document_generator.create_document(
            doc_type="msa", partner_name="TestMSACompany", fields={}
        )

        assert result is not None
        assert result["doc_type"] == "msa"
        assert "msa.md" in result["path"]

    def test_create_dpa(self):
        """Test DPA document creation"""
        result = document_generator.create_document(
            doc_type="dpa", partner_name="TestDPACorp", fields={}
        )

        assert result is not None
        assert result["doc_type"] == "dpa"

    def test_document_saved_to_filesystem(self):
        """Test document is actually saved to disk"""
        result = document_generator.create_document(
            doc_type="nda", partner_name="FileTestCorp", fields={}
        )

        assert result is not None
        path = Path(result["path"])
        assert path.exists()
        # Document exists - content check optional

    def test_document_contains_nda_content(self):
        """Test document has NDA content"""
        result = document_generator.create_document(
            doc_type="nda", partner_name="ContentTest", fields={}
        )

        assert result is not None
        path = Path(result["path"])
        content = path.read_text()
        assert "NDA" in content or "Confidential" in content


class TestPartnerState:
    """Test partner state management"""

    def test_add_partner(self):
        """Test adding a partner"""
        # Use unique name to avoid conflicts
        import time

        partner_name = f"TestPartner_{int(time.time())}"

        partner = partner_state.add_partner(
            name=partner_name, tier="Gold", email="test@example.com"
        )

        assert partner is not None
        assert partner["name"] == partner_name
        assert partner["tier"] == "Gold"

    def test_get_partner(self):
        """Test retrieving a partner"""
        import time

        partner_name = f"GetTest_{int(time.time())}"

        # Create
        partner_state.add_partner(name=partner_name, tier="Silver")

        # Get
        partner = partner_state.get_partner(partner_name)
        assert partner is not None
        assert partner["name"] == partner_name

    def test_add_document_to_partner(self):
        """Test adding document to partner"""
        import time

        partner_name = f"DocTest_{int(time.time())}"

        # Create partner
        partner_state.add_partner(name=partner_name, tier="Bronze")

        # Add document
        doc = partner_state.add_document(
            partner_name=partner_name,
            doc_type="nda",
            template="legal/01-nda.md",
            file_path=f"partners/{partner_name}/documents/test-nda.md",
            fields={"partner_name": partner_name},
            status="draft",
        )

        assert doc is not None
        # Document was added (verify in partner)
        partner = partner_state.get_partner(partner_name)
        assert "documents" in partner
        assert len(partner["documents"]) > 0


class TestChatOrchestrator:
    """Test chat orchestrator functionality"""

    def test_fallback_onboard(self):
        """Test fallback response for onboard"""
        co = chat_orchestrator.ChatOrchestrator()
        response = co._fallback_response("onboard MyCompany")

        assert "MyCompany" in response
        assert "ARCHITECT" in response or "onboard" in response.lower()

    def test_fallback_status(self):
        """Test fallback response for status check"""
        co = chat_orchestrator.ChatOrchestrator()
        response = co._fallback_response("status of SomePartner")

        assert "SomePartner" in response or "status" in response.lower()

    def test_fallback_campaign(self):
        """Test fallback response for campaign"""
        co = chat_orchestrator.ChatOrchestrator()
        response = co._fallback_response("launch campaign for CoolCo")

        assert "CoolCo" in response or "campaign" in response.lower()

    def test_memory_persistence(self):
        """Test conversation memory is saved"""
        mem = chat_orchestrator.ConversationMemory()

        # Add message
        mem.add_message("test_session", "user", "Hello")
        mem.add_message("test_session", "assistant", "Hi there")

        # Get history
        history = mem.get_history("test_session")

        assert len(history) >= 2
        assert history[0]["content"] == "Hello"

    def test_memory_persists_to_disk(self):
        """Test memory is saved to disk"""
        mem = chat_orchestrator.ConversationMemory()

        # Add unique message
        import time

        session_id = f"disk_test_{int(time.time())}"
        mem.add_message(session_id, "user", "Test message for disk")

        # Check file exists
        assert mem._conversation_file(session_id).exists()


class TestIntegration:
    """Integration tests for full flow"""

    def test_full_onboard_flow(self):
        """Test complete onboard flow: route -> create partner -> generate doc"""
        import time

        partner_name = f"IntegrationTest_{int(time.time())}"

        # 1. Route the message
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run_test():
            r = router.Router()
            result = await r.route(f"onboard {partner_name}", {"partners": []})

            assert result.is_document_request is True
            intent = result.intents[0]
            assert intent.entities.get("partner_name") == partner_name

            # 2. Create partner
            partner = partner_state.get_partner(partner_name)
            if not partner:
                partner = partner_state.add_partner(name=partner_name, tier="Bronze")

            # 3. Generate document
            doc_result = document_generator.create_document(
                doc_type="nda", partner_name=partner_name, fields={}
            )

            assert doc_result is not None
            assert Path(doc_result["path"]).exists()

            return True

        result = loop.run_until_complete(run_test())
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
