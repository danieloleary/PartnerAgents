#!/usr/bin/env python3
"""
PartnerOS Web Interface
Founder's Cockpit - Chat-based partner management with AI swarm
"""

import os
import sys
import re
import time
import hashlib

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import uvicorn

from partner_agents import partner_state, router, document_generator, chat_orchestrator

# Rate limiting
rate_limit_store = {}
RATE_LIMIT = 20
RATE_WINDOW = 60
response_cache = {}
CACHE_TTL_SECONDS = 300

app = FastAPI()


def check_rate_limit(client_ip: str) -> bool:
    """Check if client is within rate limit."""
    now = time.time()
    if client_ip not in rate_limit_store:
        rate_limit_store[client_ip] = []

    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip] if now - t < RATE_WINDOW
    ]

    if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
        return False

    rate_limit_store[client_ip].append(now)
    return True


@app.get("/")
async def root():
    return HTMLResponse(HTML)


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    api_key = data.get("apiKey", "") or os.environ.get("OPENROUTER_API_KEY", "")
    model = data.get("model", "qwen/qwen3.5-plus-02-15")

    if not user_message or len(user_message.strip()) == 0:
        return JSONResponse({"response": "Please enter a message.", "agent": "system"})

    if len(user_message) > 5000:
        return JSONResponse(
            {"response": "Message too long (max 5000 chars).", "agent": "system"}
        )

    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_ip):
        return JSONResponse(
            {
                "response": "Rate limited. Wait a moment.",
                "agent": "system",
                "rate_limited": True,
            },
            status_code=429,
        )

    sanitized = re.sub(r"<[^>]*?>", "", user_message)

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
                return JSONResponse(
                    {
                        "response": "What's the partner company name?",
                        "agent": "system",
                    }
                )

            # Create partner if doesn't exist
            partner = partner_state.get_partner(partner_name)
            if not partner:
                partner = partner_state.add_partner(
                    name=partner_name,
                    tier=intent.entities.get("tier", "Bronze"),
                )

            # Handle action types (onboard, campaign, etc.) - create NDA by default
            doc_type = intent.name
            if intent.type == "action":
                # Actions get an NDA document created
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

                return JSONResponse(
                    {
                        "response": f"Created **{doc_type.upper()}** for **{partner_name}** and started **{intent.name}** process!\n\nSaved to: `{doc_result['relative_path']}`",
                        "agent": "engine",
                        "document": {
                            "type": doc_type,
                            "partner": partner_name,
                            "path": doc_result["relative_path"],
                        },
                    }
                )

        raise Exception("Not document request")

    except Exception:
        # Use chat orchestrator
        api_key_value = api_key

        async def llm_wrapper(system_prompt: str, user_msg: str, history: list) -> str:
            if not api_key_value:
                return chat_orchestrator.orchestrator._fallback_response(user_msg)

            key = api_key_value.strip()
            if len(key) < 20 or not key.startswith("sk-"):
                return "Please configure your API key in Settings (Cmd+K)"

            messages = [{"role": "system", "content": system_prompt}]
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_msg})

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {key}",
                            "Content-Type": "application/json",
                        },
                        json={"model": model, "messages": messages},
                        timeout=30.0,
                    )
                    if response.status_code != 200:
                        return (
                            f"API Error ({response.status_code}): {response.text[:100]}"
                        )

                    result = response.json()
                    choices = result.get("choices", [])
                    if not choices:
                        return "No response from AI."

                    return choices[0].get("message", {}).get("content", "No response")
            except Exception as e:
                return f"Error: {str(e)}"

        try:
            result = await chat_orchestrator.chat(
                sanitized, conv_id="default", llm_client=llm_wrapper
            )
            return JSONResponse(
                {
                    "response": result.get("response", "No response"),
                    "agent": result.get("agent", "swarm"),
                }
            )
        except Exception as e:
            return JSONResponse(
                {
                    "response": chat_orchestrator.orchestrator._fallback_response(
                        sanitized
                    ),
                    "agent": "swarm",
                }
            )


@app.get("/api/partners")
async def get_partners():
    partners = partner_state.list_partners()
    stats = partner_state.get_partner_stats()
    return JSONResponse({"partners": partners, "stats": stats})


@app.post("/api/partners")
async def create_partner(request: Request):
    data = await request.json()
    partner = partner_state.add_partner(
        name=data.get("name", ""),
        tier=data.get("tier", "Bronze"),
        contact=data.get("contact", ""),
        email=data.get("email", ""),
    )
    return JSONResponse(partner)


@app.get("/api/partners/{name}")
async def get_partner(name: str):
    partner = partner_state.get_partner(name)
    if partner:
        return JSONResponse(partner)
    return JSONResponse({"error": "Partner not found"}, status_code=404)


@app.delete("/api/partners/{name}")
async def delete_partner(name: str):
    success = partner_state.delete_partner(name)
    if success:
        return JSONResponse({"success": True, "message": f"Partner '{name}' deleted"})
    return JSONResponse({"error": "Partner not found"}, status_code=404)


@app.get("/api/memory")
async def get_memory():
    mem = chat_orchestrator.memory.get_or_create("default")
    return JSONResponse(
        {
            "messages": [
                {"role": m.role, "content": m.content[:200], "agent": m.agent}
                for m in mem.messages[-20:]
            ],
            "context": mem.context,
        }
    )


@app.delete("/api/memory")
async def clear_memory():
    chat_orchestrator.memory.clear("default")
    return JSONResponse({"success": True})


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PartnerOS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #09090b;
            --bg-secondary: #18181b;
            --bg-tertiary: #27272a;
            --border: #27272a;
            --text: #fafafa;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --accent: #8b5cf6;
            --accent-hover: #7c3aed;
            --user-bg: #fafafa;
            --user-text: #18181b;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        html, body {
            height: 100%;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text);
            letter-spacing: -0.02em;
        }
        
        .cockpit {
            display: grid;
            grid-template-columns: auto 1fr 320px;
            height: 100vh;
            overflow: hidden;
        }
        
        /* Left Nav */
        .nav {
            width: 240px;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            padding: 16px;
            transition: width 0.2s;
        }
        
        .nav.collapsed { width: 60px; }
        
        .nav-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px;
            margin-bottom: 24px;
        }
        
        .nav-logo {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #8b5cf6, #06b6d4);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
        }
        
        .nav-title {
            font-weight: 600;
            font-size: 16px;
        }
        
        .nav.collapsed .nav-title { display: none; }
        
        .nav-section {
            margin-bottom: 24px;
        }
        
        .nav-section-title {
            font-size: 11px;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 8px;
            padding: 0 8px;
        }
        
        .nav.collapsed .nav-section-title { display: none; }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 12px;
            border-radius: 8px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s;
            font-size: 14px;
        }
        
        .nav-item:hover {
            background: var(--bg-tertiary);
            color: var(--text);
        }
        
        .nav-item.active {
            background: var(--accent);
            color: white;
        }
        
        .nav-icon { font-size: 16px; }
        
        .nav.collapsed .nav-item span { display: none; }
        
        .nav-toggle {
            margin-top: auto;
            padding: 8px;
            background: transparent;
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-muted);
            cursor: pointer;
        }
        
        .nav-toggle:hover { color: var(--text); }
        
        /* Center - Chat Arena */
        .arena {
            display: flex;
            flex-direction: column;
            height: 100vh;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
        }
        
        .arena-header {
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .arena-title {
            font-weight: 600;
            font-size: 14px;
        }
        
        .cmd-hint {
            font-size: 12px;
            color: var(--text-muted);
            background: var(--bg-secondary);
            padding: 4px 8px;
            border-radius: 4px;
            border: 1px solid var(--border);
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
        }
        
        .message {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
            max-width: 100%;
        }
        
        .message-user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        .message-user .message-content {
            background: var(--user-bg);
            color: var(--user-text);
        }
        
        .message-assistant .message-content {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
        }
        
        .message-avatar {
            width: 28px;
            height: 28px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            flex-shrink: 0;
        }
        
        .message-assistant .message-avatar {
            background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        }
        
        .message-user .message-avatar {
            background: var(--bg-tertiary);
        }
        
        .input-area {
            padding: 16px 24px 24px;
            border-top: 1px solid var(--border);
        }
        
        .input-wrapper {
            position: relative;
            max-width: 100%;
        }
        
        .input-field {
            width: 100%;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px 50px 14px 16px;
            color: var(--text);
            font-size: 14px;
            font-family: inherit;
            resize: none;
            outline: none;
            transition: border-color 0.15s, box-shadow 0.15s;
        }
        
        .input-field:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
        }
        
        .input-send {
            position: absolute;
            right: 12px;
            bottom: 10px;
            background: var(--accent);
            border: none;
            border-radius: 6px;
            color: white;
            width: 28px;
            height: 28px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.15s;
        }
        
        .input-send:hover { background: var(--accent-hover); }
        
        /* Right - Inspector */
        .inspector {
            background: var(--bg-secondary);
            border-left: 1px solid var(--border);
            padding: 16px;
            overflow-y: auto;
        }
        
        .inspector-header {
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 16px;
        }
        
        .inspector-section {
            margin-bottom: 24px;
        }
        
        .inspector-title {
            font-size: 11px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }
        
        .inspector-card {
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px;
            font-size: 12px;
        }
        
        .inspector-card pre {
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 11px;
            color: var(--text-secondary);
            white-space: pre-wrap;
            word-break: break-all;
            max-height: 200px;
            overflow-y: auto;
        }
        
        /* Welcome */
        .welcome {
            text-align: center;
            padding: 60px 24px;
        }
        
        .welcome h1 {
            font-size: 28px;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #8b5cf6, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .welcome p {
            color: var(--text-secondary);
            margin-bottom: 24px;
        }
        
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            max-width: 400px;
            margin: 0 auto;
        }
        
        .quick-action {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.15s;
            text-align: left;
        }
        
        .quick-action:hover {
            border-color: var(--accent);
            background: var(--bg-tertiary);
        }
        
        .quick-action h3 {
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .quick-action p {
            font-size: 11px;
            color: var(--text-muted);
            margin: 0;
        }
        
        /* Command Palette */
        .cmd-palette {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: flex-start;
            justify-content: center;
            padding-top: 100px;
            z-index: 100;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.15s;
        }
        
        .cmd-palette.open {
            opacity: 1;
            pointer-events: auto;
        }
        
        .cmd-content {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            width: 500px;
            max-width: 90vw;
            overflow: hidden;
        }
        
        .cmd-input {
            width: 100%;
            background: transparent;
            border: none;
            border-bottom: 1px solid var(--border);
            padding: 16px;
            color: var(--text);
            font-size: 16px;
            font-family: inherit;
            outline: none;
        }
        
        .cmd-input::placeholder {
            color: var(--text-muted);
        }
        
        .cmd-options {
            max-height: 300px;
            overflow-y: auto;
        }
        
        .cmd-group {
            padding: 8px;
        }
        
        .cmd-group-title {
            font-size: 10px;
            text-transform: uppercase;
            color: var(--text-muted);
            padding: 8px;
        }
        
        .cmd-option {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 12px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .cmd-option:hover, .cmd-option.selected {
            background: var(--bg-tertiary);
        }
        
        .cmd-option-icon {
            width: 24px;
            text-align: center;
        }
        
        /* Loading */
        .typing {
            display: flex;
            gap: 4px;
            padding: 8px 0;
        }
        
        .typing-dot {
            width: 6px;
            height: 6px;
            background: var(--text-muted);
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { opacity: 0.3; }
            30% { opacity: 1; }
        }
        
        /* Agent badges */
        .agent-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 8px;
            background: var(--bg-tertiary);
            border-radius: 12px;
            font-size: 11px;
            color: var(--text-secondary);
        }
        
        /* Error state */
        .error-card {
            background: #1a1515;
            border: 1px solid #3f2525;
            border-radius: 8px;
            padding: 12px;
            font-family: monospace;
            font-size: 12px;
            color: #f87171;
        }
        
        .error-resync {
            margin-top: 8px;
            background: #3f2525;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
            color: #f87171;
            font-size: 12px;
            cursor: pointer;
        }
        
        .error-resync:hover { background: #4f3535; }
    </style>
</head>
<body>
    <div class="cockpit">
        <!-- Left Nav -->
        <nav class="nav" id="nav">
            <div class="nav-header">
                <div class="nav-logo">PO</div>
                <span class="nav-title">PartnerOS</span>
            </div>
            
            <div class="nav-section">
                <div class="nav-section-title">Partners</div>
                <div class="nav-item active">
                    <span class="nav-icon">💬</span>
                    <span>Chat</span>
                </div>
                <div class="nav-item" onclick="loadPartners()">
                    <span class="nav-icon">👥</span>
                    <span>All Partners</span>
                </div>
            </div>
            
            <div class="nav-section">
                <div class="nav-section-title">Quick</div>
                <div class="nav-item">
                    <span class="nav-icon">📄</span>
                    <span>Documents</span>
                </div>
                <div class="nav-item">
                    <span class="nav-icon">📢</span>
                    <span>Campaigns</span>
                </div>
            </div>
            
            <button class="nav-toggle" onclick="toggleNav()">☰</button>
        </nav>
        
        <!-- Center - Chat -->
        <main class="arena">
            <header class="arena-header">
                <div class="arena-title">New Chat</div>
                <div style="display: flex; gap: 12px; align-items: center;">
                    <button onclick="showSettings()" style="background: var(--bg-tertiary); border: 1px solid var(--border); border-radius: 6px; padding: 6px 12px; color: var(--text-secondary); cursor: pointer; font-size: 13px;">⚙️ Settings</button>
                </div>
            </header>
            
            <div class="messages" id="messages">
                <div class="welcome" id="welcome">
                    <h1>PartnerOS</h1>
                    <p>Your AI partner team. Try these:</p>
                    <div class="quick-actions">
                        <div class="quick-action" onclick="sendMessage('onboard Vertex')">
                            <h3>Onboard Partner</h3>
                            <p>Start onboarding a new partner</p>
                        </div>
                        <div class="quick-action" onclick="sendMessage('status of Vertex')">
                            <h3>Check Status</h3>
                            <p>See where things stand</p>
                        </div>
                        <div class="quick-action" onclick="sendMessage('launch campaign for Vertex')">
                            <h3>Launch Campaign</h3>
                            <p>Start a co-marketing campaign</p>
                        </div>
                        <div class="quick-action" onclick="sendMessage('register a deal for Vertex, $50000')">
                            <h3>Register Deal</h3>
                            <p>Record a new deal</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="input-area">
                <div class="input-wrapper">
                    <textarea class="input-field" id="input" placeholder="Message PartnerOS..." rows="1" onkeydown="if(event.key==='Enter' && !event.shiftKey) { event.preventDefault(); sendMessage(); }"></textarea>
                    <button class="input-send" onclick="sendMessage()">↑</button>
                </div>
            </div>
        </main>
        
        <!-- Right - Inspector -->
        <aside class="inspector" id="inspector">
            <div class="inspector-header">INSPECTOR</div>
            
            <div class="inspector-section">
                <div class="inspector-title">Partner Context</div>
                <div class="inspector-card">
                    <pre id="partner-context">No partner selected</pre>
                </div>
            </div>
            
            <div class="inspector-section">
                <div class="inspector-title">Agent Activity</div>
                <div class="inspector-card">
                    <pre id="agent-activity">Waiting...</pre>
                </div>
            </div>
        </aside>
    </div>
    
    <!-- Command Palette -->
    <div class="cmd-palette" id="cmd-palette">
        <div class="cmd-content">
            <input type="text" class="cmd-input" id="cmd-input" placeholder="Type a command...">
            <div class="cmd-options" id="cmd-options"></div>
        </div>
    </div>

    <script>
        // State
        let currentPartner = null;
        
        // Load API key
        function getApiKey() {
            return localStorage.getItem('partneros_api_key') || '';
        }
        
        function getModel() {
            return localStorage.getItem('partneros_model') || 'qwen/qwen3.5-plus-02-15';
        }
        
        // Toggle nav
        function toggleNav() {
            document.getElementById('nav').classList.toggle('collapsed');
        }
        
        // Command palette
        const commands = [
            { group: 'Settings', icon: '⚙️', label: 'OpenRouter API Key', action: () => showSettings() },
            { group: 'Settings', icon: '🤖', label: 'Change Model', action: () => showSettings() },
            { group: 'Memory', icon: '🗑️', label: 'Clear Conversation', action: clearMemory },
            { group: 'Memory', icon: '👤', label: 'Clear Partner Context', action: clearPartner },
            { group: 'Actions', icon: '➕', label: 'New Chat', action: newChat },
            { group: 'Debug', icon: '📄', label: 'View Raw JSON', action: viewJson },
            { group: 'Debug', icon: '🔧', label: 'Agent Activity Log', action: viewActivity },
        ];
        
        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                toggleCmdPalette();
            }
            if (e.key === 'Escape') {
                closeCmdPalette();
            }
        });
        
        function toggleCmdPalette() {
            const palette = document.getElementById('cmd-palette');
            palette.classList.toggle('open');
            if (palette.classList.contains('open')) {
                document.getElementById('cmd-input').focus();
                renderCmdOptions('');
            }
        }
        
        function closeCmdPalette() {
            document.getElementById('cmd-palette').classList.remove('open');
        }
        
        document.getElementById('cmd-input').addEventListener('input', (e) => {
            renderCmdOptions(e.target.value);
        });
        
        document.getElementById('cmd-palette').addEventListener('click', (e) => {
            if (e.target === document.getElementById('cmd-palette')) {
                closeCmdPalette();
            }
        });
        
        function renderCmdOptions(filter) {
            const container = document.getElementById('cmd-options');
            const filtered = commands.filter(c => c.label.toLowerCase().includes(filter.toLowerCase()));
            
            let html = '';
            let currentGroup = '';
            filtered.forEach(cmd => {
                if (cmd.group !== currentGroup) {
                    currentGroup = cmd.group;
                    html += `<div class="cmd-group-title">${cmd.group}</div>`;
                }
                html += `<div class="cmd-option" onclick="${cmd.action.name}(); closeCmdPalette();"><span class="cmd-option-icon">${cmd.icon}</span>${cmd.label}</div>`;
            });
            container.innerHTML = html;
        }
        
        function showSettings() {
            const key = prompt('OpenRouter API Key:', getApiKey());
            if (key !== null) {
                localStorage.setItem('partneros_api_key', key);
            }
            const model = prompt('Model (qwen/qwen3.5-plus-02-15):', getModel());
            if (model !== null) {
                localStorage.setItem('partneros_model', model);
            }
        }
        
        function clearMemory() {
            fetch('/api/memory', { method: 'DELETE' }).then(() => {
                document.getElementById('messages').innerHTML = '<div class="welcome" id="welcome"><h1>PartnerOS</h1><p>Memory cleared.</p></div>';
                document.getElementById('agent-activity').textContent = 'Memory cleared';
            });
        }
        
        function clearPartner() {
            currentPartner = null;
            document.getElementById('partner-context').textContent = 'No partner selected';
        }
        
        function newChat() {
            location.reload();
        }
        
        function viewJson() {
            fetch('/api/memory').then(r => r.json()).then(data => {
                document.getElementById('partner-context').textContent = JSON.stringify(data, null, 2);
            });
        }
        
        function viewActivity() {
            document.getElementById('agent-activity').textContent = 'Loading...';
            fetch('/api/memory').then(r => r.json()).then(data => {
                const activity = data.messages.map(m => `${m.role}: ${m.agent || 'user'}`).join('\n');
                document.getElementById('agent-activity').textContent = activity || 'No activity';
            });
        }
        
        // Send message
        async function sendMessage(text) {
            const input = document.getElementById('input');
            const msg = text || input.value.trim();
            if (!msg) return;
            
            input.value = '';
            
            // Hide welcome
            const welcome = document.getElementById('welcome');
            if (welcome) welcome.style.display = 'none';
            
            // Add user message
            addMessage(msg, 'user');
            
            // Show typing
            showTyping();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: msg,
                        apiKey: getApiKey(),
                        model: getModel()
                    })
                });
                
                const data = await response.json();
                hideTyping();
                
                // Extract partner mention
                const partnerMatch = msg.match(/(?:for|of|with)\s+([A-Z][a-zA-Z]+)/);
                if (partnerMatch) {
                    currentPartner = partnerMatch[1];
                    document.getElementById('partner-context').textContent = `Partner: ${currentPartner}`;
                }
                
                // Update agent activity
                document.getElementById('agent-activity').textContent = `Agent: ${data.agent || 'swarm'}`;
                
                addMessage(data.response || 'No response', 'assistant', data.agent);
            } catch (e) {
                hideTyping();
                addError(e.message);
            }
        }
        
        function addMessage(content, role, agent) {
            const container = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = `message message-${role}`;
            
            const avatar = role === 'user' ? '👤' : '🤖';
            
            div.innerHTML = `
                <div class="message-avatar">${avatar}</div>
                <div class="message-content">${escapeHtml(content)}</div>
            `;
            
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
        
        function showTyping() {
            const container = document.getElementById('messages');
            const div = document.createElement('div');
            div.id = 'typing';
            div.className = 'message message-assistant';
            div.innerHTML = `
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div class="typing">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            `;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
        
        function hideTyping() {
            const typing = document.getElementById('typing');
            if (typing) typing.remove();
        }
        
        function addError(error) {
            const container = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'message message-assistant';
            div.innerHTML = `
                <div class="message-avatar">⚠️</div>
                <div class="message-content">
                    <div class="error-card">
                        ${escapeHtml(error)}
                        <button class="error-resync" onclick="sendMessage(document.getElementById('input').value)">Re-sync</button>
                    </div>
                </div>
            `;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Auto-resize input
        document.getElementById('input').addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 200) + 'px';
        });
        
        // Load partners
        function loadPartners() {
            fetch('/api/partners').then(r => r.json()).then(data => {
                document.getElementById('partner-context').textContent = JSON.stringify(data.partners, null, 2);
            });
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    print("🚀 Starting PartnerOS...")
    print("   Open http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
